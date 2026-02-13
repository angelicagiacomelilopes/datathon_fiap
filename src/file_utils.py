
 
import sys
import os
from loguru import logger
import pandas as pd
import joblib
import numpy as np

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from src.utils import LoggerConfig, ApplicationLogger

class FileUtils:
    def __init__(self, name: str = "LeituraArquivos", caminho: str = "data/", aba: str = ""):
        """
        Inicializa a aplicação
        
        Args:
            name: Nome da aplicação
            caminho: Caminho padrão para os arquivos
        """
        # Configuração do logger
        self.config = LoggerConfig(
            app_name=name,
            log_dir=f"logs/{name.lower()}"
        )
        
        self.logger = ApplicationLogger(self.__class__.__name__, self.config)
        
        self.logger.logger.info(f"Aplicação {name} inicializada")
        self.caminho = caminho
        self.aba = aba
        
    def ler_arquivo(self) -> pd.DataFrame:
        """
        Lê um arquivo CSV ou Excel e retorna um DataFrame
        
        Args:
            caminho: Caminho do arquivo a ser lido
            
        Returns:
            DataFrame com os dados lidos
        """
        
        self.logger.log_method_call("ler_arquivo", caminho=self.caminho, aba=self.aba)
        self.logger.logger.info(f"Verificando existência do arquivo: {self.caminho} / {self.aba}")
        if not os.path.exists(self.caminho):
            self.logger.logger.error(f"Arquivo não encontrado: {self.caminho} / {self.aba}") 
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho} / {self.aba}")
        
        self.logger.logger.info(f"Iniciando leitura de itens")

        if self.caminho.endswith('.xlsx'):
            df = pd.read_excel(self.caminho, sheet_name=self.aba, engine="openpyxl")
            df['ano_referencia'] = self.aba.replace("PEDE", "")  # Extrai o ano da aba, ex: "PEDE2022" -> "2022"
        else:
            self.logger.logger.error(f"Formato de arquivo não suportado: {self.caminho} / {self.aba}")
            raise ValueError("Formato de arquivo não suportado. Use .xlsx ou .csv")

        self.logger.logger.info(f"Dados carregados com sucesso do arquivo {self.caminho} / {self.aba}.Shape: {df.shape}. Colunas: {df.columns.tolist()}")
        print(df.head(5))
        return df
    
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


