import { cn } from '@/lib/utils'

type DocumentStatusType = 'uploaded' | 'processing' | 'completed' | 'failed'

interface DocumentStatusProps {
  status: DocumentStatusType
}

export function DocumentStatus({ status }: DocumentStatusProps) {
  const statusConfig = {
    uploaded: {
      label: 'Uploaded',
      color: 'bg-blue-100 text-blue-700',
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
      ),
    },
    processing: {
      label: 'Processing',
      color: 'bg-yellow-100 text-yellow-700',
      icon: (
        <svg
          className="w-4 h-4 animate-spin"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
          />
        </svg>
      ),
    },
    completed: {
      label: 'Completed',
      color: 'bg-green-100 text-green-700',
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M5 13l4 4L19 7"
          />
        </svg>
      ),
    },
    failed: {
      label: 'Failed',
      color: 'bg-red-100 text-red-700',
      icon: (
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      ),
    },
  }

  const config = statusConfig[status]

  return (
    <div
      className={cn(
        'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium',
        config.color
      )}
    >
      {config.icon}
      <span>{config.label}</span>
    </div>
  )
}

interface ProcessingStage {
  name: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
}

interface DocumentProcessingStagesProps {
  stages: ProcessingStage[]
}

export function DocumentProcessingStages({ stages }: DocumentProcessingStagesProps) {
  return (
    <div className="space-y-2">
      {stages.map((stage, index) => (
        <div key={index} className="flex items-center gap-3">
          <div className="flex-shrink-0">
            {stage.status === 'completed' && (
              <div className="w-5 h-5 rounded-full bg-green-500 flex items-center justify-center">
                <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            )}
            {stage.status === 'processing' && (
              <div className="w-5 h-5 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" />
            )}
            {stage.status === 'pending' && (
              <div className="w-5 h-5 rounded-full border-2 border-gray-300" />
            )}
            {stage.status === 'failed' && (
              <div className="w-5 h-5 rounded-full bg-red-500 flex items-center justify-center">
                <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
            )}
          </div>

          <div className="flex-1">
            <p
              className={cn(
                'text-sm font-medium',
                stage.status === 'completed' && 'text-green-700',
                stage.status === 'processing' && 'text-blue-700',
                stage.status === 'pending' && 'text-gray-500',
                stage.status === 'failed' && 'text-red-700'
              )}
            >
              {stage.name}
            </p>
          </div>
        </div>
      ))}
    </div>
  )
}

// Example usage with mock data
export function DocumentProcessingExample() {
  const mockStages: ProcessingStage[] = [
    { name: 'Upload to storage', status: 'completed' },
    { name: 'Extract text content', status: 'completed' },
    { name: 'Split into chunks', status: 'processing' },
    { name: 'Generate embeddings', status: 'pending' },
    { name: 'Store in database', status: 'pending' },
  ]

  return (
    <div className="p-4 border rounded-lg">
      <h3 className="font-medium text-sm mb-4">Processing Status</h3>
      <DocumentProcessingStages stages={mockStages} />
    </div>
  )
}
