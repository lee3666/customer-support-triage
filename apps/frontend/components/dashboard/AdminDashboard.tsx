// components/dashboard/AdminDashboard.tsx - UPDATED VERSION
'use client'
import { useState } from 'react'
import { useAuth } from '../../app/contexts/AuthContext'
import UserManagement from '../admin/UserManagement'
import SystemAnalytics from '../admin/SystemAnalytics'
import AIConfiguration from '../admin/AIConfiguration'

type AdminView = 'dashboard' | 'users' | 'analytics' | 'ai'

export default function AdminDashboard() {
  const { user, logout } = useAuth()
  const [currentView, setCurrentView] = useState<AdminView>('dashboard')

  const renderContent = () => {
    switch (currentView) {
      case 'users':
        return <UserManagement />
      case 'analytics':
        return <SystemAnalytics />
      case 'ai':
        return <AIConfiguration />
      case 'dashboard':
      default:
        return (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div 
                className="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => setCurrentView('users')}
              >
                <div className="text-2xl font-bold text-gray-900">User Management</div>
                <div className="text-gray-600 mt-2">Manage users and permissions</div>
                <div className="mt-4 text-blue-600 font-medium">Click to manage </div>
              </div>
              <div 
                className="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => setCurrentView('analytics')}
              >
                <div className="text-2xl font-bold text-gray-900">System Analytics</div>
                <div className="text-gray-600 mt-2">View system performance and metrics</div>
                <div className="mt-4 text-blue-600 font-medium">Click to view </div>
              </div>
              <div 
                className="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => setCurrentView('ai')}
              >
                <div className="text-2xl font-bold text-gray-900">AI Configuration</div>
                <div className="text-gray-600 mt-2">Configure AI analysis settings</div>
                <div className="mt-4 text-blue-600 font-medium">Click to configure </div>
              </div>
            </div>
          </div>
        )
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
              {currentView !== 'dashboard' && (
                <button
                  onClick={() => setCurrentView('dashboard')}
                  className="text-blue-600 hover:text-blue-800 font-medium"
                >
                   Back to Dashboard
                </button>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user?.full_name}</span>
              <button
                onClick={logout}
                className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {renderContent()}
    </div>
  )
}
