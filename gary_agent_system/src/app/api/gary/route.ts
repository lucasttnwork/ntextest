import { NextRequest, NextResponse } from 'next/server';
import { streamText, convertToModelMessages } from 'ai';
import { openai } from '@ai-sdk/openai';

// Função para converter mensagens AI SDK para formato Gary Bencivenga
function convertMessagesToGaryFormat(messages: Array<{role: string; content: string; parts?: any[]}>) {
  const lastMessage = messages[messages.length - 1];
  return {
    message: lastMessage?.content || '',
    conversation_history: messages.slice(0, -1).map(msg => ({
      role: msg.role,
      content: msg.content
    })),
    timestamp: new Date().toISOString(),
    session_id: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  };
}

export async function POST(request: NextRequest) {
  try {
    const { messages, webSearch, sessionId } = await request.json();

    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json(
        {
          error: 'Mensagens são obrigatórias',
          id: `error_${Date.now()}`,
          role: 'assistant',
          content: 'Por favor, forneça uma mensagem válida para o Gary Bencivenga analisar.'
        },
        { status: 400 }
      );
    }

    // Use provider direto (OpenAI) para evitar AI Gateway sem crédito
    const model = openai('gpt-4o-mini');
    const result = await streamText({
      model,
      messages: convertToModelMessages(messages),
      system: `Você é Gary Bencivenga, o maior copywriter do mundo. Responda sempre em português brasileiro, com o estilo característico de Gary: persuasivo, confiante e focado em resultados. Use linguagem direta, evite jargões desnecessários e foque no valor que você entrega para o cliente. Sempre que possível, inclua chamadas para ação (CTAs) e demonstre expertise em copywriting.`,
    });

    // Return streaming response with sources and reasoning
    return result.toUIMessageStreamResponse({
      sendSources: true,
      sendReasoning: true,
    });

  } catch (error) {
    console.error('❌ Erro na API Gary Bencivenga:', error);
    
    // Mensagem de erro no estilo Gary Bencivenga
    const errorMessage = error.message.includes('ECONNREFUSED') 
      ? '🚨 O mestre Gary está temporariamente indisponível. Por favor, tente novamente em instantes.'
      : `🎯 Parceiro, encontramos um desafio aqui: ${error.message}. Mas não tema - os maiores copywriters do mundo superam obstáculos todos os dias!`;

    return NextResponse.json(
      { 
        error: 'Erro ao processar com Gary Bencivenga',
        id: `error_${Date.now()}`,
        role: 'assistant',
        content: errorMessage
      },
      { status: 500 }
    );
  }
}

// Rota GET para informações do Gary Bencivenga
export async function GET() {
  return NextResponse.json({
    name: 'Gary Bencivenga Copywriter Agent',
    version: '1.0.0',
    description: 'O maior copywriter do mundo, agora em forma de IA',
    specialties: [
      'Copy de alta conversão',
      'Análise de mercado',
      'Personas e psicologia do consumidor',
      'Headlines matadoras',
      'Estratégias de marketing direto',
      'Testes A/B e otimização'
    ],
    status: 'online',
    powered_by: 'NTEX AI + OpenRouter API (Grok)',
    endpoints: {
      POST: '/api/gary',
      GET: '/api/gary'
    },
    motto: '"A persuasão é a arte de mostrar às pessoas como elas podem obter exatamente o que desejam." - Gary Bencivenga'
  });
}