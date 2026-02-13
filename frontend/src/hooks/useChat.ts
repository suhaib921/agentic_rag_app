import { useState, useEffect } from 'react'
import type { Message } from '@/types'
import { api } from '@/lib/api'

export function useChat(threadId: string | null) {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [streaming, setStreaming] = useState(false)

  useEffect(() => {
    if (!threadId) return

    const loadMessages = async () => {
      setLoading(true)
      try {
        const data = await api.getMessages(threadId)
        setMessages(data)
      } catch (error) {
        console.error('Failed to load messages:', error)
      } finally {
        setLoading(false)
      }
    }

    loadMessages()
  }, [threadId])

  const sendMessage = async (content: string) => {
    if (!threadId || !content.trim()) return

    // Add user message optimistically
    const userMessage: Message = {
      id: crypto.randomUUID(),
      thread_id: threadId,
      user_id: '',
      role: 'user',
      content,
      openai_message_id: null,
      created_at: new Date().toISOString(),
    }
    setMessages(prev => [...prev, userMessage])

    // Add empty assistant message for streaming
    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      thread_id: threadId,
      user_id: '',
      role: 'assistant',
      content: '',
      openai_message_id: null,
      created_at: new Date().toISOString(),
    }
    setMessages(prev => [...prev, assistantMessage])

    setStreaming(true)
    let assistantContent = ''

    try {
      await api.sendMessage(threadId, content, (chunk) => {
        assistantContent += chunk
        setMessages(prev => {
          const updated = [...prev]
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: assistantContent,
          }
          return updated
        })
      })
    } catch (error) {
      console.error('Failed to send message:', error)
    } finally {
      setStreaming(false)
    }
  }

  return { messages, loading, streaming, sendMessage }
}
