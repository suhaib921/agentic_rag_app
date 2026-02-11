import { supabase } from './supabase'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function getAuthHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.access_token) throw new Error('No auth token')
  return {
    'Authorization': `Bearer ${session.access_token}`,
    'Content-Type': 'application/json',
  }
}

export const api = {
  async createThread() {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/chat/threads`, {
      method: 'POST',
      headers,
    })
    if (!res.ok) throw new Error('Failed to create thread')
    return res.json()
  },

  async getThreads() {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/chat/threads`, { method: 'GET', headers })
    if (!res.ok) throw new Error('Failed to fetch threads')
    return res.json()
  },

  async getMessages(threadId: string) {
    const headers = await getAuthHeaders()
    const res = await fetch(`${API_BASE}/api/chat/threads/${threadId}/messages`, {
      method: 'GET',
      headers,
    })
    if (!res.ok) throw new Error('Failed to fetch messages')
    return res.json()
  },

  async sendMessage(threadId: string, content: string, onChunk: (chunk: string) => void) {
    const headers = await getAuthHeaders()
    const url = new URL(`${API_BASE}/api/chat/threads/${threadId}/messages/stream`)
    url.searchParams.append('content', content)

    const res = await fetch(url.toString(), {
      method: 'POST',
      headers,
    })

    if (!res.ok) throw new Error('Failed to send message')

    const reader = res.body?.getReader()
    if (!reader) throw new Error('No response body')

    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6))
          if (data.content) {
            onChunk(data.content)
          }
          if (data.done) {
            return
          }
        }
      }
    }
  },
}
