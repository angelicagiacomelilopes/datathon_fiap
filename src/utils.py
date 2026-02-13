from loguru import logger
import sys
import os
from typing import Optional, Dict, Any
from pathlib import Path
import pandas as pd


class LoggerConfig:
    """Classe para configuração do logger da aplicação"""
    
    def __init__(self, 
                 app_name: str = "App",
                 log_dir: str = "logs",
                 console_level: str = "INFO",
                 file_level: str = "DEBUG",
                 error_level: str = "ERROR"):
        """
        Inicializa a configuração do logger
        
        Args:
            app_name: Nome da aplicação para identificação nos logs
            log_dir: Diretório onde os logs serão salvos
            console_level: Nível de log para console
            file_level: Nível de log para arquivo geral
            error_level: Nível de log para arquivo de erros
        """
        self.app_name = app_name
        self.log_dir = Path(log_dir)
        self.console_level = console_level
        self.file_level = file_level
        self.error_level = error_level
        
        # Cria o diretório de logs se não existir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_console_format(self) -> str:
        """Retorna o formato para logs no console"""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            f"<cyan>{self.app_name}</cyan>:<cyan>{{name}}</cyan>:<cyan>{{function}}</cyan>:<cyan>{{line}}</cyan> | "
            "<level>{message}</level>"
        )
    
    def _get_file_format(self) -> str:
        """Retorna o formato para logs em arquivo"""
        return (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level} | "
            f"{self.app_name}:{{name}}:{{function}}:{{line}} | "
            "{message}"
        )
    
    def setup(self) -> None:
        """Configura os handlers do logger"""
        # Remove handlers existentes
        logger.remove()
        
        # Handler para console
        logger.add(
            sys.stdout,
            format=self._get_console_format(),
            level=self.console_level,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
        
        # Handler para arquivo geral
        logger.add(
            self.log_dir / "app_{time:YYYY-MM-DD}.log",
            format=self._get_file_format(),
            level=self.file_level,
            rotation="00:00",  # Rotação diária à meia-noite
            retention="30 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        # Handler para arquivo de erros
        logger.add(
            self.log_dir / "errors.log",
            format=self._get_file_format(),
            level=self.error_level,
            rotation="500 MB",
            retention="90 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        logger.info(f"Logger configurado para aplicação: {self.app_name}")
        logger.debug(f"Diretório de logs: {self.log_dir.absolute()}")
    
    def add_custom_handler(self, 
                          sink: Any,
                          level: str = "INFO",
                          format_str: Optional[str] = None,
                          **kwargs) -> int:
        """
        Adiciona um handler personalizado ao logger
        
        Args:
            sink: Destino do log (arquivo, stream, etc.)
            level: Nível de log
            format_str: Formato personalizado (opcional)
            **kwargs: Argumentos adicionais para logger.add()
            
        Returns:
            ID do handler adicionado
        """
        if format_str is None:
            format_str = self._get_file_format()
            
        return logger.add(
            sink=sink,
            format=format_str,
            level=level,
            **kwargs
        )


class ApplicationLogger:
    """Logger específico para aplicação com contexto"""
    
    def __init__(self, class_name: str, config: Optional[LoggerConfig] = None):
        """
        Inicializa o logger da aplicação
        
        Args:
            class_name: Nome da classe que usa o logger
            config: Configuração do logger (opcional)
        """
        self.class_name = class_name
        self.config = config or LoggerConfig()
        
        if not logger._core.handlers:
            self.config.setup()
        
        # Cria um logger com contexto
        self._logger = logger.bind(class_name=class_name)
    
    @property
    def logger(self):
        """Retorna o logger configurado"""
        return self._logger
    
    def log_method_call(self, method_name: str, **kwargs) -> None:
        """Registra a chamada de um método com parâmetros"""
        params_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        self.logger.debug(f"{method_name}({params_str})")
    
    def log_result(self, method_name: str, result: Any) -> None:
        """Registra o resultado de um método"""
        self.logger.debug(f"{method_name} -> {result}")
    
    def log_exception(self, method_name: str, exception: Exception) -> None:
        """Registra uma exceção com traceback"""
        self.logger.opt(exception=True).error(
            f"Exceção em {method_name}: {exception}"
        )
    
    def time_execution(self, operation_name: str):
        """
        Context manager para medir tempo de execução
        
        Args:
            operation_name: Nome da operação a ser cronometrada
            
        Returns:
            Context manager para medição de tempo
        """
        return self._logger.contextualize(operation=operation_name)


class SistemaMonitoramento:
    """Sistema de monitoramento com logging avançado"""
    
    def __init__(self):
        """Inicializa o sistema de monitoramento"""
        self.config = LoggerConfig(
            app_name="SistemaMonitoramento",
            log_dir="logs/monitoramento",
            console_level="WARNING",
            file_level="INFO"
        )
        
        self.logger = ApplicationLogger(self.__class__.__name__, self.config)
        
        # Adiciona handler para métricas
        self.metrics_file = self.config.log_dir / "metrics.log"
        self.metrics_handler_id = self.config.add_custom_handler(
            sink=self.metrics_file,
            level="INFO",
            format_str="{time:YYYY-MM-DD HH:mm:ss} | METRIC | {message}",
            filter=lambda record: "metric" in record["extra"]
        )
        
        self.logger.logger.info("Sistema de monitoramento inicializado")
    
    def registrar_metrica(self, nome: str, valor: float, tags: Dict[str, Any] = None):
        """Registra uma métrica no sistema"""
        tags_str = " ".join(f"{k}={v}" for k, v in (tags or {}).items())
        mensagem = f"{nome}={valor} {tags_str}"
        
        # Usa bind para marcar como métrica
        self.logger.logger.bind(metric=True).info(mensagem)
    
    def monitorar_processo(self, processo_id: str):
        """Monitora um processo específico"""
        with self.logger.logger.contextualize(processo_id=processo_id):
            self.logger.logger.info(f"Iniciando monitoramento do processo {processo_id}")
            
            # Simulação de métricas
            for i in range(5):
                self.registrar_metrica(
                    nome="cpu_usage",
                    valor=20.0 + i * 5,
                    tags={"process": processo_id, "iteration": i}
                )
            
            self.logger.logger.info(f"Monitoramento do processo {processo_id} concluído")

 
