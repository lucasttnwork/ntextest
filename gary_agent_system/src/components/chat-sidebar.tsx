'use client';

import { useState, useEffect } from 'react';
import { MessageSquare, Plus, Trash2, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { ntexApi } from '@/services/api';
import { ChatSession } from '@/types/chat';

interface ChatSidebarProps {
  currentSessionId: string | undefined;
  onSessionSelect: (sessionId: string) => void;
  onNewChat: () => void;
}

export function ChatSidebar({ currentSessionId, onSessionSelect, onNewChat }: ChatSidebarProps) {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const sessionData = await ntexApi.getSessions();
      setSessions(sessionData);
    } catch (error) {
      console.error('Erro ao carregar sessões:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.abs(now.getTime() - date.getTime()) / (1000 * 60 * 60);

    if (diffInHours < 24) {
      return date.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
      });
    } else if (diffInHours < 168) { // 7 dias
      return date.toLocaleDateString('pt-BR', {
        weekday: 'short',
        hour: '2-digit',
        minute: '2-digit'
      });
    } else {
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit'
      });
    }
  };

  const handleNewChat = async () => {
    try {
      // Criar nova sessão
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_name: `Nova conversa ${new Date().toLocaleDateString('pt-BR')}`
        }),
      });

      if (response.ok) {
        const data = await response.json();
        onNewChat();
        // Recarregar sessões
        loadSessions();
      }
    } catch (error) {
      console.error('Erro ao criar nova sessão:', error);
    }
  };

  return (
    <div className="flex flex-col h-full bg-sidebar border-r border-sidebar-border overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-sidebar-border flex-shrink-0">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-sidebar-foreground">
            Gary Bencivenga
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={handleNewChat}
            className="text-sidebar-foreground/60 hover:text-sidebar-foreground"
          >
            <Plus className="h-4 w-4" />
          </Button>
        </div>
        <p className="text-sm text-sidebar-foreground/60 mt-1">
          Especialista em Copywriting
        </p>
      </div>

      {/* Sessions List */}
      <ScrollArea className="flex-1 min-h-0">
        <div className="space-y-1 p-2">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-sidebar-foreground"></div>
            </div>
          ) : sessions.length === 0 ? (
            <div className="text-center py-8 text-sidebar-foreground/60">
              <MessageSquare className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">Nenhuma conversa ainda</p>
            </div>
          ) : (
            sessions.map((session) => (
              <button
                key={session.id}
                onClick={() => onSessionSelect(session.id)}
                className={`w-full text-left p-3 rounded-lg transition-colors group ${
                  currentSessionId === session.id
                    ? 'bg-sidebar-accent border border-sidebar-border'
                    : 'hover:bg-sidebar-accent/60'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-sidebar-foreground truncate">
                      {session.session_name}
                    </p>
                    <p className="text-xs text-sidebar-foreground/60 mt-1">
                      {session.last_activity ? formatDate(session.last_activity) : 'Nunca'}
                    </p>
                  </div>
                  <div
                    className="opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6 p-0 text-sidebar-foreground/60 hover:text-red-500 rounded flex items-center justify-center hover:bg-red-50 dark:hover:bg-red-900/20 cursor-pointer"
                    onClick={(e) => {
                      e.stopPropagation();
                      // TODO: Implementar exclusão de sessão
                      console.log('Excluir sessão:', session.id);
                    }}
                    title="Excluir conversa"
                  >
                    <Trash2 className="h-3 w-3" />
                  </div>
                </div>
              </button>
            ))
          )}
        </div>
      </ScrollArea>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border flex-shrink-0">
        <div
          className="w-full justify-start text-sidebar-foreground/60 hover:text-sidebar-foreground flex items-center cursor-pointer p-2 rounded hover:bg-sidebar-accent/60"
          onClick={() => {
            // TODO: Implementar configurações
            console.log('Abrir configurações');
          }}
        >
          <Settings className="h-4 w-4 mr-2" />
          Configurações
        </div>
      </div>
    </div>
  );
}
