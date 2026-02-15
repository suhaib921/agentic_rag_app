import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { cn } from '@/lib/utils'
import { supabase } from '@/lib/supabase'

interface DocumentUploadProps {
  onUploadComplete?: () => void
}

export function DocumentUpload({ onUploadComplete }: DocumentUploadProps) {
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleUpload = async (file: File) => {
    if (!file) return

    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)

      const token = (await supabase.auth.getSession()).data.session?.access_token
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

      const response = await fetch(`${apiUrl}/api/documents`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }))
        throw new Error(errorData.detail || 'Upload failed')
      }

      const result = await response.json()
      console.log('Uploaded:', result)

      onUploadComplete?.()
    } catch (error) {
      console.error('Upload error:', error)
      alert(error instanceof Error ? error.message : 'Upload failed')
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleUpload(file)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleUpload(e.dataTransfer.files[0])
    }
  }

  const handleButtonClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Upload Document</CardTitle>
        <CardDescription>
          Upload PDF, TXT, MD, or DOCX files to add to your knowledge base
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div
          className={cn(
            'border-2 border-dashed rounded-lg p-8 text-center transition-colors',
            dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300',
            uploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'
          )}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={handleButtonClick}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.txt,.md,.docx"
            onChange={handleFileChange}
            disabled={uploading}
            className="hidden"
          />

          <div className="flex flex-col items-center gap-2">
            <svg
              className="w-12 h-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>

            {uploading ? (
              <p className="text-sm text-gray-600">Uploading...</p>
            ) : (
              <>
                <p className="text-sm font-medium text-gray-700">
                  Drop file here or click to browse
                </p>
                <p className="text-xs text-gray-500">
                  Supports: PDF, TXT, MD, DOCX
                </p>
              </>
            )}
          </div>
        </div>

        {!uploading && (
          <div className="mt-4">
            <Button onClick={handleButtonClick} className="w-full">
              Select File
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
