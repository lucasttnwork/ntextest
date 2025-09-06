import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { messages, model, webSearch } = await request.json();

    // Converter mensagens do formato AI SDK para o formato esperado pelo Flask
    const lastMessage = messages[messages.length - 1];
    const message = lastMessage?.content || '';

    if (!message) {
      return NextResponse.json({ error: 'Mensagem vazia' }, { status: 400 });
    }

    // Fazer requisição para o backend Flask existente
    const response = await fetch('http://localhost:5003/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        // Adicionar informações do modelo se necessário
        model: model,
        webSearch: webSearch,
      }),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || 'Erro no backend');
    }

    // Converter resposta do Flask para o formato esperado pelo AI SDK
    const aiSdkResponse = {
      id: `msg_${Date.now()}`,
      role: 'assistant',
      content: data.response,
      createdAt: new Date(),
    };

    return NextResponse.json(aiSdkResponse);
  } catch (error) {
    console.error('Error in chat API:', error);
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    );
  }
}
