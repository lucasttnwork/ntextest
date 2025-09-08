'use client';

import { useState } from 'react';
import { useChat } from '@/hooks/useChat';
import { Copy, RefreshCw, Download, MessageSquare, Target, Search, Brain, TrendingUp } from 'lucide-react';

export default function CopywriterChat() {
  const [copyType, setCopyType] = useState('social_post');
  const [targetAudience, setTargetAudience] = useState('');
  const [includeResearch, setIncludeResearch] = useState(false);
  const [input, setInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const { messages, sendMessage, isLoading } = useChat();

  const copyTypes = [
    { value: 'social_post', label: '📱 Post Social', desc: 'Posts para redes sociais' },
    { value: 'email', label: '📧 Email', desc: 'Emails marketing' },
    { value: 'landing_page', label: '🎯 Landing Page', desc: 'Páginas de captura' },
    { value: 'ad_copy', label: '🚀 Anúncio', desc: 'Anúncios pagos' },
    { value: 'blog_post', label: '📝 Blog Post', desc: 'Artigos de blog' },
    { value: 'sales_page', label: '💰 Página de Vendas', desc: 'Páginas de vendas' }
  ];

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) {
      alert('🎯 Por favor, digite o que você quer criar!');
      return;
    }
    setIsGenerating(true);

    const copyPrompt = `Crie um ${copyTypes.find(t => t.value === copyType)?.label || copyType} sobre: ${input}${targetAudience ? ` para o público: ${targetAudience}` : ''}${includeResearch ? '. Inclua pesquisa atualizada sobre o assunto.' : ''}`;

    await sendMessage(copyPrompt, { webSearch: includeResearch });
    setIsGenerating(false);
    alert('🎯 Copy gerado com sucesso!');
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      alert('📝 Copy copiado para a área de transferência!');
    } catch (error) {
      alert('Erro ao copiar');
    }
  };

  const downloadCopy = (text: string) => {
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ntex-copy-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    alert('📥 Copy baixado com sucesso!');
  };

  const lastMessage = messages[messages.length - 1];
  const generatedCopy = lastMessage?.role === 'assistant' ? lastMessage.content : '';

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <div className="bg-background border-b border-border px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-muted border border-border rounded-full flex items-center justify-center text-foreground font-bold text-sm shadow-lg">
              C
            </div>
            <div>
              <h1 className="text-xl font-bold text-foreground">NTEX Copywriter</h1>
              <p className="text-sm text-muted-foreground">Criação de copy de alta conversão com IA</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
              <Brain className="w-4 h-4" />
              <span>Powered by AI</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-6xl mx-auto p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Painel de Controle */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                  <Target className="w-5 h-5 mr-2" />
                  Configurações
                </h2>

                <form onSubmit={handleFormSubmit} className="space-y-6">
                  {/* Tipo de Copy */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <MessageSquare className="w-4 h-4 inline mr-1" />
                      Tipo de Copy
                    </label>
                    <select
                      value={copyType}
                      onChange={(e) => setCopyType(e.target.value)}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      {copyTypes.map((type) => (
                        <option key={type.value} value={type.value}>
                          {type.label} - {type.desc}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Público-Alvo */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Target className="w-4 h-4 inline mr-1" />
                      Público-Alvo
                    </label>
                    <input
                      type="text"
                      value={targetAudience}
                      onChange={(e) => setTargetAudience(e.target.value)}
                      placeholder="Ex: Empresários B2B, Millennials, etc."
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>

                  {/* Pesquisa na Web */}
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="research"
                      checked={includeResearch}
                      onChange={(e) => setIncludeResearch(e.target.checked)}
                      className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                    />
                    <label htmlFor="research" className="ml-2 text-sm text-gray-700">
                      <Search className="w-4 h-4 inline mr-1" />
                      Incluir pesquisa na web
                    </label>
                  </div>

                  {/* Prompt Input */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <MessageSquare className="w-4 h-4 inline mr-1" />
                      O que você quer criar?
                    </label>
                    <textarea
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder="Ex: Crie um post sobre automação de marketing para empresários B2B..."
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent h-32 resize-none"
                      disabled={isLoading}
                    />
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="w-full bg-primary text-primary-foreground py-3 px-6 rounded-lg font-semibold hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
                  >
                    {isLoading ? (
                      <>
                        <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
                        Gerando Copy...
                      </>
                    ) : (
                      '✨ Gerar Copy'
                    )}
                  </button>
                </form>
              </div>
            </div>

            {/* Área de Resultado */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Copy Gerado
                  </h2>
                  {generatedCopy && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => copyToClipboard(generatedCopy)}
                        className="p-2 text-gray-600 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                        title="Copiar"
                      >
                        <Copy className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => downloadCopy(generatedCopy)}
                        className="p-2 text-gray-600 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                        title="Baixar"
                      >
                        <Download className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => {
                          setInput('');
                          alert('Funcionalidade de refazer será implementada em breve!');
                        }}
                        className="p-2 text-gray-600 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-colors"
                        title="Refazer"
                      >
                        <RefreshCw className="w-5 h-5" />
                      </button>
                    </div>
                  )}
                </div>

                {/* Preview do Copy */}
                <div className="min-h-[400px]">
                  {isLoading && (
                    <div className="flex items-center justify-center h-64">
                      <div className="text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
                        <p className="text-gray-600">Criando copy incrível...</p>
                      </div>
                    </div>
                  )}

                  {generatedCopy && !isLoading && (
                    <div className="prose max-w-none">
                      <div className="bg-gray-50 rounded-lg p-6 border-l-4 border-purple-500">
                        <pre className="whitespace-pre-wrap font-sans text-gray-800 leading-relaxed">
                          {generatedCopy}
                        </pre>
                      </div>
                    </div>
                  )}

                  {!generatedCopy && !isLoading && (
                    <div className="text-center text-gray-500 mt-20">
                      <MessageSquare className="w-16 h-16 mx-auto mb-4 opacity-50" />
                      <p className="text-lg">Digite o que você quer criar e clique em "Gerar Copy"</p>
                      <p className="text-sm mt-2">O agente NTEX criará copy de alta conversão para você</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Dicas e Melhores Práticas */}
              <div className="mt-6 bg-muted rounded-xl p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  💡 Dicas para Copy de Alta Conversão
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
                  <div>
                    <h4 className="font-semibold mb-2">🎯 Torne-se Específico</h4>
                    <p>Mencione números, prazos e resultados concretos</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">⚡ Crie Urgência</h4>
                    <p>Use escassez e prazos limitados para motivar ação</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">💰 Foque no Valor</h4>
                    <p>Mostre o que o cliente ganha, não o que você faz</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">🚀 Seja Direto</h4>
                    <p>Evite jargões - use linguagem simples e clara</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}