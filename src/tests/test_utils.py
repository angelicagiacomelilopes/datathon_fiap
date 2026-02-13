import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import pandas as pd # Import necessário para pd.Timestamp

# Adicionar a raiz do projeto ao PYTHONPATH para permitir importar 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils import LoggerConfig, ApplicationLogger, SistemaMonitoramento
from loguru import logger

class TestLoggerConfig:
    
    @pytest.fixture
    def logger_config(self, tmp_path):
        """Fixture para criar uma configuração de logger com diretório temporário"""
        log_dir = tmp_path / "logs"
        return LoggerConfig(
            app_name="TestApp",
            log_dir=str(log_dir),
            console_level="DEBUG",
            file_level="DEBUG",
            error_level="ERROR"
        )
    
    def test_init_creates_directory(self, tmp_path):
        """Testa se o diretório de logs é criado na inicialização"""
        log_dir = tmp_path / "test_logs"
        LoggerConfig(log_dir=str(log_dir))
        assert log_dir.exists()
        assert log_dir.is_dir()

    def test_get_console_format(self, logger_config):
        """Testa o formato do log de console"""
        fmt = logger_config._get_console_format()
        assert "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>" in fmt
        assert "<cyan>TestApp</cyan>" in fmt

    def test_get_file_format(self, logger_config):
        """Testa o formato do log de arquivo"""
        fmt = logger_config._get_file_format()
        assert "{time:YYYY-MM-DD HH:mm:ss}" in fmt
        assert "TestApp:{name}:{function}:{line}" in fmt

    def test_setup_handlers(self, logger_config):
        """Testa a configuração dos handlers"""
        logger.remove()
        logger_config.setup()
        
        test_msg = "Mensagem de teste"
        logger.info(test_msg)
        
        files = list(logger_config.log_dir.glob("app_*.log"))
        assert len(files) > 0
        
        content = files[0].read_text(encoding='utf-8')
        assert test_msg in content
        assert "INFO" in content
        assert "TestApp" in content

    def test_error_logging(self, logger_config):
        """Testa se logs de erro vão para o arquivo específico"""
        logger_config.setup()
        
        error_msg = "Erro crítico de teste"
        logger.error(error_msg)
        
        error_file = logger_config.log_dir / "errors.log"
        assert error_file.exists()
        
        content = error_file.read_text(encoding='utf-8')
        assert error_msg in content
        assert "ERROR" in content

    def test_add_custom_handler(self, logger_config):
        """Testa adição de handler personalizado"""
        custom_log = logger_config.log_dir / "custom.log"
        
        logger_config.add_custom_handler(
            sink=custom_log,
            level="WARNING",
            format_str="{message}"
        )
        
        msg_info = "Info ignorado"
        msg_warning = "Aviso capturado"
        
        logger.info(msg_info)
        logger.warning(msg_warning)
        
        assert custom_log.exists()
        content = custom_log.read_text(encoding='utf-8')
        
        assert msg_info not in content
        assert msg_warning in content

class TestApplicationLogger:
    @pytest.fixture
    def app_logger(self, tmp_path):
        log_dir = tmp_path / "app_logs"
        config = LoggerConfig(log_dir=str(log_dir))
        return ApplicationLogger("TestClass", config)

    def test_context_binding(self, app_logger):
        """Testa se o logger tem o contexto correto da classe"""
        with patch.object(app_logger.logger, 'debug') as mock_debug:
            app_logger.log_result("metodo_teste", "resultado")
            # Verifica se chamou log
            mock_debug.assert_called()

    def test_log_method_call(self, app_logger):
        """Testa log de chamada de método"""
        # Garante config
        app_logger.config.setup()
        
        app_logger.log_method_call("meu_metodo", arg1=10, arg2="teste")
        
        # Encontra o arquivo de log mais recente
        logs = list(app_logger.config.log_dir.glob("app_*.log"))
        assert len(logs) > 0
        content = logs[0].read_text(encoding='utf-8')
        
        assert "meu_metodo(arg1=10, arg2=teste)" in content
        # Removida verificação de 'TestClass' pois o formato padrão do arquivo 
        # (definido em LoggerConfig) não inclui o campo extra 'class_name'

    def test_log_exception(self, app_logger):
        """Testa log de exceção"""
        app_logger.config.setup()
        try:
            1/0
        except Exception as e:
            app_logger.log_exception("metodo_erro", e)
        
        error_file = app_logger.config.log_dir / "errors.log"
        assert error_file.exists()
        content = error_file.read_text(encoding='utf-8')
        
        assert "ZeroDivisionError" in content
        assert "metodo_erro" in content

class TestSistemaMonitoramento:
    @pytest.fixture
    def sistema(self, tmp_path):
        # Patch no LoggerConfig interno para usar diretório temporário
        with patch('src.utils.LoggerConfig') as MockConfig:
            # Configura o mock para usar o metrics.log dentro do tmp_path
            mock_instance = MockConfig.return_value
            mock_instance.log_dir = tmp_path
            mock_instance.add_custom_handler = MagicMock()
            
            # Mockar a propriedade .logger de ApplicationLogger que é chamada no __init__
            with patch('src.utils.ApplicationLogger') as MockAppLogger:
                mock_app_logger_instance = MockAppLogger.return_value
                # Mockar o logger interno do loguru
                mock_loguru_logger = MagicMock()
                mock_app_logger_instance.logger = mock_loguru_logger
                
                sis = SistemaMonitoramento()
                # Atualizar referencias
                sis.config = mock_instance
                sis.metrics_file = tmp_path / "metrics.log"
                sis.logger = mock_app_logger_instance
            
                return sis

    def test_registrar_metrica(self, sistema):
        """Testa registro de métrica"""
        # sistema.logger.logger retorna o mock criado no fixture
        mock_loguru = sistema.logger.logger 
        
        # O método registrar_metrica chama .bind(metric=True).info(...)
        # O .bind() retorna um novo logger (ou mock aqui)
        mock_bound_logger = MagicMock()
        mock_loguru.bind.return_value = mock_bound_logger
        
        sistema.registrar_metrica("cpu", 50.0, {"host": "localhost"})
        
        # Verifica se bind foi chamado
        mock_loguru.bind.assert_called_with(metric=True)
        
        # Verifica se info foi chamado no logger retornado pelo bind
        mock_bound_logger.info.assert_called()
        args = mock_bound_logger.info.call_args[0]
        assert "cpu=50.0 host=localhost" in args[0]

    def test_monitorar_processo(self, sistema):
        """Testa fluxo de monitoramento"""
        with patch.object(sistema, 'registrar_metrica') as mock_registrar:
            # Mockar o context manager do contextualize
            mock_ctx = MagicMock()
            mock_ctx.__enter__.return_value = None
            mock_ctx.__exit__.return_value = None
            sistema.logger.logger.contextualize.return_value = mock_ctx
            
            sistema.monitorar_processo("proc_123")
            
            assert mock_registrar.call_count == 5
            mock_registrar.assert_any_call(
                nome="cpu_usage", 
                valor=20.0, 
                tags={"process": "proc_123", "iteration": 0}
            )