class TratamentoDados:

    # Schema de mapeamento dos nomes de colunas (Variações -> Nome Padrão do Dicionário)
    # Estrutura: "Nome Padrão": ["Variação 1", "Variação 2", ...]
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

    # --- Schema de Dados para o Pipeline PEDE ---

    # Lista de colunas que contêm valores numéricos formatados com vírgula (padrão BR)
    COLUNAS_DECIMAIS = [
        'inde_2024', 'inde_23', 'inde_22', 'inde',
        'cg', 'cf', 'ct', 
        'iaa', 'ieg', 'ips', 'ipp', 'ida', 'ipv', 'ian', 
        'matematica', 'portugues', 'ingles'
    ]

    # Colunas que devem ser parseadas como data
    COLUNAS_DATA = ['Data de Nasc','Data de Nas','data_nascimento']

    # Dicionário de tipos para carregamento otimizado (evita inferência errada)
    SCHEMA_DTYPES = {
        'ra': str,                 # ID como string para evitar perda de zeros à esquerda se houver
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

    def __init__(self, df: pd.DataFrame, name: str = "TratamentoDados", ano: str = ""):
        """
        Inicializa a aplicação
        
        Args:
            df: DataFrame a ser tratado
            name: Nome da aplicação
            ano: Ano do DataFrame
        """
        # Configuração do logger
        self.config = LoggerConfig(
            app_name=name,
            log_dir=f"logs/{name.lower()}"
        )
        
        self.logger = ApplicationLogger(self.__class__.__name__, self.config)
        self.df = df
        self.ano = ano
        
        self.logger.logger.info(f"Aplicação {name} inicializada para o ano {ano}")

    def executar_tratamento(self) -> pd.DataFrame:
        """
        Executa o pipeline completo de tratamento de dados.
        Returns:
            DataFrame tratado.
        """
        self.logger.logger.info("Iniciando pipeline de tratamento de dados.")
        
        self._remover_colunas_duplicadas()
        self._padronizar_colunas()
        self._converter_decimal_ptbr()
        self._converter_colunas_data()
        self._converter_tipos()
        self._tratar_campo_parametrizado(['idade', 'genero'])
        self._ordenar_colunas()

        # salva o DataFrame tratado para conferência (opcional)
        self.df.to_csv(f"C:\\Users\\Angélica\\Desktop\\datathon\\projeto_datathon\\src\\logs\\tratamentodados\\df_tratado_{self.ano}.csv", index=False)


        # Aqui você pode adicionar outros métodos de tratamento conforme necessário
        # Ex: self._tratar_valores_nulos()
        # Ex: self._converter_tipos()

        # Exibe as colunas após padronização (opcional)
        # self.logger.logger.info(f"Colunas após padronização: {self.df.columns.tolist()}")

        return self.df
 
    def _remover_colunas_duplicadas(self):
        """
        Remove colunas duplicadas de um DataFrame.
        Se houver colunas com o mesmo nome (ex: 'Ativo/ Inativo', 'Ativo/ Inativo.1'),
        mantém apenas a primeira ocorrência.
        """
        # Identifica colunas duplicadas (pelo nome original ou pandas sufixos)
        self.df = self.df.loc[:, ~self.df.columns.duplicated()]
        self.logger.logger.info(f"Colunas após remoção de duplicatas exatas: {self.df.shape[1]}")

 
        seen = set()
        cols_to_drop = []
        
        for i, col in enumerate(self.df.columns):
            nome_base = col.split('.')[0] # Remove sufixo .1, .2 gerado pelo pandas
            
            if nome_base in seen and col != nome_base:
                # Verifica se o conteúdo é igual ao original
                if self.df[nome_base].equals(self.df[col]):
                    cols_to_drop.append(col)
                    self.logger.logger.info(f"Coluna duplicada removida: {col} (cópia idêntica de {nome_base})")
                else:
                    self.logger.logger.warning(f"Aviso: Coluna {col} tem nome similar a {nome_base} mas conteúdo diferente. Mantida.")
            else:
                seen.add(nome_base)
                
        if cols_to_drop:
            self.logger.logger.info(f"Removendo {len(cols_to_drop)} colunas duplicadas: {cols_to_drop}")
            self.df = self.df.drop(columns=cols_to_drop)

        # Apenas para log statistics
        nomes_limpos = [col.split('.')[0] for col in self.df.columns]
        from collections import Counter
        contagem = Counter(nomes_limpos)
        for coluna, qtd in contagem.items():
            if qtd > 1:
                self.logger.logger.info(f" - '{coluna}': {qtd} ocorrências")

    def _padronizar_colunas(self):
        """
        Renomeia colunas do DF baseado no mapping definido na classe.
        """
        self.logger.logger.info("Iniciando padronização de colunas com base no dicionário de mapeamento.")
        col_map = {}
        # O mapping está na estrutura: "Nome Padrão": ["var1", "var2"]
        # Queremos: {"var1": "Nome Padrão", "var2": "Nome Padrão"}
        
        for padrao, variacoes in self.DICTIONARY_MAPPING['columns'].items():
            for var in variacoes:
                if var in self.df.columns:
                    col_map[var] = padrao
        
        if col_map:
            self.df = self.df.rename(columns=col_map)
            self.logger.logger.info(f"{len(col_map)} colunas renomeadas.")
            self.logger.logger.info(f"Colunas renomeadas: {col_map}")
        else:
            self.logger.logger.info("Nenhuma coluna precisou ser renomeada.")


    def _converter_valor_decimal(self, valor):
        """
        Função auxiliar para converter valor individual.
        """
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
        """
        Converte strings numéricas no formato PT-BR (1.000,00) para float Python.
        Trata valores nulos e erros como NaN.
        """
        self.logger.logger.info("Iniciando conversão de colunas decimais no formato PT-BR.")
        
        # Filtra apenas as colunas que existem no DataFrame atual
        cols_presentes = [col for col in self.COLUNAS_DECIMAIS if col in self.df.columns]
        
        if not cols_presentes:
            self.logger.logger.info("Nenhuma coluna decimal encontrada para conversão.")
            return

        self.logger.logger.info(f"Convertendo {len(cols_presentes)} colunas: {cols_presentes}")
        
        # Iterar sobre colunas para aplicar a conversão de forma segura
        for col in cols_presentes:
            self.df[col] = self.df[col].apply(self._converter_valor_decimal)
       

    def _converter_colunas_data(self):
        """
        Converte colunas de data para o formato datetime do pandas.
        Trata erros de conversão como NaT.
        Tenta formato BR (dia/mês) primeiro, e faz fallback para US (mês/dia) se falhar.
        """
        self.logger.logger.info("Iniciando conversão de colunas de data.")
        
        # Filtra apenas as colunas que existem no DataFrame atual
        cols_presentes = [col for col in self.COLUNAS_DATA if col in self.df.columns]
        
        if not cols_presentes:
            self.logger.logger.info("Nenhuma coluna de data encontrada para conversão.")
            return

        self.logger.logger.info(f"Convertendo {len(cols_presentes)} colunas: {cols_presentes}")
        
        for col in cols_presentes:
            # Salva valores originais para verificar o que falhou
            original_values = self.df[col].copy()
            
            # 1ª Tentativa: Forçando formato dia/mês (BR)
            try:
                dates_br = pd.to_datetime(self.df[col], errors='coerce', dayfirst=True, format='mixed')
            except ValueError:
                # Fallback para versões antigas do pandas sem format='mixed'
                dates_br = pd.to_datetime(self.df[col], errors='coerce', dayfirst=True)
            
            # Verifica onde falhou (NaT) mas o valor original não era nulo/vazio
            # Considera NaN, None, NaT como nulos
            mask_failed = dates_br.isna() & original_values.notna() & (original_values != '')
            
            items_failed = mask_failed.sum()
            if items_failed > 0:
                self.logger.logger.warning(f"Coluna '{col}': {items_failed} valores falharam na conversão BR (dia/mês). Tentando formato US (mês/dia).")
                
                # 2ª Tentativa: Para os que falharam, tenta formato US (mês/dia)
                try:
                    dates_us = pd.to_datetime(original_values[mask_failed], errors='coerce', dayfirst=False, format='mixed')
                except ValueError:
                    dates_us = pd.to_datetime(original_values[mask_failed], errors='coerce', dayfirst=False)
                
                # Preenche os buracos (NaT) da conversão BR com o sucesso da conversão US
                dates_br = dates_br.fillna(dates_us)
            
            self.df[col] = dates_br
            self.logger.logger.info(f"Coluna '{col}': conversão concluída.")

        return self.df

    def _converter_tipos(self):
        """
        Converte colunas para os tipos definidos no SCHEMA_DTYPES.
        """
        self.logger.logger.info("Iniciando conversão de tipos de colunas com base no schema definido.")
        
        for col, dtype in self.SCHEMA_DTYPES.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                    self.logger.logger.info(f"Coluna '{col}' convertida para {dtype}.")
                except Exception as e:
                    self.logger.logger.error(f"Erro ao converter coluna '{col}' para {dtype}: {e}")
            else:
                self.logger.logger.info(f"Coluna '{col}' não encontrada para conversão de tipo.")
                
                # Tenta tratar/calcular campo calculado
                self._tratar_campo_criado_parametrizado(col)
                
                # Se a coluna ainda não existir após a tentativa de tratamento, cria com NaN
                if col not in self.df.columns:
                    self.logger.logger.info(f"Coluna não calculada, criada com valor NaN: '{col}'")
                    self.df[col] = np.nan  # Cria a coluna com NaN


        self.logger.logger.info("Conversão de tipos concluída.")

    def _tratar_campo_criado_parametrizado(self, campo: str):
        """
        Método para tratar/calcular campos específicos que não vieram no arquivo original.
        """
        # Caso: ano_nasc não existe, mas data_nascimento existe
        if campo == 'ano_nasc' and 'data_nascimento' in self.df.columns:
            if self.df['data_nascimento'].notna().any():
                self.logger.logger.info(f"Calculando '{campo}' a partir de 'data_nascimento'")
                # Se for datetime
                if pd.api.types.is_datetime64_any_dtype(self.df['data_nascimento']):
                    self.df[campo] = self.df['data_nascimento'].dt.year # Usa Int64 para permitir NaNs
                else:
                    # Tenta converter string pra extrair ano
                    self.df[campo] = pd.to_datetime(self.df['data_nascimento'], errors='coerce').dt.year
                
                self.logger.logger.info(f"Campo '{campo}' preenchido.")
            else:
                self.logger.logger.warning(f"Campo 'data_nascimento' vazio. '{campo}' será NaN.")

        # Caso: data_nascimento não existe, mas ano_nasc existe
        elif campo == 'data_nascimento' and 'ano_nasc' in self.df.columns:
            if self.df['ano_nasc'].notna().any():
                self.logger.logger.info(f"Calculando '{campo}' a partir de 'ano_nasc'")
                # Assume 01/01/Ano
                self.df[campo] = self.df['ano_nasc'].apply(
                    lambda x: pd.to_datetime(f"{int(float(x))}-01-01", errors='coerce') if pd.notna(x) else pd.NaT
                )
                self.logger.logger.info(f"Campo '{campo}' preenchido.")
            else:
                self.logger.logger.warning(f"Campo 'ano_nasc' vazio. '{campo}' será NaN.")

    def _ordenar_colunas(self):
        """
        Ordena as colunas do DataFrame em ordem alfabética.
        Isso garante que todos os DataFrames tenham a mesma estrutura de colunas ao final.
        """
        self.logger.logger.info("Ordenando colunas em ordem alfabética.")
        self.df = self.df.reindex(sorted(self.df.columns), axis=1)

    def _tratar_campo_parametrizado(self, campo_lista: list):
        for campo in campo_lista:
            # caso o campo idade seja nulo, faz o calculo pelo ano_nasc ou data_nascimento
            if campo == 'idade':
                if 'ano_nasc' in self.df.columns and self.df['ano_nasc'].notna().any():
                    self.logger.logger.info("Calculando 'idade' a partir de 'ano_nasc'")
                    
                    # Converte para numérico forçando NaN em caso de erro
                    ano_ref = pd.to_numeric(self.df['ano_referencia'], errors='coerce')
                    ano_nasc = pd.to_numeric(self.df['ano_nasc'], errors='coerce')
                    
                    self.df['idade'] = ano_ref - ano_nasc
                    self.logger.logger.info("Campo 'idade' preenchido a partir de 'ano_nasc'.")
                else:
                    self.logger.logger.warning("Campos 'ano_nasc' e 'data_nascimento' vazios. 'idade' será NaN.")

            if campo == 'genero':
                # padroniza gênero para Masculino, Feminino, Menino e Menina
                if 'genero' in self.df.columns:
                    self.logger.logger.info("Padronizando campo 'genero'")
                    self.df['genero'] = self.df['genero'].str.strip().str.lower()
                    self.df['genero'] = self.df['genero'].replace({
                        'masculino': 'Masculino',
                        'feminino': 'Feminino',
                        'menino': 'Masculino',
                        'menina': 'Feminino'
                    })
                    self.logger.logger.info("Campo 'genero' padronizado.")
                else:
                    self.logger.logger.warning("Campo 'genero' não encontrado para padronização.")


if __name__ == "__main__": # pragma: no cover    
    caminho="C:\\Users\\Angélica\\Desktop\\datathon\\projeto_datathon\\arquivos\\BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
    
    print("--- Carregando 2022 ---")
    leitura = FileUtils(caminho=caminho, aba="PEDE2022")
    df_2022 = leitura.ler_arquivo()

    if df_2022 is not None:
        print(f"Primeira etapa:{df_2022['Ano nasc']}")
        tratamento_2022 = TratamentoDados(df_2022, ano="2022")
        df_2022_tratado = tratamento_2022.executar_tratamento()
        print(df_2022_tratado.head(10))

    print("\n--- Carregando 2023 ---")
    leitura = FileUtils(caminho=caminho, aba="PEDE2023")
    df_2023 = leitura.ler_arquivo()
    if df_2023 is not None:
        tratamento_2023 = TratamentoDados(df_2023, ano="2023") 
        df_2023_tratado = tratamento_2023.executar_tratamento()
        print(df_2023_tratado.head(10))
 
    print("\n--- Carregando 2024 ---")
    leitura = FileUtils(caminho=caminho, aba="PEDE2024")
    df_2024 = leitura.ler_arquivo()
    if df_2024 is not None:
        tratamento_2024 = TratamentoDados(df_2024, ano="2024")
        df_2024_tratado = tratamento_2024.executar_tratamento()
        print(df_2024_tratado.head(10))

    # concatenar os DataFrames tratados
    df_concatenado = pd.concat([df_2022_tratado, df_2023_tratado, df_2024_tratado], ignore_index=True)
    print("\n--- DataFrame Concatenado ---")   
    print(df_concatenado.head(10))

    # # salva o DataFrame tratado para conferência (opcional)
    df_concatenado.to_csv(f"C:\\Users\\Angélica\\Desktop\\datathon\\projeto_datathon\\src\\logs\\tratamentodados\\df_tratado_concatenado.csv", index=False)
    # mostrar o total de linhas de cada DataFrame para conferência
    print("Total 2022 :", len(df_2022))
    print("Total 2023  :", len(df_2023))
    print("Total 2024  :", len(df_2024))
    print("Total 2022 tratado :", len(df_2022_tratado))
    print("Total 2023 tratado :", len(df_2023_tratado))
    print("Total 2024 tratado :", len(df_2024_tratado))
    print("Total concatenado :", len(df_concatenado))