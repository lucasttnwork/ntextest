'use client';

import { useState } from 'react';
import { Menu, X, Target, MessageSquare, Settings } from 'lucide-react';
import AIChat from '@/components/ai-chat';
import GaryChat from '@/components/gary-chat';
import CopywriterInterface from '@/copywriter-app/app/page';

interface ChatType {
  id: string;
  name: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  component: React.ComponentType;
  color: string;
}

const chatTypes: ChatType[] = [
  {
    id: 'gary',
    name: 'Gary Bencivenga AI',
    description: 'O mestre do copywriting agora em IA',
    icon: Target,
    component: GaryChat,
    color: 'from-purple-600 to-blue-600'
  },
  {
    id: 'general',
    name: 'NTEX AI Chat',
    description: 'Chat inteligente com IA geral',
    icon: MessageSquare,
    component: AIChat,
    color: 'from-green-600 to-blue-600'
  },
  {
    id: 'copywriter',
    name: 'NTEX Copywriter',
    description: 'Especialista em criação de copy',
    icon: Settings,
    component: CopywriterInterface,
    color: 'from-orange-600 to-red-600'
  }
];

export default function ChatPage() {
  const [activeChat, setActiveChat] = useState<string>('gary');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  const ActiveComponent = chatTypes.find(chat => chat.id === activeChat)?.component || GaryChat;

  const SidebarContent = () => (
    <>
      <div className="p-4 border-b border-border flex items-center justify-between">
        <div className="text-sm font-medium text-foreground/90">NTEX Chats</div>
        <button aria-label="Fechar menu" onClick={() => setMobileSidebarOpen(false)} className="text-muted-foreground hover:text-foreground">
          <X className="w-5 h-5" />
        </button>
      </div>
      <div className="p-3">
        <button
          className="w-full inline-flex items-center justify-center px-4 py-2 rounded-md bg-foreground text-background hover:opacity-90"
          onClick={() => { setActiveChat('gary'); if (mobileSidebarOpen) setMobileSidebarOpen(false); }}
        >Novo chat</button>
      </div>
      <div className="flex-1 min-h-0 px-3 py-2 overflow-y-auto">
        {chatTypes.map((chat) => {
          const Icon = chat.icon;
          const isActive = activeChat === chat.id;
          return (
            <button
              key={chat.id}
              onClick={() => { setActiveChat(chat.id); if (mobileSidebarOpen) setMobileSidebarOpen(false); }}
              className={`w-full mb-2 p-3 rounded-md text-left transition ${isActive ? 'bg-accent text-foreground' : 'hover:bg-accent/60 text-foreground/90'}`}
            >
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-md flex items-center justify-center bg-muted/60`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="truncate">
                  <div className="text-sm font-medium truncate">{chat.name}</div>
                  <div className="text-xs text-muted-foreground truncate">{chat.description}</div>
                </div>
              </div>
            </button>
          );
        })}
      </div>
      <div className="p-3 border-t border-border text-xs text-muted-foreground">
        Powered by NTEX AI
      </div>
    </>
  );
  
  return (
    <div className="flex h-screen bg-background">
      {/* Desktop Sidebar */}
      <aside className={`hidden md:flex w-72 xl:w-80 flex-shrink-0 flex-col min-h-0 bg-sidebar border-r border-border transition-all duration-300 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <SidebarContent />
      </aside>

      {/* Mobile Drawer */}
      {mobileSidebarOpen && (
        <>
          <div className="md:hidden fixed inset-0 z-40 bg-black/60" onClick={() => setMobileSidebarOpen(false)} />
          <aside className="md:hidden fixed inset-y-0 left-0 z-50 w-72 bg-sidebar border-r border-border transform transition-transform duration-300" style={{ transform: mobileSidebarOpen ? 'translateX(0)' : 'translateX(-100%)' }}>
            <SidebarContent />
          </aside>
        </>
      )}

      {/* Main Content */}
      <section className="flex-1 min-w-0 min-h-0 flex flex-col">
        <div className="flex-1 min-h-0">
          <ActiveComponent />
        </div>
      </section>
    </div>
  );
}