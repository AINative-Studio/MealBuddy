from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.api.v1.deps import get_current_active_user
from app.models.user import User
from app.schemas.user import UserInventoryUpdate
import os
import uuid
import base64

from app.services.llama_service import analyze_image_with_llama

router = APIRouter()

UPLOAD_DIR = "./uploads"

@router.post("/inventory/scan")
async def scan_inventory_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload an image of fridge/pantry for inventory scanning.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_extension = file.filename.split(".")[-1]
    if file_extension not in ["jpg", "jpeg", "png", "gif"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only JPG, JPEG, PNG, GIF are allowed.")

    # Read file content and encode to base64
    file_content = await file.read()
    image_data_base64 = base64.b64encode(file_content).decode("utf-8")

    # Call Llama service for image analysis
    detected_items = await analyze_image_with_llama(image_data_base64)

    # Optionally save the uploaded file (for debugging or future use)
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    try:
        with open(file_path, "wb") as f:
            f.write(file_content)
    except Exception as e:
        print(f"Error saving uploaded file: {e}")
        # Don't raise HTTPException here, as the main task (LLM analysis) was successful

    return {"message": "Image processed successfully", "detected_items": detected_items}

@router.put("/inventory")
async def update_user_inventory(
    inventory_update: UserInventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Manually update the user's pantry inventory.
    """
    current_user.pantry_inventory = inventory_update.pantry_inventory
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"message": "Pantry inventory updated successfully", "inventory": current_user.pantry_inventory}

@router.get("/inventory")
async def get_user_inventory(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get the current user's pantry inventory.
    """
    return {"inventory": current_user.pantry_inventory}
