'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function Onboarding() {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    full_name: '',
    date_of_birth: '',
    gender: '',
    height_cm: '',
    weight_kg: '',
    activity_level: '',
    goal: '',
    dietary_restrictions: {},
    allergies: [],
    disliked_ingredients: [],
    preferred_cuisines: [],
    weekly_budget_cents: '',
    target_daily_calories: '',
    target_protein_g: '',
    target_carbs_g: '',
    target_fats_g: '',
  })
  const router = useRouter()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
        const { checked } = e.target as HTMLInputElement;
        setFormData(prev => ({
            ...prev,
            dietary_restrictions: {
                ...prev.dietary_restrictions,
                [name]: checked
            }
        }));
    } else {
        setFormData({ ...formData, [name]: value });
    }
  }

  const nextStep = () => setStep(step + 1)
  const prevStep = () => setStep(step - 1)

  const handleSubmit = async () => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    try {
      const res = await fetch('/api/v1/users/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      })

      if (res.ok) {
        router.push('/dashboard')
      } else {
        console.error('Failed to update profile')
      }
    } catch (error) {
      console.error('Failed to update profile', error)
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-lg">
        <h1 className="text-2xl font-bold text-center mb-8">Welcome to MealBuddy!</h1>
        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          {step === 1 && (
            <Step1 formData={formData} handleChange={handleChange} nextStep={nextStep} />
          )}
          {step === 2 && (
            <Step2 formData={formData} handleChange={handleChange} nextStep={nextStep} prevStep={prevStep} />
          )}
          {step === 3 && (
            <Step3 formData={formData} handleChange={handleChange} handleSubmit={handleSubmit} prevStep={prevStep} />
          )}
        </div>
      </div>
    </div>
  )
}

const Step1 = ({ formData, handleChange, nextStep }) => (
  <div>
    <h2 className="text-xl font-semibold mb-4">Step 1: Personal Information</h2>
    <div className="mb-4">
      <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="full_name">Full Name</label>
      <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="full_name" type="text" name="full_name" value={formData.full_name} onChange={handleChange} />
    </div>
    <div className="mb-4">
      <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="date_of_birth">Date of Birth</label>
      <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="date_of_birth" type="date" name="date_of_birth" value={formData.date_of_birth} onChange={handleChange} />
    </div>
    <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="gender">Gender</label>
        <select className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="gender" name="gender" value={formData.gender} onChange={handleChange}>
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
            <option value="prefer_not_to_say">Prefer not to say</option>
        </select>
    </div>
    <div className="flex justify-end">
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={nextStep}>Next</button>
    </div>
  </div>
);

const Step2 = ({ formData, handleChange, nextStep, prevStep }) => (
    <div>
        <h2 className="text-xl font-semibold mb-4">Step 2: Health & Fitness</h2>
        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="height_cm">Height (cm)</label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="height_cm" type="number" name="height_cm" value={formData.height_cm} onChange={handleChange} />
        </div>
        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="weight_kg">Weight (kg)</label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="weight_kg" type="number" name="weight_kg" value={formData.weight_kg} onChange={handleChange} />
        </div>
        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="activity_level">Activity Level</label>
            <select className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="activity_level" name="activity_level" value={formData.activity_level} onChange={handleChange}>
                <option value="">Select Activity Level</option>
                <option value="sedentary">Sedentary</option>
                <option value="light">Light</option>
                <option value="moderate">Moderate</option>
                <option value="very_active">Very Active</option>
                <option value="extra_active">Extra Active</option>
            </select>
        </div>
        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="goal">Goal</label>
            <select className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="goal" name="goal" value={formData.goal} onChange={handleChange}>
                <option value="">Select Goal</option>
                <option value="lose_weight">Lose Weight</option>
                <option value="maintain_weight">Maintain Weight</option>
                <option value="gain_weight">Gain Weight</option>
                <option value="build_muscle">Build Muscle</option>
                <option value="improve_endurance">Improve Endurance</option>
            </select>
        </div>
        <div className="flex justify-between">
            <button className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded" onClick={prevStep}>Back</button>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={nextStep}>Next</button>
        </div>
    </div>
);

const Step3 = ({ formData, handleChange, handleSubmit, prevStep }) => (
    <div>
        <h2 className="text-xl font-semibold mb-4">Step 3: Dietary Preferences</h2>
        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">Dietary Restrictions</label>
            <div>
                <label><input type="checkbox" name="vegetarian" checked={formData.dietary_restrictions.vegetarian} onChange={handleChange} /> Vegetarian</label>
                <label><input type="checkbox" name="vegan" checked={formData.dietary_restrictions.vegan} onChange={handleChange} /> Vegan</label>
                <label><input type="checkbox" name="gluten_free" checked={formData.dietary_restrictions.gluten_free} onChange={handleChange} /> Gluten-Free</label>
            </div>
        </div>
        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="allergies">Allergies (comma-separated)</label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="allergies" type="text" name="allergies" value={formData.allergies} onChange={handleChange} />
        </div>
        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="disliked_ingredients">Disliked Ingredients (comma-separated)</label>
            <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700" id="disliked_ingredients" type="text" name="disliked_ingredients" value={formData.disliked_ingredients} onChange={handleChange} />
        </div>
        <div className="flex justify-between">
            <button className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded" onClick={prevStep}>Back</button>
            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={handleSubmit}>Finish</button>
        </div>
    </div>
);