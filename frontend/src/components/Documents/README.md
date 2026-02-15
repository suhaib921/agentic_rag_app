# Document Management Components

Created for **Wave 2, Track 3** of Module 2 implementation.

## Overview

This directory contains frontend components for document management with **MOCK DATA**. Real API integration will be implemented in Wave 4, Track 1.

## Components

### 1. DocumentUpload.tsx

Upload component with drag-and-drop support.

**Features:**
- File input with accept filter (.pdf, .txt, .md, .docx)
- Drag and drop support
- Visual feedback during upload
- Upload progress indication

**Mock Behavior:**
- Simulates 1.5s upload delay
- Logs uploaded filename to console
- Calls `onUploadComplete` callback after mock upload

**TODO for Wave 4:**
- Replace mock upload with real API call to `POST /documents`
- Add Supabase auth token to request headers
- Handle actual FormData submission
- Add error handling and user feedback

**Props:**
```typescript
interface DocumentUploadProps {
  onUploadComplete?: () => void
}
```

### 2. DocumentList.tsx

Displays list of user's documents with status.

**Features:**
- Document cards with filename, size, and upload date
- Status badges (uploaded, processing, completed, failed)
- Chunk count for completed documents
- Error messages for failed uploads
- Empty state when no documents
- Loading state

**Mock Data:**
4 sample documents with different statuses:
- introduction-to-react.pdf (completed, 45 chunks)
- python-best-practices.md (processing)
- typescript-handbook.pdf (completed, 67 chunks)
- fastapi-tutorial.txt (failed with error)

**TODO for Wave 4:**
- Replace mock data with real API call to `GET /documents`
- Add Supabase Realtime subscription for status updates
- Implement real-time chunk count updates
- Add document actions (delete, retry, etc.)

**Props:**
```typescript
interface DocumentListProps {
  refreshTrigger?: number  // Increment to trigger refresh
}
```

**Document Type:**
```typescript
interface Document {
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
```

### 3. DocumentStatus.tsx

Status badges and processing stage indicators.

**Components:**

#### DocumentStatus
Simple status badge with icon and label.

**Props:**
```typescript
interface DocumentStatusProps {
  status: 'uploaded' | 'processing' | 'completed' | 'failed'
}
```

**Visual Design:**
- Uploaded: Blue badge with upload icon
- Processing: Yellow badge with spinning refresh icon
- Completed: Green badge with checkmark
- Failed: Red badge with X icon

#### DocumentProcessingStages
Step-by-step processing progress indicator.

**Props:**
```typescript
interface ProcessingStage {
  name: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
}

interface DocumentProcessingStagesProps {
  stages: ProcessingStage[]
}
```

**Example Usage:**
```typescript
const stages = [
  { name: 'Upload to storage', status: 'completed' },
  { name: 'Extract text content', status: 'completed' },
  { name: 'Split into chunks', status: 'processing' },
  { name: 'Generate embeddings', status: 'pending' },
  { name: 'Store in database', status: 'pending' },
]
```

#### DocumentProcessingExample
Pre-configured example component with mock stages.

## Styling

All components use:
- **Tailwind CSS** for styling
- **shadcn/ui** components (Card, Button)
- Consistent color scheme matching existing chat UI
- Responsive design
- Hover states and transitions

## Testing

To verify components:

1. Import DocumentsTest component
2. Render in your app
3. Check that all components display correctly
4. Verify TypeScript compilation with no errors

```typescript
import { DocumentsTest } from '@/components/Documents/DocumentsTest'

function App() {
  return <DocumentsTest />
}
```

Or use individual components:

```typescript
import { DocumentUpload, DocumentList } from '@/components/Documents'

function DocumentsPage() {
  const [refresh, setRefresh] = useState(0)

  return (
    <div className="space-y-6 p-8">
      <DocumentUpload onUploadComplete={() => setRefresh(r => r + 1)} />
      <DocumentList refreshTrigger={refresh} />
    </div>
  )
}
```

## Integration Roadmap

**Wave 3: Backend API (Track 1)**
- Implement `POST /documents` endpoint
- Implement `GET /documents` endpoint
- Set up Supabase Storage
- Configure RLS policies

**Wave 4: Frontend Integration (Track 1)**
- Replace mock upload with real API call
- Replace mock data fetch with real API call
- Add Supabase Realtime subscription
- Wire up processing status updates
- Add error handling
- Add success notifications

## Files

```
Documents/
├── DocumentUpload.tsx       # Upload component with drag-drop
├── DocumentList.tsx         # List of documents with status
├── DocumentStatus.tsx       # Status badges and stage indicators
├── DocumentsTest.tsx        # Test/demo component
├── index.ts                 # Barrel exports
└── README.md               # This file
```

## Verification Checklist

- [x] Components render without errors
- [x] Upload component shows file input
- [x] Upload component supports drag-drop
- [x] Document list displays mock documents
- [x] Status badges show all 4 states correctly
- [x] Processing stages component works
- [x] All TypeScript types are correct
- [x] Components follow existing UI patterns
- [x] Tailwind styling applied consistently
- [x] shadcn/ui components used appropriately
- [x] TODO comments indicate API integration points
- [x] No compilation errors
