
 
import sys
import os
from loguru import logger
import pandas as pd
import joblib
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from src.utils import LoggerConfig, ApplicationLogger

class FileUtils:
    def __init__(self, name: str = "LeituraArquivos", caminho: str = "data/", aba: str = ""):
        self.config = LoggerConfig(app_name=name, log_dir=f"logs/{name.lower()}")
        self.logger = ApplicationLogger(self.__class__.__name__, self.config)
        self.logger.logger.info(f"Aplicação {name} inicializada")
        self.caminho = caminho
        self.aba = aba
        
    def ler_arquivo(self) -> pd.DataFrame:
        self.logger.log_method_call("ler_arquivo", caminho=self.caminho, aba=self.aba)
        self.logger.logger.info(f"Verificando existência do arquivo: {self.caminho} / {self.aba}")
        if not os.path.exists(self.caminho):
            self.logger.logger.error(f"Arquivo não encontrado: {self.caminho} / {self.aba}") 
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho} / {self.aba}")
        
        self.logger.logger.info(f"Iniciando leitura de itens")

        if self.caminho.endswith('.xlsx'):
            df = pd.read_excel(self.caminho, sheet_name=self.aba, engine="openpyxl")
            df['ano_referencia'] = self.aba.replace("PEDE", "")
    
    def save_model(self, model, filepath: str):
        """
        Salva o modelo treinado em disco.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(model, filepath)
        self.logger.logger.info(f"Modelo salvo em {filepath}")


    def load_model(self, filepath: str):
        """
        Carrega um modelo treinado do disco.
        """
        if not os.path.exists(filepath):
            self.logger.logger.error(f"Modelo não encontrado em: {filepath}")
            raise FileNotFoundError(f"Modelo não encontrado em: {filepath}")
        
        model = joblib.load(filepath)
        self.logger.logger.info(f"Modelo carregado de {filepath}")
        return model


