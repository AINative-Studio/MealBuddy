'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function GroceryList() {
  const [groceryListData, setGroceryListData] = useState(null)
  const [error, setError] = useState('')
  const [instacartMessage, setInstacartMessage] = useState('')
  const [instacartError, setInstacartError] = useState('')
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const fetchGroceryList = async () => {
      try {
        const res = await fetch('/api/v1/users/grocery-list', {
          headers: { Authorization: `Bearer ${token}` },
        })

        if (res.ok) {
          const data = await res.json()
          setGroceryListData(data)
        } else {
          const data = await res.json()
          setError(data.detail || 'Failed to fetch grocery list.')
        }
      } catch (err) {
        setError('An error occurred while fetching the grocery list.')
      }
    }

    fetchGroceryList()
  }, [router])

  const handleInstacartOrder = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    setInstacartMessage('')
    setInstacartError('')

    try {
      const res = await fetch('/api/v1/users/shopping/instacart', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (res.ok) {
        const data = await res.json()
        setInstacartMessage(data.message + ` Order ID: ${data.order_id}. Estimated Delivery: ${data.estimated_delivery_time}. Total Cost: ${data.total_cost}`)
      } else {
        const data = await res.json()
        setInstacartError(data.detail || 'Failed to place Instacart order.')
      }
    } catch (err) {
      setInstacartError('An error occurred while placing the Instacart order.')
    }
  }

  const handleExportCsv = () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }
    // Trigger the download by navigating to the API endpoint
    window.open(`/api/v1/users/grocery-list/export/csv?token=${token}`, '_blank');
  };

  const handleExportText = () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }
    // Trigger the download by navigating to the API endpoint
    window.open(`/api/v1/users/grocery-list/export/text?token=${token}`, '_blank');
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-md bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
        <h1 className="text-2xl font-bold text-center mb-4">Your Grocery List</h1>
        {error && <p className="text-red-500 text-xs italic mb-4">{error}</p>}
        {groceryListData && groceryListData.items.length > 0 ? (
          <>
            <ul>
              {groceryListData.items.map((item, index) => (
                <li key={index} className="text-gray-700">{item.item} ({item.quantity}) - ${item.estimated_price?.toFixed(2)}</li>
              ))}
            </ul>
            <p className="mt-4 text-lg font-semibold">Total Estimated Cost: ${groceryListData.total_estimated_cost?.toFixed(2)}</p>
            {groceryListData.budget_optimization_message && (
              <p className="text-sm text-gray-600 mt-2">{groceryListData.budget_optimization_message}</p>
            )}
            <div className="mt-6 flex justify-between">
              <button
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleInstacartOrder}
              >
                Order with Instacart
              </button>
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleExportCsv}
              >
                Export to CSV
              </button>
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                onClick={handleExportText}
              >
                Export to Text
              </button>
            </div>
            {instacartMessage && <p className="text-green-500 text-xs italic mt-2">{instacartMessage}</p>}
            {instacartError && <p className="text-red-500 text-xs italic mt-2">{instacartError}</p>}
          </>
        ) : (
          <p>No items in your grocery list.</p>
        )}
      </div>
    </div>
  )
}
