import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import { Toaster } from 'react-hot-toast'

function App() {
  return (
    <div className="flex h-screen bg-chat-bg overflow-hidden">
      <Sidebar />
      <ChatArea />
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#444654',
            color: '#ececf1',
            border: '1px solid #565869',
          },
        }}
      />
    </div>
  )
}

export default App
