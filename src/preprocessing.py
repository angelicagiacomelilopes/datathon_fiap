import sys
import os
import logging
import traceback
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

try:
    from src.utils import LoggerConfig, ApplicationLogger
    HAS_LOGGER = True
except ImportError:
    HAS_LOGGER = False

class LeituraArquivos:
    def __init__(self, caminho, aba=""):
        self.caminho = caminho
        self.aba = aba
        self._setup_logger()

    def _setup_logger(self):
        if HAS_LOGGER:
            try:
                config = LoggerConfig(app_name="DataLoading", log_dir="logs/leitura")
                self.logger = ApplicationLogger(self.__class__.__name__, config).logger
                return
            except Exception:
                pass
        
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)

    def ler_arquivo(self) -> pd.DataFrame:
        if not os.path.exists(self.caminho):
            self.logger.error(f"Arquivo não existente: {self.caminho}") 
            raise FileNotFoundError(f"Arquivo não existente: {self.caminho}")

        try:
            if self.caminho.endswith('.xlsx'):
                df = pd.read_excel(self.caminho, sheet_name=self.aba, engine="openpyxl")
                if "PEDE" in self.aba:
                    df['ano_referencia'] = self.aba.replace("PEDE", "")
            elif self.caminho.endswith('.csv'):
                df = pd.read_csv(self.caminho)
            else:
                self.logger.error("Formato inválido")
                return None
                
            self.logger.info(f"Leitura: {self.aba} ({len(df)} rows)")
            return df

        except Exception as e:
            self.logger.error(f"Erro leitura: {e}")
            return None

 
