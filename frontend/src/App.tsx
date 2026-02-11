import { useAuth } from '@/hooks/useAuth'
import { LoginForm } from '@/components/Auth/LoginForm'
import { ChatContainer } from '@/components/Chat/ChatContainer'
import { Button } from '@/components/ui/button'

function App() {
  const { user, loading, signOut } = useAuth()

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <LoginForm />
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col">
      <header className="border-b px-4 py-2 flex justify-between items-center">
        <h1 className="text-xl font-semibold">Agentic RAG</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-600">{user.email}</span>
          <Button variant="outline" size="sm" onClick={() => signOut()}>
            Sign Out
          </Button>
        </div>
      </header>
      <main className="flex-1 overflow-hidden">
        <ChatContainer />
      </main>
    </div>
  )
}

export default App
