import { useState, useEffect } from 'react'
import { Thread } from '@/types'
import { api } from '@/lib/api'
import { MessageList } from './MessageList'
import { ChatInput } from './ChatInput'
import { ThreadSidebar } from './ThreadSidebar'
import { useChat } from '@/hooks/useChat'

export function ChatContainer() {
  const [threads, setThreads] = useState<Thread[]>([])
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null)
  const { messages, loading, streaming, sendMessage } = useChat(currentThreadId)

  useEffect(() => {
    loadThreads()
  }, [])

  const loadThreads = async () => {
    try {
      const data = await api.getThreads()
      setThreads(data)
      if (data.length > 0 && !currentThreadId) {
        setCurrentThreadId(data[0].id)
      }
    } catch (error) {
      console.error('Failed to load threads:', error)
    }
  }

  const handleNewThread = async () => {
    try {
      const newThread = await api.createThread()
      setThreads(prev => [newThread, ...prev])
      setCurrentThreadId(newThread.id)
    } catch (error) {
      console.error('Failed to create thread:', error)
    }
  }

  return (
    <div className="flex h-full">
      <ThreadSidebar
        threads={threads}
        currentThreadId={currentThreadId}
        onSelectThread={setCurrentThreadId}
        onNewThread={handleNewThread}
      />
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} loading={loading} />
        </div>
        <div className="border-t p-4">
          <ChatInput
            onSendMessage={sendMessage}
            disabled={!currentThreadId || streaming}
          />
        </div>
      </div>
    </div>
  )
}
