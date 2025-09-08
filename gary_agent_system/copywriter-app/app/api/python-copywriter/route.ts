import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import { promisify } from 'util';
import { writeFile, readFile, unlink } from 'fs/promises';
import { join } from 'path';
import { tmpdir } from 'os';

export async function POST(req: NextRequest) {
  try {
    const { prompt, copyType, targetAudience, includeResearch, maxTokens } = await req.json();

    if (!prompt) {
      return NextResponse.json({ error: 'Prompt é obrigatório' }, { status: 400 });
    }

    // Cria arquivo temporário para o prompt
    const tempFile = join(tmpdir(), `copywriter_${Date.now()}.json`);
    const inputData = {
      prompt,
      copy_type: copyType || 'social_post',
      target_audience: targetAudience || '',
      include_research: includeResearch || false,
      max_tokens: maxTokens || 4000
    };

    await writeFile(tempFile, JSON.stringify(inputData));

    // Executa o script Python
    const pythonProcess = spawn('python3', [
      '/Users/lucasttn/Documents/Documents/Cérebro NTEX/scripts/copywriter_cli.py',
      '--file', tempFile
    ]);

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    return new Promise((resolve) => {
      pythonProcess.on('close', async (code) => {
        try {
          // Limpa arquivo temporário
          await unlink(tempFile).catch(() => {});

          if (code !== 0) {
            console.error('Erro no Python:', stderr);
            resolve(NextResponse.json({ 
              error: 'Erro ao executar agente Python', 
              details: stderr 
            }, { status: 500 }));
            return;
          }

          // Extrai o resultado do stdout
          const lines = stdout.split('\n');
          const copyStart = lines.findIndex(line => line.includes('COPY GERADO:'));
          const copyEnd = lines.findIndex((line, index) => index > copyStart && line.includes('==='));
          
          let generatedCopy = '';
          if (copyStart !== -1 && copyEnd !== -1) {
            generatedCopy = lines.slice(copyStart + 1, copyEnd).join('\n').trim();
          }

          // Tenta encontrar arquivo salvo
          const fileMatch = stdout.match(/Salvo em: (.+\.json)/);
          let savedFile = null;
          if (fileMatch) {
            savedFile = fileMatch[1];
            try {
              const savedData = JSON.parse(await readFile(savedFile, 'utf-8'));
              resolve(NextResponse.json({
                copy: generatedCopy || savedData.copy,
                analysis: savedData.analysis,
                savedFile: savedFile,
                researchUsed: savedData.research_used,
                tokensUsed: savedData.tokens_used
              }));
              return;
            } catch (e) {
              // Se não conseguir ler o arquivo, retorna o texto gerado
            }
          }

          resolve(NextResponse.json({
            copy: generatedCopy || stdout,
            rawOutput: stdout
          }));

        } catch (error) {
          console.error('Erro ao processar resultado:', error);
          resolve(NextResponse.json({ 
            error: 'Erro ao processar resultado',
            details: error.message 
          }, { status: 500 }));
        }
      });
    });

  } catch (error) {
    console.error('Erro na API:', error);
    return NextResponse.json({ 
      error: 'Erro interno do servidor',
      details: error.message 
    }, { status: 500 });
  }
}

// Adiciona também uma rota GET para teste
export async function GET() {
  return NextResponse.json({
    message: 'NTEX Copywriter Python API',
    version: '1.0.0',
    status: 'online',
    endpoints: {
      POST: '/api/python-copywriter'
    }
  });
}