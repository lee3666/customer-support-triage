// components/admin/SystemAnalytics.tsx
export default function SystemAnalytics() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">System Analytics</h1>
      
      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-6 mb-6">
        <h2 className="text-lg font-medium text-yellow-900 mb-2">Analytics Dashboard</h2>
        <p className="text-yellow-800">
          This feature is under development. System analytics will include:
        </p>
        <ul className="text-yellow-700 list-disc list-inside mt-2 space-y-1">
          <li>Ticket volume and trends</li>
          <li>Response time metrics</li>
          <li>Agent performance analytics</li>
          <li>Customer satisfaction scores</li>
          <li>System usage statistics</li>
        </ul>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-blue-600">1,247</div>
          <div className="text-gray-600">Total Tickets</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-green-600">89%</div>
          <div className="text-gray-600">Resolution Rate</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-purple-600">2.3h</div>
          <div className="text-gray-600">Avg. Response Time</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-orange-600">156</div>
          <div className="text-gray-600">Active Users</div>
        </div>
      </div>
    </div>
  )
}
