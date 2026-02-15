import { useState } from 'react'
import { DocumentUpload, DocumentList } from '@/components/Documents'

export function DocumentsDemo() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleUploadComplete = () => {
    // Trigger a refresh of the document list
    setRefreshTrigger((prev) => prev + 1)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Document Management</h1>
          <p className="text-gray-600">Upload and manage your knowledge base documents</p>
        </div>

        <DocumentUpload onUploadComplete={handleUploadComplete} />

        <DocumentList refreshTrigger={refreshTrigger} />
      </div>
    </div>
  )
}
