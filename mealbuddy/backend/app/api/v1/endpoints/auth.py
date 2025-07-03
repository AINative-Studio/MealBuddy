from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.db.base import get_db
from app.models.user import User
from app.schemas.user import (
    User as UserSchema,
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    OnboardingData
)
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user,
    create_user as create_user_service,
    update_user_last_login,
    get_password_hash
)
import httpx

router = APIRouter()

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

@router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Authenticate user
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    await update_user_last_login(db, user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Set secure HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=not settings.DEBUG,  # Secure flag in production
        samesite="lax"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserSchema)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create new user without the need to be logged in
    """
    try:
        user = await create_user_service(db, user_in)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user
    """
    return current_user


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    """
    Logout by removing the access token cookie
    """
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}


@router.post("/onboarding", response_model=UserSchema)
async def complete_onboarding(
    onboarding_data: OnboardingData,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Complete user onboarding with profile and preference data
    """
    try:
        # Update user profile data
        for field, value in onboarding_data.dict(exclude_unset=True).items():
            setattr(current_user, field, value)
        
        # Mark onboarding as completed
        current_user.onboarding_completed = True
        
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user profile"
        )


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Refresh access token
    """
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/google-login")
async def google_login():
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google Client ID not configured")

    redirect_uri = f"{settings.SERVER_HOST}{settings.API_V1_STR}/auth/google-callback"
    scope = "openid profile email"
    google_auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}&scope={scope}"
    )
    return RedirectResponse(google_auth_url)


@router.get("/google-callback", response_model=Token)
async def google_callback(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth credentials not configured")

    redirect_uri = f"{settings.SERVER_HOST}{settings.API_V1_STR}/auth/google-callback"

    async with httpx.AsyncClient() as client:
        # Exchange authorization code for access token
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data["access_token"]

        # Get user info from Google
        user_info_response = await client.get(
            GOOGLE_USER_INFO_URL,
            headers={
                "Authorization": f"Bearer {access_token}"
            },
        )
        user_info_response.raise_for_status()
        user_info = user_info_response.json()

        google_id = user_info["sub"]
        email = user_info["email"]
        full_name = user_info.get("name")

        # Check if user exists in our DB
        user = await db.scalar(select(User).where(User.google_id == google_id))

        if not user:
            # If user doesn't exist, check by email (for existing users who might link Google later)
            user = await db.scalar(select(User).where(User.email == email))
            if user:
                # Link existing user with Google ID
                user.google_id = google_id
                db.add(user)
                await db.commit()
                await db.refresh(user)
            else:
                # Create new user
                user_create_data = UserCreate(
                    email=email,
                    password=get_password_hash(str(uuid.uuid4())),
                    password_confirm=get_password_hash(str(uuid.uuid4())),
                    full_name=full_name,
                )
                user = await create_user_service(db, user_create_data)
                user.google_id = google_id
                db.add(user)
                await db.commit()
                await db.refresh(user)

        # Generate our own JWT token for the user
        our_access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        our_access_token = create_access_token(
            data={"sub": user.email}, expires_delta=our_access_token_expires
        )

        response.set_cookie(
            key="access_token",
            value=f"Bearer {our_access_token}",
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=not settings.DEBUG,
            samesite="lax"
        )

        return {"access_token": our_access_token, "token_type": "bearer"}