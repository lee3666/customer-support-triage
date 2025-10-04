// app/support-triage/page.tsx
'use client'
import { useAuth } from '../contexts/AuthContext'
import CustomerDashboard from '../../components/dashboard/CustomerDashboard'
import SupportAgentDashboard from '../../components/dashboard/SupportAgentDashboard'
import AdminDashboard from '../../components/dashboard/AdminDashboard'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DashboardPage() {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user) return null

  // Render different dashboards based on role
  const renderDashboard = () => {
    switch (user.role) {
      case 'admin':
        return <AdminDashboard />
      case 'support_agent':
        return <SupportAgentDashboard />
      case 'customer':
      default:
        return <CustomerDashboard />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {renderDashboard()}
    </div>
  )
}
