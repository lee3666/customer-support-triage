// app/page.tsx - New landing page
'use client'
import { useAuth } from './contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import Link from 'next/link'

export default function HomePage() {
  const { user } = useAuth()
  const router = useRouter()

  // If user is logged in, redirect to support triage
  useEffect(() => {
    if (user) {
      router.push('/support-triage')
    }
  }, [user, router])

  if (user) {
    return null // Will redirect
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Customer Support System
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          AI-powered customer support management
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10 text-center">
          <div className="space-y-4">
            <Link 
              href="/register"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
            >
              Get Started
            </Link>
            <Link 
              href="/login"
              className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}