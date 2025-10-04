// components/admin/AIConfiguration.tsx
import { useState } from 'react'

export default function AIConfiguration() {
  const [aiEnabled, setAiEnabled] = useState(true)
  const [autoCategorization, setAutoCategorization] = useState(true)
  const [sentimentAnalysis, setSentimentAnalysis] = useState(true)
  const [urgencyScoring, setUrgencyScoring] = useState(true)

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">AI Configuration</h1>
      
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">AI Features</h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium text-gray-900">AI-Powered Support</h3>
              <p className="text-gray-600 text-sm">Enable AI analysis for all incoming tickets</p>
            </div>
            <button
              onClick={() => setAiEnabled(!aiEnabled)}
              className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                aiEnabled ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                  aiEnabled ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium text-gray-900">Auto Categorization</h3>
              <p className="text-gray-600 text-sm">Automatically categorize tickets by type</p>
            </div>
            <button
              onClick={() => setAutoCategorization(!autoCategorization)}
              className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                autoCategorization ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                  autoCategorization ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium text-gray-900">Sentiment Analysis</h3>
              <p className="text-gray-600 text-sm">Analyze customer sentiment in tickets</p>
            </div>
            <button
              onClick={() => setSentimentAnalysis(!sentimentAnalysis)}
              className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                sentimentAnalysis ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                  sentimentAnalysis ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium text-gray-900">Urgency Scoring</h3>
              <p className="text-gray-600 text-sm">Automatically assign urgency scores to tickets</p>
            </div>
            <button
              onClick={() => setUrgencyScoring(!urgencyScoring)}
              className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                urgencyScoring ? 'bg-blue-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                  urgencyScoring ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        </div>
      </div>

      <div className="bg-green-50 border border-green-200 rounded-md p-4">
        <h3 className="text-lg font-medium text-green-900 mb-2">AI Configuration Status</h3>
        <p className="text-green-800">
          All AI features are currently active and processing incoming tickets automatically.
        </p>
      </div>
    </div>
  )
}
