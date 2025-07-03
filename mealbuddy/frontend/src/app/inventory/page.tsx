'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function InventoryScan() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [detectedItems, setDetectedItems] = useState([])
  const [matchingRecipes, setMatchingRecipes] = useState([])
  const [currentInventory, setCurrentInventory] = useState([])
  const [newItem, setNewItem] = useState({ item: '', quantity: '' })
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const fetchInventory = async () => {
      try {
        const res = await fetch('/api/v1/users/inventory', {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (res.ok) {
          const data = await res.json()
          setCurrentInventory(data.inventory || [])
        } else {
          console.error('Failed to fetch current inventory')
        }
      } catch (err) {
        console.error('Error fetching current inventory', err)
      }
    }
    fetchInventory()
  }, [router])

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0])
    setMessage('')
    setError('')
    setDetectedItems([])
    setMatchingRecipes([])
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file first.')
      return
    }

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const res = await fetch('/api/v1/users/inventory/scan', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      })

      if (res.ok) {
        const data = await res.json()
        setMessage(data.message + ": " + data.file_path)
        setDetectedItems(data.detected_items || [])
        setError('')

        // Merge detected items with current inventory for confirmation
        const mergedInventory = [...currentInventory];
        data.detected_items.forEach(detectedItem => {
          const existingIndex = mergedInventory.findIndex(item => item.item === detectedItem.item);
          if (existingIndex > -1) {
            // Update quantity if item exists
            mergedInventory[existingIndex].quantity = detectedItem.quantity; // Simple overwrite for now
          } else {
            mergedInventory.push(detectedItem);
          }
        });
        setCurrentInventory(mergedInventory);

        // Automatically fetch matching recipes after successful scan
        if (mergedInventory.length > 0) {
          await fetchMatchingRecipes(mergedInventory)
        }

      } else {
        const data = await res.json()
        setError(data.detail || 'Failed to upload image.')
        setMessage('')
        setDetectedItems([])
        setMatchingRecipes([])
      }
    } catch (err) {
      setError('An error occurred during upload.')
      setMessage('')
      setDetectedItems([])
      setMatchingRecipes([])
    }
  }

  const fetchMatchingRecipes = async (ingredients) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const res = await fetch('/api/v1/users/recipes/match', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(ingredients),
      })

      if (res.ok) {
        const data = await res.json()
        setMatchingRecipes(data)
      } else {
        const data = await res.json()
        setError(data.detail || 'Failed to fetch matching recipes.')
      }
    } catch (err) {
      setError('An error occurred while fetching recipes.')
    }
  }

  const handleInventoryChange = (index, field, value) => {
    const updatedInventory = [...currentInventory];
    updatedInventory[index][field] = value;
    setCurrentInventory(updatedInventory);
  };

  const handleRemoveItem = (index) => {
    const updatedInventory = currentInventory.filter((_, i) => i !== index);
    setCurrentInventory(updatedInventory);
  };

  const handleAddItem = () => {
    if (newItem.item && newItem.quantity) {
      setCurrentInventory([...currentInventory, newItem]);
      setNewItem({ item: '', quantity: '' });
    }
  };

  const handleSaveInventory = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const res = await fetch('/api/v1/users/inventory', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ pantry_inventory: currentInventory }),
      })

      if (res.ok) {
        setMessage('Inventory saved successfully!')
      } else {
        const data = await res.json()
        setError(data.detail || 'Failed to save inventory.')
      }
    } catch (err) {
      setError('An error occurred while saving inventory.')
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h1 className="text-2xl font-bold text-center mb-4">Scan Your Fridge/Pantry</h1>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="file_upload">
            Upload Image
          </label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="file_upload"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
          />
        </div>
        {message && <p className="text-green-500 text-xs italic mb-4">{message}</p>}
        {error && <p className="text-red-500 text-xs italic mb-4">{error}</p>}
        <div className="flex items-center justify-between">
          <button
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
            onClick={handleUpload}
          >
            Upload and Scan
          </button>
        </div>

        {currentInventory.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-2">Current Inventory:</h2>
            <ul>
              {currentInventory.map((item, index) => (
                <li key={index} className="text-gray-700 flex justify-between items-center mb-2">
                  <input
                    type="text"
                    value={item.item}
                    onChange={(e) => handleInventoryChange(index, 'item', e.target.value)}
                    className="shadow appearance-none border rounded py-1 px-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-1/2 mr-2"
                  />
                  <input
                    type="text"
                    value={item.quantity}
                    onChange={(e) => handleInventoryChange(index, 'quantity', e.target.value)}
                    className="shadow appearance-none border rounded py-1 px-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-1/4 mr-2"
                  />
                  <button
                    className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-xs"
                    onClick={() => handleRemoveItem(index)}
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
            <div className="mt-4 flex">
              <input
                type="text"
                placeholder="New Item"
                value={newItem.item}
                onChange={(e) => setNewItem({ ...newItem, item: e.target.value })}
                className="shadow appearance-none border rounded py-1 px-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-1/2 mr-2"
              />
              <input
                type="text"
                placeholder="Quantity"
                value={newItem.quantity}
                onChange={(e) => setNewItem({ ...newItem, quantity: e.target.value })}
                className="shadow appearance-none border rounded py-1 px-2 text-gray-700 leading-tight focus:outline-none focus:shadow-outline w-1/4 mr-2"
              />
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-1 px-2 rounded text-xs"
                onClick={handleAddItem}
              >
                Add Item
              </button>
            </div>
            <button
              className="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              onClick={handleSaveInventory}
            >
              Save Inventory
            </button>
          </div>
        )}

        {matchingRecipes.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-2">Matching Recipes:</h2>
            <ul>
              {matchingRecipes.map((recipe, index) => (
                <li key={index} className="text-gray-700">
                  <strong>{recipe.name}</strong> - Needs: {recipe.ingredients_needed.join(", ")}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}