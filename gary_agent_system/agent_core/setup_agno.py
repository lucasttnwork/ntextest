#!/usr/bin/env python3
"""
Script de Instalação e Configuração do Framework Agno
Configura automaticamente o sistema para usar a arquitetura Agno otimizada
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Any

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgnoSetup:
    """Classe para instalação e configuração do Agno"""
    
    def __init__(self):
        """Inicializa o setup do Agno"""
        self.project_root = Path(__file__).parent
        self.requirements_file = self.project_root / "requirements.txt"
        self.env_file = self.project_root / ".env"
        self.agno_config_file = self.project_root / "agno_config.py"
        
        # Status de instalação
        self.installation_status = {
            "agno_installed": False,
            "dependencies_installed": False,
            "environment_configured": False,
            "agno_configured": False
        }
    
    def run_setup(self) -> bool:
        """Executa o setup completo do Agno"""
        logger.info("🚀 Iniciando setup do Framework Agno para NTEX")
        
        try:
            # 1. Verificar Python
            if not self._check_python_version():
                return False
            
            # 2. Instalar dependências
            if not self._install_dependencies():
                return False
            
            # 3. Verificar instalação do Agno
            if not self._verify_agno_installation():
                return False
            
            # 4. Configurar variáveis de ambiente
            if not self._configure_environment():
                return False
            
            # 5. Configurar Agno
            if not self._configure_agno():
                return False
            
            # 6. Testar configuração
            if not self._test_configuration():
                return False
            
            logger.info("✅ Setup do Agno concluído com sucesso!")
            self._print_next_steps()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro durante setup: {e}")
            return False
    
    def _check_python_version(self) -> bool:
        """Verifica versão do Python"""
        logger.info("🔍 Verificando versão do Python...")
        
        if sys.version_info < (3, 8):
            logger.error("❌ Python 3.8+ é necessário")
            return False
        
        logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
        return True
    
    def _install_dependencies(self) -> bool:
        """Instala dependências do projeto"""
        logger.info("📦 Instalando dependências...")
        
        try:
            # Atualizar pip
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # Instalar dependências
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)], 
                         check=True, capture_output=True)
            
            logger.info("✅ Dependências instaladas com sucesso")
            self.installation_status["dependencies_installed"] = True
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Erro ao instalar dependências: {e}")
            return False
    
    def _verify_agno_installation(self) -> bool:
        """Verifica se o Agno foi instalado corretamente"""
        logger.info("🔍 Verificando instalação do Agno...")
        
        try:
            import agno
            logger.info(f"✅ Agno {agno.__version__} instalado com sucesso")
            self.installation_status["agno_installed"] = True
            return True
            
        except ImportError:
            logger.error("❌ Agno não foi instalado corretamente")
            return False
    
    def _configure_environment(self) -> bool:
        """Configura variáveis de ambiente"""
        logger.info("⚙️ Configurando variáveis de ambiente...")
        
        try:
            # Verificar se .env existe
            if not self.env_file.exists():
                logger.warning("⚠️ Arquivo .env não encontrado. Criando template...")
                self._create_env_template()
            
            # Verificar variáveis obrigatórias
            required_vars = ["OPENAI_API_KEY"]
            missing_vars = []
            
            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            if missing_vars:
                logger.warning(f"⚠️ Variáveis de ambiente faltando: {', '.join(missing_vars)}")
                logger.info("💡 Configure estas variáveis no arquivo .env")
                return False
            
            logger.info("✅ Variáveis de ambiente configuradas")
            self.installation_status["environment_configured"] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar ambiente: {e}")
            return False
    
    def _create_env_template(self):
        """Cria template do arquivo .env"""
        env_template = """# Configurações do Sistema NTEX
# Framework Agno

# OpenAI API
OPENAI_API_KEY=sua_chave_openai_aqui

# Anthropic API (opcional)
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui

# Supabase
SUPABASE_URL=sua_url_supabase_aqui
SUPABASE_ANON_KEY=sua_chave_anon_supabase_aqui

# Configurações do Sistema
NTEX_JWT_SECRET=ntex_secret_key_2025
NTEX_ENVIRONMENT=development

