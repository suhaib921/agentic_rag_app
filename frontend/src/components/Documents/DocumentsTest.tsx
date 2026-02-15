import { DocumentUpload } from './DocumentUpload'
import { DocumentList } from './DocumentList'
import { DocumentStatus, DocumentProcessingStages } from './DocumentStatus'

/**
 * Test component to verify all document components render correctly
 * This is a temporary component for verification purposes
 */
export function DocumentsTest() {
  const mockStages = [
    { name: 'Upload to storage', status: 'completed' as const },
    { name: 'Extract text content', status: 'completed' as const },
    { name: 'Split into chunks', status: 'processing' as const },
    { name: 'Generate embeddings', status: 'pending' as const },
    { name: 'Store in database', status: 'pending' as const },
  ]

  return (
    <div className="p-8 space-y-8 bg-gray-50 min-h-screen">
      <div>
        <h1 className="text-2xl font-bold mb-4">Document Components Test</h1>
        <p className="text-gray-600 mb-8">
          All components use MOCK DATA. Real API integration will happen in Wave 4.
        </p>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">1. DocumentUpload Component</h2>
        <DocumentUpload onUploadComplete={() => console.log('Upload completed')} />
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">2. DocumentList Component</h2>
        <DocumentList />
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">3. DocumentStatus Component</h2>
        <div className="grid grid-cols-4 gap-4">
          <div className="p-4 border rounded bg-white">
            <p className="text-sm font-medium mb-2">Uploaded</p>
            <DocumentStatus status="uploaded" />
          </div>
          <div className="p-4 border rounded bg-white">
            <p className="text-sm font-medium mb-2">Processing</p>
            <DocumentStatus status="processing" />
          </div>
          <div className="p-4 border rounded bg-white">
            <p className="text-sm font-medium mb-2">Completed</p>
            <DocumentStatus status="completed" />
          </div>
          <div className="p-4 border rounded bg-white">
            <p className="text-sm font-medium mb-2">Failed</p>
            <DocumentStatus status="failed" />
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">4. DocumentProcessingStages Component</h2>
        <div className="p-6 border rounded bg-white max-w-md">
          <DocumentProcessingStages stages={mockStages} />
        </div>
      </div>
    </div>
  )
}
