import type { Thread } from '@/types'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { cn } from '@/lib/utils'

interface ThreadSidebarProps {
  threads: Thread[]
  currentThreadId: string | null
  onSelectThread: (threadId: string) => void
  onNewThread: () => void
}

export function ThreadSidebar({ threads, currentThreadId, onSelectThread, onNewThread }: ThreadSidebarProps) {
  return (
    <div className="w-64 border-r flex flex-col">
      <div className="p-4">
        <Button onClick={onNewThread} className="w-full">
          New Chat
        </Button>
      </div>
      <Separator />
      <ScrollArea className="flex-1">
        <div className="p-2">
          {threads.map((thread) => (
            <button
              key={thread.id}
              onClick={() => onSelectThread(thread.id)}
              className={cn(
                'w-full text-left p-3 rounded-lg mb-1 hover:bg-gray-100 transition-colors',
                currentThreadId === thread.id && 'bg-gray-200'
              )}
            >
              <p className="font-medium truncate">{thread.title || 'Untitled'}</p>
              <p className="text-xs text-gray-500">
                {new Date(thread.updated_at).toLocaleDateString()}
              </p>
            </button>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}
