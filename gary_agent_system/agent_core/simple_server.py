#!/usr/bin/env python3
"""
Servidor Flask simplificado para NTEX
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Template HTML simples
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NTEX - Sistema de Agentes IA</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .api-test { background: #f0f8ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Sistema NTEX - Agentes IA</h1>
            <p>Sistema de agentes especializados com memória persistente</p>
        </div>
        
        <div class="status">
            <h3>✅ Status do Sistema</h3>
            <p>Servidor Flask funcionando na porta {{ port }}</p>
            <p>Timestamp: {{ timestamp }}</p>
        </div>
        
        <div class="api-test">
            <h3>🧪 Teste da API</h3>
            <button onclick="testAPI()">Testar API</button>
            <div id="api-result"></div>
        </div>
        
        <div class="status">
            <h3>🔗 Endpoints Disponíveis</h3>
            <ul>
                <li><strong>GET /</strong> - Esta página</li>
                <li><strong>GET /api/status</strong> - Status do sistema</li>
                <li><strong>GET /api/agents</strong> - Lista de agentes</li>
            </ul>
        </div>
    </div>
    
    <script>
        async function testAPI() {
            const resultDiv = document.getElementById('api-result');
            resultDiv.innerHTML = '🔄 Testando...';
            
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                resultDiv.innerHTML = '<strong>✅ API OK!</strong><br>Resposta: ' + JSON.stringify(data, null, 2);
            } catch (error) {
                resultDiv.innerHTML = '<strong>❌ Erro na API:</strong><br>' + error.message;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Página principal"""
    from datetime import datetime
    return render_template_string(HTML_TEMPLATE, 
                               port=os.environ.get('PORT', 5003),
                               timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/api/status')
def api_status():
    """Status da API"""
    return jsonify({
        "status": "ok",
        "message": "Sistema NTEX funcionando!",
        "timestamp": "2025-08-15 22:00:00",
        "version": "1.0.0"
    })

@app.route('/api/agents')
def api_agents():
    """Lista de agentes"""
    return jsonify({
        "agents": [
            {
                "name": "Master Agent",
                "status": "active",
                "capabilities": ["coordenação", "roteamento"]
            },
            {
                "name": "Copy Agent", 
                "status": "active",
                "capabilities": ["copywriting", "redes sociais"]
            },
            {
                "name": "Design Agent",
                "status": "active", 
                "capabilities": ["design visual", "templates"]
            }
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    print(f"🚀 Iniciando servidor NTEX na porta {port}...")
    print(f"📱 Acesse: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
