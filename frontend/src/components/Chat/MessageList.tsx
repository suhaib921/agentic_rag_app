import { Message } from '@/types'
import { MessageItem } from './MessageItem'
import { ScrollArea } from '@/components/ui/scroll-area'

interface MessageListProps {
  messages: Message[]
  loading: boolean
}

export function MessageList({ messages, loading }: MessageListProps) {
  if (loading) {
    return <div className="flex items-center justify-center h-full">Loading...</div>
  }

  return (
    <ScrollArea className="h-full p-4">
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} />
      ))}
    </ScrollArea>
  )
}
