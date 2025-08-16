export interface ChatResponse {
  success: boolean
  response?: string
  agent?: string
  capabilities?: string[]
  error?: string
}

export const sendMessageToBackend = async (
  message: string, 
  sessionId: string
): Promise<ChatResponse> => {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data

  } catch (error) {
    console.error('Erro ao enviar mensagem:', error)
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Erro de conexão'
    }
  }
}

export const getAgentsStatus = async (): Promise<any> => {
  try {
    const response = await fetch('/api/agents/status')
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()

  } catch (error) {
    console.error('Erro ao obter status dos agentes:', error)
    return null
  }
}

export const getSessions = async (): Promise<any[]> => {
  try {
    const response = await fetch('/api/sessions')
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()

  } catch (error) {
    console.error('Erro ao obter sessões:', error)
    return []
  }
}
