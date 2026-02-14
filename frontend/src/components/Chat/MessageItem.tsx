import type { Message } from '@/types'
import { Avatar } from '@/components/ui/avatar'
import { cn } from '@/lib/utils'

interface MessageItemProps {
  message: Message
}

export function MessageItem({ message }: MessageItemProps) {
  const isUser = message.role === 'user'

  return (
    <div className={cn('flex gap-3 mb-4', isUser ? 'flex-row-reverse' : 'flex-row')}>
      <Avatar className="h-8 w-8">
        <div className={cn(
          'h-full w-full flex items-center justify-center text-sm font-medium',
          isUser ? 'bg-blue-500 text-white' : 'bg-gray-500 text-white'
        )}>
          {isUser ? 'U' : 'A'}
        </div>
      </Avatar>
      <div className={cn('flex flex-col max-w-[70%]', isUser ? 'items-end' : 'items-start')}>
        <div className={cn(
          'rounded-lg px-4 py-2',
          isUser ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-900'
        )}>
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>
        <span className="text-xs text-gray-500 mt-1">
          {new Date(message.created_at).toLocaleTimeString()}
        </span>
      </div>
    </div>
  )
}
