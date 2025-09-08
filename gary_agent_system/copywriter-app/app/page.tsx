'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';
import { Copy, RefreshCw, Download, MessageSquare, Target, Search, Settings } from 'lucide-react';
import { toast } from 'sonner';

export default function CopywriterInterface() {
  const [copyType, setCopyType] = useState('social_post');
  const [targetAudience, setTargetAudience] = useState('');
  const [includeResearch, setIncludeResearch] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const { messages, input, handleInputChange, handleSubmit, reload, isLoading } = useChat({
    api: '/api/copywriter',
    body: {
      copyType,
      targetAudience,
      includeResearch
    },
    onFinish: () => {
      setIsGenerating(false);
      toast.success('Copy gerado com sucesso!');
    },
    onError: (error) => {
      setIsGenerating(false);
      toast.error('Erro ao gerar copy');
      console.error(error);
    }
  });

  const copyTypes = [
    { value: 'social_post', label: '📱 Post Social', desc: 'Posts para redes sociais' },
    { value: 'email', label: '📧 Email', desc: 'Emails marketing' },
    { value: 'landing_page', label: '🎯 Landing Page', desc: 'Páginas de captura' },
    { value: 'ad_copy', label: '🚀 Anúncio', desc: 'Anúncios pagos' },
    { value: 'blog_post', label: '📝 Blog Post', desc: 'Artigos de blog' },
    { value: 'sales_page', label: '💰 Página de Vendas', desc: 'Páginas de vendas' }
  ];

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) {
      toast.error('Por favor, digite o que você quer criar');
      return;
    }
    setIsGenerating(true);
    handleSubmit(e);
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast.success('Copy copiado para a área de transferência!');
    } catch (error) {
      toast.error('Erro ao copiar');
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
    toast.success('Copy baixado!');
  };

  const lastMessage = messages[messages.length - 1];
  const generatedCopy = lastMessage?.role === 'assistant' ? lastMessage.content : '';

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🚀 NTEX Copywriter Agent
          </h1>
          <p className="text-lg text-gray-600">
            Crie copy de alta conversão com o poder da IA
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Painel de Controle */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                <Settings className="w-5 h-5 mr-2" />
                Configurações
              </h2>

              <form onSubmit={handleFormSubmit} className="space-y-6">
                {/* Tipo de Copy */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Copy className="w-4 h-4 inline mr-1" />
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
                    onChange={handleInputChange}
                    placeholder="Ex: Crie um post sobre automação de marketing para empresários B2B..."
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent h-32 resize-none"
                    disabled={isLoading}
                  />
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
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
                      onClick={() => reload()}
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
            <div className="mt-6 bg-gradient-to-r from-purple-100 to-blue-100 rounded-xl p-6">
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
  );
}