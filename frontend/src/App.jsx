import { useMemo, useRef, useState } from 'react'
import ChatMessage from './components/ChatMessage'
import CitationList from './components/CitationList'
import { openStream } from './lib/api'

function App() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Hi, I am Project Nexus. Ask something from the uploaded PDFs.',
    },
  ])
  const [citations, setCitations] = useState([])
  const [workflowSteps, setWorkflowSteps] = useState([])
  const [loading, setLoading] = useState(false)
  const streamRef = useRef(null)

  const canSend = useMemo(() => question.trim().length > 0 && !loading, [question, loading])

  function handleAsk(event) {
    event.preventDefault()

    if (!canSend) {
      return
    }

    const userQuestion = question.trim()
    setQuestion('')
    setCitations([])
    setWorkflowSteps([])
    setLoading(true)

    setMessages((prev) => [
      ...prev,
      { role: 'user', text: userQuestion },
      { role: 'assistant', text: '' },
    ])

    if (streamRef.current) {
      streamRef.current.close()
    }

    streamRef.current = openStream(userQuestion, {
      onWorkflow: (data) => {
        setWorkflowSteps((prev) => [...prev, data.name])
      },
      onToken: (data) => {
        setMessages((prev) => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            role: 'assistant',
            text: data.text,
          }
          return updated
        })
      },
      onCitations: (data) => {
        setCitations(data)
      },
      onDone: () => {
        setLoading(false)
      },
      onError: (message) => {
        setLoading(false)
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', text: message },
        ])
      },
    })
  }

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-8">
      <div className="mx-auto grid max-w-6xl gap-6 lg:grid-cols-[1fr_320px]">
        <div className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <div className="border-b border-gray-200 pb-4">
            <h1 className="m-0 text-2xl font-semibold text-gray-900">Project Nexus</h1>
            <p className="mt-2 text-sm text-gray-600">
              Simple React + Tailwind chat for the Limi AI technical assessment.
            </p>
          </div>

          <div className="mt-5 h-[500px] space-y-4 overflow-y-auto rounded-xl bg-gray-50 p-4">
            {messages.map((message, index) => (
              <ChatMessage key={index} role={message.role} text={message.text} />
            ))}
          </div>

          <form onSubmit={handleAsk} className="mt-4 flex flex-col gap-3 sm:flex-row">
            <input
              type="text"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask a question..."
              className="h-12 flex-1 rounded-xl border border-gray-300 px-4 text-sm outline-none focus:border-blue-500"
            />

            <button
              type="submit"
              disabled={!canSend}
              className="h-12 rounded-xl bg-blue-600 px-5 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-blue-300"
            >
              {loading ? 'Thinking...' : 'Send'}
            </button>
          </form>
        </div>

        <div className="space-y-4">
          <div className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
            <h2 className="m-0 text-sm font-semibold text-gray-900">Workflow</h2>
            <div className="mt-3 space-y-2 text-sm text-gray-600">
              {workflowSteps.length === 0 && <div>No events yet</div>}
              {workflowSteps.map((step, index) => (
                <div key={index} className="rounded-lg bg-gray-50 px-3 py-2">
                  {step}
                </div>
              ))}
            </div>
          </div>

          <CitationList citations={citations} />
        </div>
      </div>
    </div>
  )
}

export default App
