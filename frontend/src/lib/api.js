const API_BASE = 'http://127.0.0.1:8000'

export async function sendQuestion(question) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  })

  if (!response.ok) {
    const data = await response.json()
    throw new Error(data.detail || 'Something went wrong')
  }

  return response.json()
}

export function openStream(question, handlers) {
  const url = `${API_BASE}/chat/stream?question=${encodeURIComponent(question)}`
  const eventSource = new EventSource(url)

  eventSource.addEventListener('workflow', (event) => {
    handlers.onWorkflow?.(JSON.parse(event.data))
  })

  eventSource.addEventListener('token', (event) => {
    handlers.onToken?.(JSON.parse(event.data))
  })

  eventSource.addEventListener('citations', (event) => {
    handlers.onCitations?.(JSON.parse(event.data))
  })

  eventSource.addEventListener('done', () => {
    handlers.onDone?.()
    eventSource.close()
  })

  eventSource.onerror = () => {
    handlers.onError?.('Stream stopped unexpectedly.')
    eventSource.close()
  }

  return eventSource
}