# Configurações de Performance
MAX_CONCURRENT_AGENTS=5
AGENT_TIMEOUT=30
CACHE_ENABLED=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=ntex_system.log
"""
        
        with open(self.env_file, 'w') as f:
            f.write(env_template)
        
        logger.info("📝 Template .env criado. Configure as variáveis necessárias.")
    
    def _configure_agno(self) -> bool:
        """Configura o framework Agno"""
        logger.info("⚙️ Configurando framework Agno...")
        
        try:
            # Verificar se agno_config.py existe
            if not self.agno_config_file.exists():
                logger.error("❌ Arquivo agno_config.py não encontrado")
                return False
            
            # Testar configuração
            from agno_config import get_agno_config
            config = get_agno_config()
            
            # Validar configuração
            validation = config.validate_config()
            if not validation["valid"]:
                logger.error(f"❌ Configuração inválida: {validation['errors']}")
                return False
            
            if validation["warnings"]:
                logger.warning(f"⚠️ Avisos de configuração: {validation['warnings']}")
            
            logger.info("✅ Framework Agno configurado")
            self.installation_status["agno_configured"] = True
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar Agno: {e}")
            return False
    
    def _test_configuration(self) -> bool:
        """Testa a configuração do Agno"""
        logger.info("🧪 Testando configuração...")
        
        try:
            # Testar importação dos agentes
            from master_agent import NTEXMasterAgent
            from copy_agent import CopyAgent
            from design_agent import DesignAgent
            
            # Testar inicialização dos agentes
            master = NTEXMasterAgent()
            copy = CopyAgent()
            design = DesignAgent()
            
            # Verificar status do Agno
            agno_status = master.get_agno_status()
            
            if agno_status["agno_available"]:
                logger.info("✅ Agentes funcionando com framework Agno")
            else:
                logger.warning("⚠️ Agentes funcionando em modo fallback")
            
            logger.info("✅ Teste de configuração concluído")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no teste de configuração: {e}")
            return False
    
    def _print_next_steps(self):
        """Imprime próximos passos"""
        logger.info("\n" + "="*60)
        logger.info("🎯 PRÓXIMOS PASSOS")
        logger.info("="*60)
        
        if self.installation_status["agno_configured"]:
            logger.info("✅ Framework Agno configurado com sucesso!")
            logger.info("🚀 Você pode agora usar todas as funcionalidades avançadas:")
            logger.info("   • Agent Teams para coordenação")
            logger.info("   • Workflows determinísticos")
            logger.info("   • ReasoningTools para tomada de decisões")
            logger.info("   • Storage e Memory nativos")
        else:
            logger.info("⚠️ Framework Agno não configurado completamente")
            logger.info("📚 Consulte a documentação: https://docs.agno.com")
        
        logger.info("\n🔧 Para testar o sistema:")
        logger.info("   python working_chat_interface.py")
        
        logger.info("\n📊 Para verificar status:")
        logger.info("   curl http://localhost:5003/api/agents/status")
        
        logger.info("\n💡 Para funcionalidades avançadas:")
        logger.info("   • Instale o framework Agno: pip install agno")
        logger.info("   • Configure as variáveis de ambiente")
        logger.info("   • Reinicie o sistema")
        
        logger.info("="*60)
    
    def get_installation_status(self) -> Dict[str, bool]:
        """Retorna status da instalação"""
        return self.installation_status
    
    def diagnose_issues(self) -> List[str]:
        """Diagnostica problemas de instalação"""
        issues = []
        
        if not self.installation_status["agno_installed"]:
            issues.append("Framework Agno não instalado")
        
        if not self.installation_status["dependencies_installed"]:
            issues.append("Dependências não instaladas")
        
        if not self.installation_status["environment_configured"]:
            issues.append("Variáveis de ambiente não configuradas")
        
        if not self.installation_status["agno_configured"]:
            issues.append("Framework Agno não configurado")
        
        return issues

def main():
    """Função principal"""
    setup = AgnoSetup()
    
    if setup.run_setup():
        logger.info("🎉 Setup concluído com sucesso!")
        return 0
    else:
        logger.error("❌ Setup falhou")
        
        # Diagnóstico
        issues = setup.diagnose_issues()
        if issues:
            logger.error("🔍 Problemas identificados:")
            for issue in issues:
                logger.error(f"   • {issue}")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
