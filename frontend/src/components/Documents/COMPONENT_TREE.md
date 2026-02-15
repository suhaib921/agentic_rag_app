# Document Components Architecture

## Component Hierarchy

```
DocumentsPage (or DocumentsDemo)
├── DocumentUpload
│   ├── Card (shadcn/ui)
│   │   ├── CardHeader
│   │   ├── CardTitle
│   │   ├── CardDescription
│   │   └── CardContent
│   │       ├── File Input (hidden)
│   │       ├── Drag-Drop Area
│   │       └── Button (shadcn/ui)
│   └── State: uploading, dragActive
│
└── DocumentList
    ├── Card (shadcn/ui)
    │   ├── CardHeader
    │   │   └── CardTitle
    │   └── CardContent
    │       ├── Loading State
    │       ├── Empty State
    │       └── Document Cards (map)
    │           ├── File Icon
    │           ├── Filename
    │           ├── Metadata (size, date, chunks)
    │           ├── Error Message (if failed)
    │           └── DocumentStatus
    │               └── Status Badge
    └── State: documents[], loading
```

## Component Details

### DocumentUpload
```
Props: { onUploadComplete?: () => void }
State: { uploading: boolean, dragActive: boolean }

Features:
- Drag and drop file upload
- Click to browse files
- Accept: .pdf, .txt, .md, .docx
- Visual feedback during upload
- Disabled state when uploading

Mock Behavior:
- Simulates 1.5s upload delay
- Console logs filename
- Calls callback on completion
```

### DocumentList
```
Props: { refreshTrigger?: number }
State: { documents: Document[], loading: boolean }

Features:
- Display list of documents
- Show status badges
- Format file sizes (bytes → KB/MB)
- Format dates (relative time)
- Empty state (no documents)
- Loading state

Mock Data:
- 4 sample documents
- Different statuses (completed, processing, failed)
- Realistic metadata
```

### DocumentStatus
```
Props: { status: 'uploaded' | 'processing' | 'completed' | 'failed' }

Features:
- Color-coded badges
- Status-specific icons
- Animated processing state (spinning icon)

Colors:
- Uploaded: Blue
- Processing: Yellow
- Completed: Green
- Failed: Red
```

### DocumentProcessingStages
```
Props: { stages: ProcessingStage[] }
Type: ProcessingStage = {
  name: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
}

Features:
- Step-by-step progress indicator
- Visual checkmarks for completed
- Spinner for processing
- Gray circles for pending
- Red X for failed
```

## Data Flow

```
User Action: Upload File
    ↓
DocumentUpload: handleUpload()
    ↓
Mock: Simulate API call (1.5s delay)
    ↓
DocumentUpload: onUploadComplete callback
    ↓
Parent: Increment refreshTrigger
    ↓
DocumentList: useEffect triggers
    ↓
Mock: Load documents from MOCK_DOCUMENTS
    ↓
DocumentList: Update state
    ↓
Render: Document cards with status badges
```

## Integration Points (Wave 4)

```
DocumentUpload
    ↓
[TODO] Real API Call
    ↓
POST /documents
    ↓
Backend: Upload to Supabase Storage
    ↓
Backend: Create document record
    ↓
Response: { id, status, storage_path }
    ↓
DocumentUpload: Trigger refresh
    ↓
DocumentList: Fetch updated list
    ↓
[TODO] GET /documents
    ↓
Backend: Query user's documents
    ↓
Response: Document[]
    ↓
DocumentList: Render with real data
    ↓
[TODO] Supabase Realtime
    ↓
Subscribe to 'documents' table changes
    ↓
Real-time updates as status changes
    ↓
DocumentList: Update state reactively
```

## File Organization

```
/frontend/src/components/Documents/
│
├── Core Components
│   ├── DocumentUpload.tsx      (150 lines)
│   ├── DocumentList.tsx        (262 lines)
│   └── DocumentStatus.tsx      (161 lines)
│
├── Testing
│   └── DocumentsTest.tsx       (67 lines)
│
├── Exports
│   └── index.ts                (4 lines)
│
└── Documentation
    ├── README.md               (223 lines)
    ├── VERIFICATION.md         (Current file)
    └── COMPONENT_TREE.md       (This file)

Total: 867 lines
```

## Styling System

```
Tailwind CSS Classes
├── Layout: flex, grid, space-y, gap, p-*, m-*
├── Colors: bg-*, text-*, border-*
├── Effects: hover:*, transition-*, animate-*
├── Typography: font-*, text-*
└── Utilities: rounded-*, shadow-*

shadcn/ui Components
├── Card, CardHeader, CardTitle, CardDescription, CardContent
├── Button (with variants)
└── Avatar (used in chat, available for future use)

Custom Utilities
└── cn() - Tailwind merge utility from @/lib/utils
```

## Type System

```typescript
// Document type (from DocumentList.tsx)
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

// Component props
interface DocumentUploadProps {
  onUploadComplete?: () => void
}

interface DocumentListProps {
  refreshTrigger?: number
}

interface DocumentStatusProps {
  status: 'uploaded' | 'processing' | 'completed' | 'failed'
}

interface ProcessingStage {
  name: string
  status: 'pending' | 'processing' | 'completed' | 'failed'
}

interface DocumentProcessingStagesProps {
  stages: ProcessingStage[]
}
```

## State Management

```
Component-Level State (useState)
├── DocumentUpload
│   ├── uploading: boolean
│   └── dragActive: boolean
│
└── DocumentList
    ├── documents: Document[]
    └── loading: boolean

Props-Based Communication
├── onUploadComplete: callback
└── refreshTrigger: number (increment to refresh)

Future State (Wave 4)
├── Supabase Auth Session
├── Realtime Subscription
└── Error/Success Notifications
```

## Mock vs Real Data

```
Current (Wave 2):
├── MOCK_DOCUMENTS array with 4 samples
├── Simulated upload delay
└── No API calls

Future (Wave 4):
├── Real API endpoints
├── Supabase Storage
├── Realtime updates
└── Authentication tokens
```

## Testing Strategy

```
Manual Testing (DocumentsTest component):
├── Render all components
├── Visual verification
├── Type checking
└── Build verification

TypeScript Compilation:
└── npx tsc --noEmit --skipLibCheck

Integration Testing (Wave 4):
├── Upload actual files
├── Verify storage
├── Check database records
└── Validate realtime updates
```
