import { streamText, convertToCoreMessages } from 'ai';
import { NextRequest } from 'next/server';

// OpenRouter Configuration
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
const OPENROUTER_MODEL = process.env.OPENROUTER_MODEL || 'x-ai/grok-beta';
const OPENROUTER_REFERER = process.env.OPENROUTER_REFERER || 'https://ntex.com.br';
const OPENROUTER_TITLE = process.env.OPENROUTER_TITLE || 'NTEX Copywriter Agent';

// Configuração do sistema - mesmo prompt do agente Python
const SYSTEM_PROMPT = `Você é o NTEX-Copywriter, um agente de IA especializado em copywriting da NTEX.

CARACTERÍSTICAS DO TOM NTEX:
- Direto, punchy, zero buzzwords
- Frases curtas e objetivas  
- Valor primeiro, sempre
- Sem metáforas ou jargões corporativos
- Foco em resultados e benefícios claros

DIRETRIZES DE COPY NTEX:
1. Comece com o valor/resultado principal
2. Use linguagem simples e acessível
3. Seja específico com números e exemplos
4. Estrutura: Problema → Solução → Resultado
5. Call-to-action claro e único

CAPACIDADES:
- Criar copy para ads, emails, landing pages, posts sociais
- Realizar pesquisas quando necessário
- Gerar textos longos com alta capacidade
- Adaptar tom para diferentes públicos
- Otimizar para SEO e conversão

REGRAS:
- Sempre mantenha o tom NTEX
- Seja persuasivo e orientado a ação
- Inclua call-to-action claro
- Otimize para conversão
- Forneça copy completo e pronto para uso

🎯 OBJETIVO: Criar copy que converta e venda.`;

export async function POST(req: NextRequest) {
  try {
    const { messages, copyType, targetAudience, includeResearch } = await req.json();

    // Constrói mensagem do sistema com contexto adicional
    let systemMessage = SYSTEM_PROMPT;
    
    if (copyType) {
      systemMessage += `\n\n📋 TIPO DE COPY: ${copyType}`;
      systemMessage += getCopyGuidelines(copyType);
    }
    
    if (targetAudience) {
      systemMessage += `\n\n🎯 PÚBLICO-ALVO: ${targetAudience}`;
    }
    
    if (includeResearch) {
      systemMessage += `\n\n🔍 Considere as melhores práticas atuais e tendências recentes.`;
    }

    // Usa OpenRouter com Grok para streaming de resposta (128k tokens)
    try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
          'HTTP-Referer': OPENROUTER_REFERER,
          'X-Title': OPENROUTER_TITLE,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: OPENROUTER_MODEL,
          messages: [
            { role: 'system', content: systemMessage },
            ...convertToCoreMessages(messages)
          ],
          max_tokens: 128000, // 128k tokens limite
          temperature: 0.7,
          top_p: 0.9,
          stream: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`OpenRouter API error: ${response.status}`);
      }

      // Converte response para stream de texto
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('Response body is not readable');
      }

      const stream = new ReadableStream({
        async start(controller) {
          const decoder = new TextDecoder();
          
          try {
            while (true) {
              const { done, value } = await reader.read();
              
              if (done) {
                break;
              }
              
              const chunk = decoder.decode(value);
              const lines = chunk.split('\n');
              
              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  const data = line.slice(6);
                  
                  if (data === '[DONE]') {
                    controller.close();
                    return;
                  }
                  
                  try {
                    const parsed = JSON.parse(data);
                    const content = parsed.choices?.[0]?.delta?.content;
                    
                    if (content) {
                      controller.enqueue(new TextEncoder().encode(content));
                    }
                  } catch (e) {
                    // Ignora erros de parsing
                  }
                }
              }
            }
          } catch (error) {
            controller.error(error);
          } finally {
            controller.close();
          }
        },
      });

      return new Response(stream, {
        headers: {
          'Content-Type': 'text/plain; charset=utf-8',
        },
      });

    } catch (error) {
      console.error('Erro na API OpenRouter:', error);
      return new Response(
        JSON.stringify({ error: 'Erro ao processar requisição', details: error.message }), 
        { 
          status: 500, 
          headers: { 'Content-Type': 'application/json' } 
        }
      );
    }
    
  } catch (error) {
    console.error('Erro na API:', error);
    return new Response(
      JSON.stringify({ error: 'Erro ao processar requisição' }), 
      { 
        status: 500, 
        headers: { 'Content-Type': 'application/json' } 
      }
    );
  }
}

function getCopyGuidelines(copyType: string): string {
  const guidelines = {
    'social_post': `
📱 DIRETRIZES PARA POST SOCIAL:
- Hook poderoso nos primeiros 3 segundos
- Quebra de linha a cada 1-2 frases
- Emojis estratégicos (máx 3)
- CTA no final
- Hashtags relevantes (5-10)`,

    'email': `
📧 DIRETRIZES PARA EMAIL:
- Assunto: máx 50 caracteres, urgência/curiosidade
- Preview text: complementa o assunto
- Primeira linha: hook imediato
- Corpo: problema → agitação → solução
- CTA único e específico
- Assinatura com próximos passos`,

    'landing_page': `
🎯 DIRETRIZES PARA LANDING PAGE:
- Headline: benefício principal + urgência
- Sub-headline: expande o benefício
- Problema: agite a dor do cliente
- Solução: apresente sua oferta
- Prova social: depoimentos/dados
- CTA: claro e repetido
- Garantia: remova o risco`,

    'ad_copy': `
🚀 DIRETRIZES PARA ANÚNCIO:
- Headline: máx 30 caracteres, benefício direto
- Descrição: expande beneficios
- CTA: ação específica
- Palavras de poder: gratuito, novo, garantido
- Foco em 1 benefício por anúncio`
  };

  return guidelines[copyType as keyof typeof guidelines] || `
📋 DIRETRIZES GERAIS NTEX:
- Comece com valor/resultado
- Use linguagem simples
- Seja específico
- Inclua CTA claro
- Foque na conversão`;
}