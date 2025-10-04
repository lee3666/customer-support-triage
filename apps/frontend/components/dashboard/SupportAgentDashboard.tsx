// components/dashboard/SupportAgentDashboard.tsx
'use client'
import toast from 'react-hot-toast';
import { useState, useEffect } from 'react'
import { useAuth } from '../../app/contexts/AuthContext'
import axios from 'axios'

interface Ticket {
  id: string
  customer_id: string
  assigned_agent_id: string | null
  subject: string
  description: string
  status: string
  urgency: number
  created_at: string
  updated_at: string
  assigned_at: string | null
  resolved_at: string | null
  closed_at: string | null
  ai_urgency?: number
  ai_sentiment?: string
  ai_category?: string
}

export default function SupportAgentDashboard() {
  const { user, logout } = useAuth()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalTickets: 0,
    assignedTickets: 0,
    unassignedTickets: 0,
    resolvedToday: 0,
    avgResponseTime: 0,
    highUrgencyTickets: 0,
    openTickets: 0,
    myAssignedTickets: 0,
    inProgressTickets: 0,
    resolvedTickets: 0,
    closedTickets: 0
  })
  const [activeTab, setActiveTab] = useState('all')

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [ticketsRes, statsRes] = await Promise.all([
        axios.get('http://localhost:8001/api/dashboard/support-agent/tickets'),
        axios.get('http://localhost:8001/api/dashboard/support-agent/stats')
      ])
      
      setTickets(ticketsRes.data)
      setStats(statsRes.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const assignTicket = async (ticketId: string) => {
    try {
      await axios.post(`http://localhost:8001/api/tickets/${ticketId}/assign`)
      
      // SUCCESS MESSAGE
      toast.success('✅ Ticket assigned successfully! Customer has been notified via email.', {
        duration: 4000,
      })
      
      await fetchDashboardData()
    } catch (error) {
      console.error('Error assigning ticket:', error)
      
      // ERROR MESSAGE
      toast.error('Failed to assign ticket. Please try again.')
    }
  }

  const unassignTicket = async (ticketId: string) => {
    try {
      await axios.post(`http://localhost:8001/api/tickets/${ticketId}/unassign`)
      
      // SUCCESS MESSAGE
      toast.success('🔄 Ticket unassigned successfully.', {
        duration: 4000,
      })
      
      await fetchDashboardData()
    } catch (error) {
      console.error('Error unassigning ticket:', error)
      
      // ERROR MESSAGE
      toast.error('Failed to unassign ticket. Please try again.')
    }
  }

  const updateTicketStatus = async (ticketId: string, newStatus: string) => {
    try {
      await axios.post(`http://localhost:8001/api/tickets/${ticketId}/status?status=${newStatus}`)
      
      // Status-specific success messages
      const statusMessages = {
        'in_progress': '🔄 Status updated to In Progress. Customer has been notified.',
        'resolved': '✅ Ticket resolved successfully! Customer notified of resolution.',
        'closed': '🔒 Ticket closed. Customer has been notified.',
        'assigned': '👤 Ticket assigned. Customer notified.',
        'open': '📝 Ticket reopened. Customer has been notified.'
      }
      
      const message = statusMessages[newStatus] || 'Status updated successfully.'
      toast.success(message, {
        duration: 4000,
      })
      
      await fetchDashboardData()
    } catch (error) {
      console.error('Error updating ticket status:', error)
      
      // ERROR MESSAGE
      toast.error('Failed to update ticket status. Please try again.')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return 'bg-red-100 text-red-800 border-red-200'
      case 'assigned': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'in_progress': return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'resolved': return 'bg-green-100 text-green-800 border-green-200'
      case 'closed': return 'bg-gray-100 text-gray-800 border-gray-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getUrgencyColor = (urgency: number) => {
    switch (urgency) {
      case 1: return 'bg-green-100 text-green-800 border-green-200'
      case 2: return 'bg-blue-100 text-blue-800 border-blue-200'
      case 3: return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 4: return 'bg-orange-100 text-orange-800 border-orange-200'
      case 5: return 'bg-red-100 text-red-800 border-red-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getNextStatusOptions = (currentStatus: string, isAssignedToMe: boolean) => {
    if (!isAssignedToMe) return []
    
    switch (currentStatus) {
      case 'open':
        return [{ value: 'in_progress', label: 'Start Work', color: 'blue' }]
      case 'assigned':
        return [{ value: 'in_progress', label: 'Start Work', color: 'blue' }]
      case 'in_progress':
        return [
          { value: 'resolved', label: 'Mark Resolved', color: 'green' },
          { value: 'open', label: 'Re-open', color: 'red' }
        ]
      case 'resolved':
        return [
          { value: 'closed', label: 'Close Ticket', color: 'gray' },
          { value: 'in_progress', label: 'Re-open', color: 'blue' }
        ]
      case 'closed':
        return [{ value: 'open', label: 'Re-open', color: 'red' }]
      default:
        return []
    }
  }

  const filteredTickets = tickets.filter(ticket => {
    if (activeTab === 'all') return true
    if (activeTab === 'unassigned') return !ticket.assigned_agent_id
    if (activeTab === 'assigned') return ticket.assigned_agent_id === user?.id
    if (activeTab === 'in_progress') return ticket.status === 'in_progress'
    if (activeTab === 'resolved') return ticket.status === 'resolved'
    if (activeTab === 'closed') return ticket.status === 'closed'
    return ticket.status === activeTab
  })

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Support Agent Dashboard</h1>
              <p className="text-gray-600">Welcome, {user?.full_name}</p>
            </div>
            <button
              onClick={logout}
              className="text-gray-500 hover:text-gray-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Enhanced Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-xl font-bold text-gray-900">{stats.totalTickets}</div>
            <div className="text-gray-600 text-sm">Total</div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-xl font-bold text-blue-600">{stats.unassignedTickets}</div>
            <div className="text-gray-600 text-sm">Unassigned</div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-xl font-bold text-yellow-600">{stats.myAssignedTickets}</div>
            <div className="text-gray-600 text-sm">My Tickets</div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-xl font-bold text-purple-600">{stats.inProgressTickets}</div>
            <div className="text-gray-600 text-sm">In Progress</div>
          </div>
          <div className="bg-white rounded-lg shadow p-4">
            <div className="text-xl font-bold text-green-600">{stats.resolvedTickets}</div>
            <div className="text-gray-600 text-sm">Resolved</div>
          </div>
        </div>

        {/* Tickets Section */}
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px overflow-x-auto">
              {['all', 'unassigned', 'assigned', 'in_progress', 'resolved', 'closed'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`flex-shrink-0 py-4 px-4 text-sm font-medium border-b-2 whitespace-nowrap ${
                    activeTab === tab
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  }`}
                >
                  {tab === 'all' ? 'All Tickets' : 
                   tab === 'assigned' ? 'My Assigned' :
                   tab === 'in_progress' ? 'In Progress' :
                   tab.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </button>
              ))}
            </nav>
          </div>

          <div className="p-6">
            {loading ? (
              <div className="text-center py-8">Loading tickets...</div>
            ) : filteredTickets.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No tickets found in this category.
              </div>
            ) : (
              <div className="space-y-6">
                {filteredTickets.map((ticket) => {
                  const isAssignedToMe = ticket.assigned_agent_id === user?.id
                  const nextStatusOptions = getNextStatusOptions(ticket.status, isAssignedToMe)
                  
                  return (
                    <div key={ticket.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start mb-4">
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg text-gray-900">{ticket.subject}</h3>
                          <p className="text-gray-600 mt-2">{ticket.description}</p>
                          
                          {/* Customer and Assignment Info */}
                          <div className="mt-3 flex flex-wrap gap-4 text-sm text-gray-500">
                            <span>Customer: {ticket.customer_id.substring(0, 8)}...</span>
                            {ticket.assigned_agent_id && (
                              <span className={isAssignedToMe ? "text-blue-600 font-medium" : ""}>
                                {isAssignedToMe ? "Assigned to you" : "Assigned to another agent"}
                              </span>
                            )}
                          </div>
                        </div>
                        
                        <div className="flex flex-col items-end space-y-2">
                          <span className={`px-3 py-1 rounded-full text-sm border ${getUrgencyColor(ticket.urgency)}`}>
                            Urgency {ticket.urgency}
                          </span>
                          <span className={`px-3 py-1 rounded-full text-sm border ${getStatusColor(ticket.status)}`}>
                            {ticket.status.replace('_', ' ').toUpperCase()}
                          </span>
                        </div>
                      </div>

                      {/* AI Insights */}
                      {ticket.ai_urgency && (
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                          <h4 className="text-sm font-medium text-blue-800 mb-2">AI Analysis</h4>
                          <div className="flex flex-wrap gap-4 text-sm">
                            <div className="flex items-center space-x-1">
                              <span className="text-blue-700">AI Urgency:</span>
                              <span className={`px-2 py-1 rounded text-xs border ${getUrgencyColor(ticket.ai_urgency)}`}>
                                {ticket.ai_urgency}
                              </span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <span className="text-blue-700">Sentiment:</span>
                              <span className="font-medium text-blue-900">{ticket.ai_sentiment}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <span className="text-blue-700">Category:</span>
                              <span className="font-medium text-blue-900">{ticket.ai_category}</span>
                            </div>
                          </div>
                        </div>
                      )}

                      <div className="flex justify-between items-center pt-4 border-t border-gray-100">
                        <div className="text-sm text-gray-500 space-y-1">
                          <div>Created: {new Date(ticket.created_at).toLocaleString()}</div>
                          {ticket.assigned_at && (
                            <div>Assigned: {new Date(ticket.assigned_at).toLocaleString()}</div>
                          )}
                          {ticket.resolved_at && (
                            <div className="text-green-600">Resolved: {new Date(ticket.resolved_at).toLocaleString()}</div>
                          )}
                          {ticket.closed_at && (
                            <div className="text-gray-600">Closed: {new Date(ticket.closed_at).toLocaleString()}</div>
                          )}
                        </div>
                        
                        <div className="flex space-x-2">
                          {/* Assignment Controls */}
                          {!ticket.assigned_agent_id ? (
                            <button
                              onClick={() => assignTicket(ticket.id)}
                              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 text-sm"
                            >
                              Assign to Me
                            </button>
                          ) : isAssignedToMe ? (
                            <button
                              onClick={() => unassignTicket(ticket.id)}
                              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 text-sm"
                            >
                              Unassign
                            </button>
                          ) : (
                            <span className="text-gray-500 text-sm py-2">Assigned to another agent</span>
                          )}

                          {/* Status Update Controls */}
                          {nextStatusOptions.map((option) => (
                            <button
                              key={option.value}
                              onClick={() => updateTicketStatus(ticket.id, option.value)}
                              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                                option.color === 'blue' ? 'bg-blue-600 hover:bg-blue-700' :
                                option.color === 'green' ? 'bg-green-600 hover:bg-green-700' :
                                option.color === 'red' ? 'bg-red-600 hover:bg-red-700' :
                                'bg-gray-600 hover:bg-gray-700'
                              } text-white`}
                            >
                              {option.label}
                            </button>
                          ))}
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