class TratamentoDados:
    
    # ... (Schema e constantes mantidos como estão) ...
    DICTIONARY_MAPPING = {
        "columns": {
            "ano_ingresso": ["Ano ingresso"],
            "ano_nasc": ["Ano nasc"],
            "data_nascimento": ["Data de Nasc","Data de Nas"],
            "atingiu_pv": ["Atingiu PV"],
            "avaliador_1": ["Avaliador1"],
            "avaliador_2": ["Avaliador2"],
            "avaliador_3": ["Avaliador3"],
            "avaliador_4": ["Avaliador4"],
            "avaliador_5": ["Avaliador5"],
            "avaliador_6": ["Avaliador6"],
            "cf": ["Cf"],
            "cg": ["Cg"],
            "ct": ["Ct"],
            "defasagem": ["Defas", "Defasagem"],
            "destaque_ida": ["Destaque IDA"],
            "destaque_ieh": ["Destaque IEG"],
            "destaque_ipv": ["Destaque IPV"],
            "escola": ["Escola"],
            "fase": ["Fase"],
            "fase_ideal": ["Fase ideal", "Fase Ideal"],
            "genero": ["Gênero"],
            "iaa": ["IAA"],
            "ian": ["IAN"],
            "ida": ["IDA"],
            "idade": ["Idade 22", "Idade"],
            "ieg": ["IEG"],
            "inde_22": ["INDE 22"],
            "inde_23": ["INDE 23"],
            "inde_2023": ["INDE 2023"],
            "inde_2024": ["INDE 2024"], 
            "indicado": ["Indicado"],
            "ingles": ["Inglês", "Ing"],
            "instituicao_de_ensino": ["Instituição de ensino"],
            "ipp": ["IPP"],
            "ips": ["IPS"],
            "ipv": ["IPV"],
            "matematica": ["Matem", "Mat"],
            "nome_anonimizado": ["Nome", "Nome Anonimizado"],
            "num_av": ["Nº Av"],
            "pedra_20": ["Pedra 20"],
            "pedra_21": ["Pedra 21"],
            "pedra_22": ["Pedra 22"],
            "pedra_23": ["Pedra 23"],
            "pedra_2023": ["Pedra 2023"],
            "pedra_2024": ["Pedra 2024"],
            "portugues": ["Portug", "Por"],
            "ra": ["RA"],
            "rec_av1": ["Rec Av1"],
            "rec_av2": ["Rec Av2"],
            "rec_av3": ["Rec Av3"],
            "rec_av4": ["Rec Av4"],
            "rec_psicologia": ["Rec Psicologia"],
            "turma": ["Turma"],
            "ativo_inativo": ["Ativo/ Inativo"],
            "ano_referencia": ["ano_referencia"]
        }
    }

    # Lista de colunas que contêm valores numéricos formatados com vírgula (padrão BR)
    COLUNAS_DECIMAIS = [
        'inde_2024', 'inde_23', 'inde_22', 'inde',
        'cg', 'cf', 'ct', 
        'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian', 
        'matematica', 'portugues', 'ingles'
    ]

    # Colunas que devem ser parseadas como data
    COLUNAS_DATA = ['Data de Nasc','Data de Nas','data_nascimento']

    # Dicionário de tipos
    SCHEMA_DTYPES = {
        'ra': str,
        'fase': str,
        'fase_ideal': str,
        'pedra_2024': str,
        'pedra_2023':str,
        'pedra_23': str,
        'pedra_22': str,
        'pedra_21': str,
        'pedra_20': str,
        'turma': str,
        'nome_anonimizado': str,
        'genero': str,
        'data_nascimento':str,
        'instituicao_de_ensino': str,
        'escola': str,
        'defasagem': float,        # Usamos float pois pode conter NaNs
        'num_av': float,
        'ano_ingresso': int,
        'idade': str,
        'ativo_inativo': str,
        'avaliador_1': str, 
        'avaliador_2': str, 
        'avaliador_3': str, 
        'avaliador_4': str, 
        'avaliador_5': str, 
        'avaliador_6': str,
        'destaque_ieh': str, 
        'destaque_ida': str, 
        'destaque_ipv': str, 
        'ano_nasc': str,
        'ano_referencia':str,
        'atingiu_pv': str,
        'cf': float,
        'cg': float,
        'ct': float,
        'iaa': float,
        'ian': float,
        'ida': float,
        'ieg': float,
        'inde_22': float,
        'inde_23': float,
        'inde_2023': float,
        'inde_2024': float, 
        'indicado': str,
        'ingles': float,
        'ipp': float,
        'ips': float,
        'ipv': float,
        'matematica': float,
        'portugues': float,
        'rec_av1': str,
        'rec_av2': str,
        'rec_av3': str,
        'rec_av4': str,
        'rec_psicologia': str,
        'ano_referencia': str
    }

    def __init__(self, df: pd.DataFrame, ano: str = ""):
        self.df = df
        self.ano = ano
        self._setup_logger()
        
    def _setup_logger(self):
        if HAS_LOGGER:
            try:
                config = LoggerConfig(app_name="DataProcessing", log_dir="logs/tratamento")
                self.logger = ApplicationLogger(self.__class__.__name__, config).logger
                return
            except Exception:
                pass
        
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO)

    def executar_tratamento(self) -> pd.DataFrame:
        self._remover_colunas_duplicadas()
        self._padronizar_colunas()
        self._converter_decimal_ptbr()
        self._converter_colunas_data()
        self._converter_tipos()
        self._tratar_campo_parametrizado(['idade', 'genero'])
        self._ordenar_colunas()
        
        self.logger.info(f"Tratamento concluído para {self.ano}")
        return self.df
 
    def _remover_colunas_duplicadas(self):
        # Identifica colunas duplicadas (pelo nome original ou pandas sufixos)
        self.df = self.df.loc[:, ~self.df.columns.duplicated()]

        seen = set()
        cols_to_drop = []
        
        for i, col in enumerate(self.df.columns):
            nome_base = col.split('.')[0] # Remove sufixo .1, .2 gerado pelo pandas
            
            if nome_base in seen and col != nome_base:
                # Verifica se o conteúdo é igual ao original
                try:
                    if self.df[nome_base].equals(self.df[col]):
                        cols_to_drop.append(col)
                except KeyError:
                     pass

            else:
                seen.add(nome_base)
                
        if cols_to_drop:
            self.logger.info(f"Removendo duplicadas: {cols_to_drop}")
            self.df = self.df.drop(columns=cols_to_drop)

    def _padronizar_colunas(self):
        col_map = {}
        
        for padrao, variacoes in self.DICTIONARY_MAPPING['columns'].items():
            for var in variacoes:
                if var in self.df.columns:
                    col_map[var] = padrao
        
        if col_map:
            self.df = self.df.rename(columns=col_map)
            self.logger.info(f"{len(col_map)} colunas renomeadas.")

    def _converter_valor_decimal(self, valor):
        if pd.isna(valor) or valor == '' or str(valor).strip() == '#N/A':
            return np.nan
            
        if isinstance(valor, (int, float)):
            return float(valor)
            
        try:
            # Remove pontos de milhar e troca vírgula decimal por ponto
            limpo = str(valor).replace('.', '').replace(',', '.')
            return float(limpo)
        except ValueError:
            return np.nan

    def _converter_decimal_ptbr(self):
        cols_presentes = [col for col in self.COLUNAS_DECIMAIS if col in self.df.columns]
        
        if not cols_presentes:
            return

        for col in cols_presentes:
            self.df[col] = self.df[col].apply(self._converter_valor_decimal)
       
    def _converter_colunas_data(self):
        cols_presentes = [col for col in self.COLUNAS_DATA if col in self.df.columns]
        
        if not cols_presentes:
            return

        for col in cols_presentes:
            original_values = self.df[col].copy()
            
            try:
                dates_br = pd.to_datetime(self.df[col], errors='coerce', dayfirst=True, format='mixed')
            except ValueError:
                dates_br = pd.to_datetime(self.df[col], errors='coerce', dayfirst=True)
            
            mask_failed = dates_br.isna() & original_values.notna() & (original_values != '')
            
            items_failed = mask_failed.sum()
            if items_failed > 0:
                self.logger.warning(f"Coluna '{col}': {items_failed} falhas na conv. BR -> tentando US.")
                
                try:
                    dates_us = pd.to_datetime(original_values[mask_failed], errors='coerce', dayfirst=False, format='mixed')
                except ValueError:
                    dates_us = pd.to_datetime(original_values[mask_failed], errors='coerce', dayfirst=False)
                
                dates_br = dates_br.fillna(dates_us)
            
            self.df[col] = dates_br

        return self.df

    def _converter_tipos(self):
        for col, dtype in self.SCHEMA_DTYPES.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                except Exception as e:
                    self.logger.error(f"Erro ao converter '{col}' para {dtype}: {e}")
            else:
                self._tratar_campo_criado_parametrizado(col)
                
                # Se a coluna ainda não existir após a tentativa de tratamento, cria com NaN
                if col not in self.df.columns:
                    self.df[col] = np.nan

    def _tratar_campo_criado_parametrizado(self, campo: str):
        if campo == 'ano_nasc' and 'data_nascimento' in self.df.columns:
            if self.df['data_nascimento'].notna().any():
                if pd.api.types.is_datetime64_any_dtype(self.df['data_nascimento']):
                    self.df[campo] = self.df['data_nascimento'].dt.year
                else:
                    self.df[campo] = pd.to_datetime(self.df['data_nascimento'], errors='coerce').dt.year

        elif campo == 'data_nascimento' and 'ano_nasc' in self.df.columns:
            if self.df['ano_nasc'].notna().any():
                self.df[campo] = self.df['ano_nasc'].apply(
                    lambda x: pd.to_datetime(f"{int(float(x))}-01-01", errors='coerce') if pd.notna(x) else pd.NaT
                )

    def _ordenar_colunas(self):
        self.df = self.df.reindex(sorted(self.df.columns), axis=1)

    def _tratar_campo_parametrizado(self, campo_lista: list):
        for campo in campo_lista:
            if campo == 'idade':
                if 'ano_nasc' in self.df.columns and self.df['ano_nasc'].notna().any():
                    ano_ref = pd.to_numeric(self.df['ano_referencia'], errors='coerce')
                    ano_nasc = pd.to_numeric(self.df['ano_nasc'], errors='coerce')
                    self.df['idade'] = ano_ref - ano_nasc

            if campo == 'genero':
                if 'genero' in self.df.columns:
                    self.df['genero'] = self.df['genero'].str.strip().str.lower()
                    self.df['genero'] = self.df['genero'].replace({
                        'masculino': 'Masculino',
                        'feminino': 'Feminino',
                        'menino': 'Masculino',
                        'menina': 'Feminino'
                    })

            if campo in ['pedra_2024', 'pedra_2023', 'pedra_23', 'pedra_22', 'pedra_21', 'pedra_20']:
                self.df[campo] = self.df[campo].str.strip().str.lower()
                self.df[campo] = self.df[campo].replace('á','a').replace('#DIV/0!', np.nan).replace('#N/A', np.nan)


class DataPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.pipeline = None
        self.numerical_cols = []
        self.categorical_cols = []

    def fit(self, X, y=None):
        # Conversão explícita de colunas categóricas para string para evitar erros de ordenação (int vs str)
        self.numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        for col in self.categorical_cols:
             X[col] = X[col].astype(str)

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        self.pipeline = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numerical_cols),
                ('cat', categorical_transformer, self.categorical_cols)
            ])
        
        X = X.copy()
        for col in self.categorical_cols:
             if col in X.columns:
                 X[col] = X[col].astype(str)
                 
        self.pipeline.fit(X, y)
        return self

    def transform(self, X):
        return pd.DataFrame(self.pipeline.transform(X), columns=self._get_feature_names())

    def _get_feature_names(self):
        output_features = []
        if 'num' in self.pipeline.named_transformers_:
             output_features.extend(self.numerical_cols)
        
        if 'cat' in self.pipeline.named_transformers_ and self.categorical_cols:
            cat_transformer = self.pipeline.named_transformers_['cat']
            onehot = cat_transformer.named_steps['onehot']
            try:
                cat_features = onehot.get_feature_names_out(self.categorical_cols)
                output_features.extend(cat_features)
            except Exception:
                pass
        return output_features


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza limpeza básica dos dados antes do processamento.
    Remove colunas irrelevantes como nomes e IDs.
    """
    df = df.copy()
    
    cols_to_drop = [
        'NOME', 'INSTITUICAO_ENSINO_ALUNO_2020', 'INSTITUICAO_ENSINO_ALUNO_2021',
        'nome_anonimizado', 'ra', 'data_nascimento'
    ]
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
    return df


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria novas features a partir dos dados existentes.
    """
    df = df.copy()
    
    # Feature Engineering: Comparação entre anos / Deltas
    if 'INDE_2021' in df.columns and 'INDE_2020' in df.columns:
        df['DELTA_INDE_20_21'] = df['INDE_2021'] - df['INDE_2020']
    
    if 'INDE_2022' in df.columns and 'INDE_2021' in df.columns:
        df['DELTA_INDE_21_22'] = df['INDE_2022'] - df['INDE_2021']

    # Unificação de colunas dispersas por ano
    colunas_base = ['inde', 'pedra', 'iaa', 'ieg', 'ips', 'ida', 'ipp', 'ipv', 'ian', 'ponto_virada']
    
    for base_col in colunas_base:
        cols_presentes = [c for c in df.columns if base_col.lower() in c.lower() and c.lower() != base_col.lower()]
        
        if cols_presentes and base_col not in df.columns:
            df[base_col] = df[cols_presentes].bfill(axis=1).iloc[:, 0]

    # Converter colunas booleanas/string para int
    for col in df.columns:
        if 'ponto_virada' in col.lower() or 'bolsista' in col.lower() or 'atingiu_pv' in col.lower():
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).apply(lambda x: 1 if x.strip().lower() in ['sim', 'true', '1', 's'] else 0)

    # Tratamento de Pedras (Label Encoding manual)
    pedra_map = {'quartzo': 1, 'ágata': 2, 'agata': 2, 'ametista': 3, 'topázio': 4, 'topazio': 4}
    for col in df.columns:
        if 'pedra' in col.lower():
            # Cria coluna numérica se não existir ou substitui
            # Assegura que está lower para o map
            if df[col].dtype == 'object':
                df[f'{col}_NUM'] = df[col].str.lower().map(pedra_map).fillna(0)
    
    return df

