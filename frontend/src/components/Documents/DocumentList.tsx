import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { DocumentStatus } from './DocumentStatus'
import { cn } from '@/lib/utils'
import { supabase } from '@/lib/supabase'
import type { RealtimeChannel } from '@supabase/supabase-js'

export interface Document {
  id: string
  user_id: string
  filename: string
  file_size: number
  file_type: string
  storage_path: string
  status: 'uploaded' | 'processing' | 'completed' | 'failed'
  chunk_count: number
  error_message: string | null
  created_at: string
  updated_at: string
}

interface DocumentListProps {
  refreshTrigger?: number
}

export function DocumentList({ refreshTrigger }: DocumentListProps) {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDocuments()
    const channel = subscribeToUpdates()

    return () => {
      if (channel) {
        channel.unsubscribe()
      }
    }
  }, [refreshTrigger])

  const fetchDocuments = async () => {
    setLoading(true)
    try {
      const token = (await supabase.auth.getSession()).data.session?.access_token
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

      const response = await fetch(`${apiUrl}/api/documents`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch documents')
      }

      const data = await response.json()
      setDocuments(data)
    } catch (error) {
      console.error('Failed to fetch documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const subscribeToUpdates = (): RealtimeChannel | null => {
    try {
      const channel = supabase
        .channel('document_updates')
        .on('postgres_changes', {
          event: 'UPDATE',
          schema: 'public',
          table: 'documents'
        }, (payload) => {
          console.log('Document updated:', payload.new)
          setDocuments(prev =>
            prev.map(doc =>
              doc.id === payload.new.id ? payload.new as Document : doc
            )
          )
        })
        .on('postgres_changes', {
          event: 'INSERT',
          schema: 'public',
          table: 'documents'
        }, (payload) => {
          console.log('Document inserted:', payload.new)
          setDocuments(prev => [payload.new as Document, ...prev])
        })
        .subscribe()

      return channel
    } catch (error) {
      console.error('Failed to subscribe to updates:', error)
      return null
    }
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60))

    if (diffHours < 24) {
      if (diffHours < 1) return 'Just now'
      return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
    }

    const diffDays = Math.floor(diffHours / 24)
    if (diffDays < 7) {
      return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`
    }

    return date.toLocaleDateString()
  }

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Documents</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <p className="text-sm text-gray-500">Loading documents...</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (documents.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Your Documents</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <svg
              className="w-12 h-12 text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <p className="text-sm font-medium text-gray-700">No documents yet</p>
            <p className="text-xs text-gray-500 mt-1">Upload your first document to get started</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Documents ({documents.length})</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className={cn(
                'border rounded-lg p-4 transition-colors',
                'hover:bg-gray-50'
              )}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-2">
                    <svg
                      className="w-5 h-5 text-gray-400 flex-shrink-0"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    <h3 className="font-medium text-sm text-gray-900 truncate">
                      {doc.filename}
                    </h3>
                  </div>

                  <div className="flex flex-wrap items-center gap-3 text-xs text-gray-500">
                    <span>{formatFileSize(doc.file_size)}</span>
                    <span>•</span>
                    <span>{formatDate(doc.created_at)}</span>
                    {doc.status === 'completed' && (
                      <>
                        <span>•</span>
                        <span>{doc.chunk_count} chunks</span>
                      </>
                    )}
                  </div>

                  {doc.error_message && (
                    <p className="text-xs text-red-600 mt-2">
                      Error: {doc.error_message}
                    </p>
                  )}
                </div>

                <div className="flex-shrink-0">
                  <DocumentStatus status={doc.status} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
