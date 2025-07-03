'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Bar, Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LineElement
)

const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];

export default function Dashboard() {
  const [mealPlan, setMealPlan] = useState(null)
  const [nutrition, setNutrition] = useState(null)
  const [swapError, setSwapError] = useState('')
  const [feedbackRecipeName, setFeedbackRecipeName] = useState('')
  const [feedbackRating, setFeedbackRating] = useState(0)
  const [feedbackComment, setFeedbackComment] = useState('')
  const [feedbackMessage, setFeedbackMessage] = useState('')
  const [feedbackError, setFeedbackError] = useState('')
  const [weightInput, setWeightInput] = useState('')
  const [weightLog, setWeightLog] = useState([])
  const [weightLogMessage, setWeightLogMessage] = useState('')
  const [weightLogError, setWeightLogError] = useState('')
  const [leftoverSuggestions, setLeftoverSuggestions] = useState([])
  const [leftoverError, setLeftoverError] = useState('')
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const fetchDashboardData = async () => {
      try {
        const [mealPlanRes, nutritionRes, weightLogRes, leftoverRes] = await Promise.all([
          fetch('/api/v1/users/meal-plan', {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch('/api/v1/users/nutrition-dashboard', {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch('/api/v1/users/weight-log', {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch('/api/v1/users/meal-plan/leftovers', {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ])

        if (mealPlanRes.ok) {
          const mealPlanData = await mealPlanRes.json()
          setMealPlan(mealPlanData)
        }

        if (nutritionRes.ok) {
          const nutritionData = await nutritionRes.json()
          setNutrition(nutritionData)
        }

        if (weightLogRes.ok) {
          const weightLogData = await weightLogRes.json()
          setWeightLog(weightLogData)
        }

        if (leftoverRes.ok) {
          const leftoverData = await leftoverRes.json()
          setLeftoverSuggestions(leftoverData)
        } else {
          const data = await leftoverRes.json()
          setLeftoverError(data.detail || 'Failed to fetch leftover suggestions.')
        }

      } catch (error) {
        console.error('Failed to fetch dashboard data', error)
      }
    }

    fetchDashboardData()
  }, [router])

  const handleSwapMeal = async (day, mealType) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    setSwapError('')

    try {
      const res = await fetch('/api/v1/users/meal-plan/swap', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ day, meal_type: mealType }),
      })

      if (res.ok) {
        const updatedMealPlan = await res.json()
        setMealPlan(updatedMealPlan)
      } else {
        const data = await res.json()
        setSwapError(data.detail || 'Failed to swap meal.')
      }
    } catch (err) {
      setSwapError('An error occurred while swapping meal.')
    }
  }

  const handleShiftMealPlan = async (daysToShift) => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const res = await fetch('/api/v1/users/meal-plan/shift', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ days_to_shift: daysToShift }),
      })

      if (res.ok) {
        const shiftedMealPlan = await res.json()
        setMealPlan(shiftedMealPlan)
      } else {
        const data = await res.json()
        setError(data.detail || 'Failed to shift meal plan.')
      }
    } catch (err) {
      setError('An error occurred while shifting meal plan.')
    }
  }

  const handleSubmitFeedback = async (e) => {
    e.preventDefault()
    setFeedbackMessage('')
    setFeedbackError('')

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    if (!feedbackRecipeName || feedbackRating === 0) {
      setFeedbackError('Recipe name and rating are required.')
      return
    }

    try {
      const res = await fetch('/api/v1/users/recipe-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          recipe_name: feedbackRecipeName,
          rating: feedbackRating,
          comment: feedbackComment,
        }),
      })

      if (res.ok) {
        setFeedbackMessage('Feedback submitted successfully!')
        setFeedbackRecipeName('')
        setFeedbackRating(0)
        setFeedbackComment('')
      } else {
        const data = await res.json()
        setFeedbackError(data.detail || 'Failed to submit feedback.')
      }
    } catch (err) {
      setFeedbackError('An error occurred while submitting feedback.')
    }
  }

  const handleWeightLogSubmit = async (e) => {
    e.preventDefault()
    setWeightLogMessage('')
    setWeightLogError('')

    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    if (!weightInput || parseFloat(weightInput) <= 0) {
      setWeightLogError('Please enter a valid weight.')
      return
    }

    try {
      const res = await fetch('/api/v1/users/weight-log', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ weight_kg: parseFloat(weightInput) }),
      })

      if (res.ok) {
        const newLog = await res.json()
        setWeightLog([...weightLog, newLog].sort((a, b) => new Date(a.logged_at).getTime() - new Date(b.logged_at).getTime()))
        setWeightLogMessage('Weight logged successfully!')
        setWeightInput('')
      } else {
        const data = await res.json()
        setWeightLogError(data.detail || 'Failed to log weight.')
      }
    } catch (err) {
      setWeightLogError('An error occurred while logging weight.')
    }
  }

  const chartData = {
    labels: ['Calories', 'Protein', 'Carbs', 'Fat'],
    datasets: [
      {
        label: 'Daily Intake',
        data: nutrition ? [nutrition.calories, nutrition.protein, nutrition.carbs, nutrition.fat] : [0, 0, 0, 0],
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Daily Nutrition Overview',
      },
    },
  };

  const weightChartData = {
    labels: weightLog.map(log => new Date(log.logged_at).toLocaleDateString()),
    datasets: [
      {
        label: 'Weight (kg)',
        data: weightLog.map(log => log.weight_kg),
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const weightChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Weight Progress',
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  const isMealPlanStructured = mealPlan && mealPlan.is_structured;

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-4xl font-bold text-center mb-8">Your Dashboard</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <h2 className="text-2xl font-semibold mb-4">This Week's Meal Plan</h2>
          {swapError && <p className="text-red-500 text-xs italic mb-4">{swapError}</p>}
          <div className="mb-4">
            <button
              className={`bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mr-2 ${!isMealPlanStructured ? 'opacity-50 cursor-not-allowed' : ''}`}
              onClick={() => isMealPlanStructured && handleShiftMealPlan(1)}
              disabled={!isMealPlanStructured}
            >
              Shift Plan +1 Day
            </button>
            <button
              className={`bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline ${!isMealPlanStructured ? 'opacity-50 cursor-not-allowed' : ''}`}
              onClick={() => isMealPlanStructured && handleShiftMealPlan(-1)}
              disabled={!isMealPlanStructured}
            >
              Shift Plan -1 Day
            </button>
          </div>
          <div className="bg-white shadow-md rounded-lg p-4">
            {mealPlan ? (
              isMealPlanStructured ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {daysOfWeek.map(day => (
                    <div key={day} className="bg-gray-50 shadow-md rounded-lg p-4">
                      <h3 className="text-lg font-semibold capitalize">{day}</h3>
                      <ul>
                        <li>
                          <strong>Breakfast:</strong> {mealPlan[day]?.breakfast}
                          <button
                            className="ml-2 px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-700"
                            onClick={() => handleSwapMeal(day, 'breakfast')}
                          >
                            Swap
                          </button>
                        </li>
                        <li>
                          <strong>Lunch:</strong> {mealPlan[day]?.lunch}
                          <button
                            className="ml-2 px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-700"
                            onClick={() => handleSwapMeal(day, 'lunch')}
                          >
                            Swap
                          </button>
                        </li>
                        <li>
                          <strong>Dinner:</strong> {mealPlan[day]?.dinner}
                          <button
                            className="ml-2 px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-700"
                            onClick={() => handleSwapMeal(day, 'dinner')}
                          >
                            Swap
                          </button>
                        </li>
                      </ul>
                    </div>
                  ))}
                </div>
              ) : (
                <pre className="whitespace-pre-wrap">{mealPlan.unstructured_plan_text}</pre>
              )
            ) : (
              <p>Loading meal plan...</p>
            )}
          </div>

          <h2 className="text-2xl font-semibold mb-4 mt-8">Leftover Suggestions</h2>
          <div className="bg-white shadow-md rounded-lg p-4">
            {leftoverError && <p className="text-red-500 text-xs italic mb-4">{leftoverError}</p>}
            {leftoverSuggestions.length > 0 ? (
              <ul>
                {leftoverSuggestions.map((suggestion, index) => (
                  <li key={index} className="text-gray-700">{suggestion}</li>
                ))}
              </ul>
            ) : (
              <p>No leftover suggestions at the moment.</p>
            )}
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-semibold mb-4">Nutrition Dashboard</h2>
          <div className="bg-white shadow-md rounded-lg p-4 mb-8">
            {nutrition ? (
              <Bar data={chartData} options={chartOptions} />
            ) : (
              <p>Loading nutrition data...</p>
            )}
          </div>

          <h2 className="text-2xl font-semibold mb-4">Submit Recipe Feedback</h2>
          <div className="bg-white shadow-md rounded-lg p-4 mb-8">
            <form onSubmit={handleSubmitFeedback}>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="recipeName">
                  Recipe Name
                </label>
                <input
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="recipeName"
                  type="text"
                  value={feedbackRecipeName}
                  onChange={(e) => setFeedbackRecipeName(e.target.value)}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="rating">
                  Rating (1-5)
                </label>
                <input
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="rating"
                  type="number"
                  min="1"
                  max="5"
                  value={feedbackRating}
                  onChange={(e) => setFeedbackRating(parseInt(e.target.value))}
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="comment">
                  Comment (Optional)
                </label>
                <textarea
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="comment"
                  rows="3"
                  value={feedbackComment}
                  onChange={(e) => setFeedbackComment(e.target.value)}
                ></textarea>
              </div>
              {feedbackMessage && <p className="text-green-500 text-xs italic mb-4">{feedbackMessage}</p>}
              {feedbackError && <p className="text-red-500 text-xs italic mb-4">{feedbackError}</p>}
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                type="submit"
              >
                Submit Feedback
              </button>
            </form>
          </div>

          <h2 className="text-2xl font-semibold mb-4 mt-8">Weight Tracking</h2>
          <div className="bg-white shadow-md rounded-lg p-4">
            <form onSubmit={handleWeightLogSubmit}>
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="weightInput">
                  Log Your Weight (kg)
                </label>
                <input
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="weightInput"
                  type="number"
                  step="0.1"
                  value={weightInput}
                  onChange={(e) => setWeightInput(e.target.value)}
                  required
                />
              </div>
              {weightLogMessage && <p className="text-green-500 text-xs italic mb-4">{weightLogMessage}</p>}
              {weightLogError && <p className="text-red-500 text-xs italic mb-4">{weightLogError}</p>}
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                type="submit"
              >
                Log Weight
              </button>
            </form>

            {weightLog.length > 0 ? (
              <div className="mt-8">
                <h3 className="text-lg font-semibold mb-2">Weight History</h3>
                <Line data={weightChartData} options={weightChartOptions} />
              </div>
            ) : (
              <p className="mt-4">No weight data logged yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
