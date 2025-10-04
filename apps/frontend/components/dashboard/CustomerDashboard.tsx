// components/dashboard/CustomerDashboard.tsx
'use client'
import toast from 'react-hot-toast';
import { useState, useEffect } from 'react'
import { useAuth } from '../../app/contexts/AuthContext'
import axios from 'axios'

interface Ticket {
  id: string
  customer_id: string
  subject: string
  description: string
  status: string
  urgency: number
  created_at: string
  ai_urgency?: number
  ai_sentiment?: string
  ai_category?: string
}

export default function CustomerDashboard() {
  const { user, logout } = useAuth()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('all')
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [newTicket, setNewTicket] = useState({ subject: '', description: '' })

  useEffect(() => {
    fetchMyTickets()
  }, [])

const fetchMyTickets = async () => {
  try {
    // Use the new dashboard endpoint instead of customer-specific endpoint
    const response = await axios.get('http://localhost:8001/api/dashboard/customer/tickets')
    setTickets(response.data)
  } catch (error) {
    console.error('Error fetching tickets:', error)
  } finally {
    setLoading(false)
  }
}

  const createTicket = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await axios.post('http://localhost:8001/api/tickets', {
        customer_id: user?.id,
        subject: newTicket.subject,
        description: newTicket.description
      })
      
      // ADD SUCCESS MESSAGE
      toast.success('🎉 Ticket created successfully! Confirmation email has been sent to you.', {
        duration: 5000,
      })
      
      setNewTicket({ subject: '', description: '' })
      setShowCreateForm(false)
      await fetchMyTickets()
    } catch (error) {
      console.error('Error creating ticket:', error)
      
      // ADD ERROR MESSAGE
      toast.error('Failed to create ticket. Please try again.')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-red-100 text-red-800'
      case 'in_progress': return 'bg-yellow-100 text-yellow-800'
      case 'resolved': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredTickets = tickets.filter(ticket => {
    if (activeTab === 'all') return true
    return ticket.status === activeTab
  })

  const stats = {
    total: tickets.length,
    open: tickets.filter(t => t.status === 'open').length,
    inProgress: tickets.filter(t => t.status === 'in_progress').length,
    resolved: tickets.filter(t => t.status === 'resolved').length
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Customer Dashboard</h1>
              <p className="text-gray-600">Welcome back, {user?.full_name}</p>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowCreateForm(true)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                New Ticket
              </button>
              <button
                onClick={logout}
                className="text-gray-500 hover:text-gray-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
            <div className="text-gray-600">Total Tickets</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-red-600">{stats.open}</div>
            <div className="text-gray-600">Open</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-yellow-600">{stats.inProgress}</div>
            <div className="text-gray-600">In Progress</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-2xl font-bold text-green-600">{stats.resolved}</div>
            <div className="text-gray-600">Resolved</div>
          </div>
        </div>

        {/* Create Ticket Modal */}
        {showCreateForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-lg font-semibold mb-4">Create New Support Ticket</h3>
              <form onSubmit={createTicket} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Subject</label>
                  <input
                    type="text"
                    value={newTicket.subject}
                    onChange={(e) => setNewTicket({...newTicket, subject: e.target.value})}
                    className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Description</label>
                  <textarea
                    value={newTicket.description}
                    onChange={(e) => setNewTicket({...newTicket, description: e.target.value})}
                    rows={4}
                    className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md"
                    required
                  />
                </div>
                <div className="flex space-x-3">
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
                  >
                    Create Ticket
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowCreateForm(false)}
                    className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Tickets Section */}
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              {['all', 'open', 'in_progress', 'resolved'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`py-4 px-6 text-sm font-medium border-b-2 ${
                    activeTab === tab
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab === 'all' ? 'All Tickets' : tab.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                </button>
              ))}
            </nav>
          </div>

          <div className="p-6">
            {loading ? (
              <div className="text-center py-8">Loading tickets...</div>
            ) : filteredTickets.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No tickets found. Create your first support ticket!
              </div>
            ) : (
              <div className="space-y-4">
                {filteredTickets.map((ticket) => (
                  <div key={ticket.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold text-lg">{ticket.subject}</h3>
                        <p className="text-gray-600 mt-1">{ticket.description}</p>
                      </div>
                      <div className="flex space-x-2">
                        <span className={`px-3 py-1 rounded-full text-sm ${getStatusColor(ticket.status)}`}>
                          {ticket.status.replace('_', ' ').toUpperCase()}
                        </span>
                        {ticket.ai_urgency && (
                          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                            AI Urgency: {ticket.ai_urgency}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="mt-2 text-sm text-gray-500">
                      Created: {new Date(ticket.created_at).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
