import { NextRequest } from 'next/server';
import { streamText, UIMessage, convertToModelMessages } from 'ai';
import { openai } from '@ai-sdk/openai';

export const maxDuration = 30;

export async function POST(request: NextRequest) {
  try {
    const {
      messages,
      model,
      webSearch,
    }: { messages: UIMessage[]; model?: string; webSearch?: boolean } = await request.json();

    const result = streamText({
      model: openai('gpt-4o-mini'),
      messages: convertToModelMessages(messages),
      system:
        'Você é um assistente útil que responde em português brasileiro e pode citar fontes quando disponível.',
    });

    return result.toUIMessageStreamResponse({
      sendSources: true,
      sendReasoning: true,
    });
  } catch (error) {
    console.error('Error in chat API:', error);
    return new Response(JSON.stringify({ error: 'Erro interno do servidor' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