if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATA_DIR = PROJECT_ROOT / "arquivos"
    OUTPUT_DIR = PROJECT_ROOT / "src" / "arquivo_tratado"
    LOGS_DIR = PROJECT_ROOT / "src" / "logs" / "tratamentodados"

    # Logger
    if HAS_LOGGER:
        try:
            config = LoggerConfig(app_name="DataPipeline", log_dir=str(LOGS_DIR))
            logger = ApplicationLogger("Main", config).logger
        except:
            logger = logging.getLogger("Main")
            logging.basicConfig(level=logging.INFO)
    else:
        logger = logging.getLogger("Main")
        logging.basicConfig(level=logging.INFO)

    FILE_PATH = DATA_DIR / "BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    processed_dfs = []

    for ano in ["2022", "2023", "2024"]:
        aba = f"PEDE{ano}"
        
        try:
            leitura = LeituraArquivos(caminho=str(FILE_PATH), aba=aba)
            df_raw = leitura.ler_arquivo()
            
            if df_raw is not None:
                tratamento = TratamentoDados(df_raw, ano=ano)
                df_tratado = tratamento.executar_tratamento()
                
                out_path = OUTPUT_DIR / f"df_tratado_{ano}.csv"
                df_tratado.to_csv(out_path, index=False)
                logger.info(f"Processado {ano}: {out_path.name}")
                
                processed_dfs.append(df_tratado)
                
        except Exception as e:
            logger.error(f"Falha em {ano}: {e}")

    if processed_dfs:
        try:
            df_concatenado = pd.concat(processed_dfs, ignore_index=True)
            
            # Feature Engineering
            df_final = create_features(df_concatenado)

            final_path = OUTPUT_DIR / "df_features_final.csv"
            df_final.to_csv(final_path, index=False)
            logger.info(f"Features geradas: {final_path.name}")

            # Machine Learning Prep
            preprocessor = DataPreprocessor()
            df_model_ready = preprocessor.fit_transform(df_final)
            
            ml_path = OUTPUT_DIR / "df_model_ready.csv"
            df_model_ready.to_csv(ml_path, index=False)
            logger.info(f"Arquivo ML pronto: {ml_path.name}")
            
        except Exception as e:
            logger.error(f"Erro final: {e}")
    else:
        logger.warning("Nenhum dado processado.")


