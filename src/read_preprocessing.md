# Documentação da Arquitetura: `preprocessing.py`

Este documento descreve a estrutura, funcionamento e a lógica do script de pré-processamento de dados (`src/preprocessing.py`) do projeto.

## 1. Visão Geral

O script `preprocessing.py` é responsável pelo pipeline ETL (Extract, Transform, Load) do projeto. Ele consome planilhas Excel "cruas" (Raw Data), aplica regras de negócio para limpeza e padronização, gera novas features (Engenharia de Recursos) e prepara o dataset final para uso em modelos de Machine Learning.

**Fluxo de Execução:**
1.  **Leitura**: Carrega abas específicas (anos 2022, 2023, 2024) do arquivo Excel principal.
2.  **Tratamento**: Padroniza nomes de colunas, converte tipos, limpa formatos numéricos (PT-BR) e trata datas.
3.  **Unificação**: Concatena os dados de diferentes anos em um único DataFrame histórico.
4.  **Feature Engineering**: Cria variáveis de delta (evolução do aluno) e normaliza indicadores chave.
5.  **ML Preparation**: Imputa valores nulos e aplica One-Hot Encoding para variáveis categóricas.
6.  **Saída**: Salva arquivos intermediários (`df_tratado_ANO.csv`) e o arquivo final pronto para o modelo (`df_model_ready.csv`).

---

## 2. Classes e Componentes

### 2.1 Class `LeituraArquivos`

Responsável exclusivamente pela ingestão de dados.

*   **`__init__(self, caminho, aba="")`**: Configura o caminho do arquivo e a aba (se Excel). Inicializa o logger.
*   **`ler_arquivo(self) -> pd.DataFrame`**:
    *   Verifica a existência do arquivo.
    *   Suporta formatos `.csv` e `.xlsx`.
    *   Adiciona automaticamente a coluna `ano_referencia` com base no nome da aba (ex: "PEDE2024" -> "2024").
    *   Utiliza a engine `openpyxl` para leitura de Excel.

### 2.2 Class `TratamentoDados`

O "coração" da limpeza de dados. Encapsula as regras de negócio para transformar dados brutos em dados estruturados.

*   **Atributos de Configuração:**
    *   `DICTIONARY_MAPPING`: Mapeia variações de nomes de colunas (ex: "Data de Nasc", "Data de Nas") para um nome padrão ("data_nascimento").
    *   `COLUNAS_DECIMAIS`: Lista de colunas que precisam de conversão de formato numérico brasileiro (ex: "1.234,56" -> 1234.56).
    *   `SCHEMA_DTYPES`: Define explicitamente o tipo de dados esperado para cada coluna (float, int, str).

*   **`executar_tratamento(self) -> pd.DataFrame`**: Método fachada que orquestra a chamada sequencial de todos os métodos privados de limpeza.

*   **Métodos Privados de Limpeza:**
    *   `_remover_colunas_duplicadas`: Remove colunas com nomes repetidos ou conteúdo idêntico.
    *   `_padronizar_colunas`: Renomeia as colunas usando o `DICTIONARY_MAPPING`.
    *   `_converter_decimal_ptbr`: Corrige pontuação de milhar e vírgula decimal.
    *   `_converter_colunas_data`: Tenta converter datas usando formato Brasil (dia/mês), com fallback para formato US se falhar.
    *   `_converter_tipos`: Força o cast das colunas para os tipos definidos no schema.
    *   `_tratar_campo_parametrizado`: Calcula campos derivados como `idade` (baseado no ano de nascimento) e padroniza `genero` e `pedra`.

### 2.3 Class `DataPreprocessor` (Scikit-Learn Compliant)

Uma classe que segue a interface do Scikit-Learn (`BaseEstimator`, `TransformerMixin`), facilitando a integração com pipelines de ML.

*   **Objetivo**: Transformar o DataFrame limpo em uma matriz numérica sem nulos, pronta para algoritmos.
*   **`fit(self, X, y=None)`**:
    *   Identifica automaticamente colunas numéricas e categóricas.
    *   Configura pipelines de transformação separados:
        *   **Numéricos**: Imputação pela mediana + `StandardScaler`.
        *   **Categóricos**: Imputação constante ("missing") + `OneHotEncoder`.
*   **`transform(self, X)`**: Aplica as transformações aprendidas no `fit` e retorna um DataFrame com nomes de colunas preservados.

---

## 3. Funções Auxiliares

### `clean_data(df)`
Remove colunas que não agregam valor preditivo ou contêm PII (Informação Pessoal Identificável), como nomes, RAs e instituições específicas de anos passados.

### `create_features(df)`
Gera inteligência adicional sobre os dados:
*   **Deltas**: Calcula a evolução do índice INDE entre anos (`DELTA_INDE_21_22`).
*   **Unificação**: Preenche indicadores chave (`inde`, `pedra`, `iaa`) mesclando colunas dispersas.
*   **Binarização**: Converte respostas "Sim/Não" em 1/0.
*   **Label Encoding Manual**: Transforma a variável ordinal "Pedra" em números (Quartzo=1, Ágata=2, etc.) para manter a hierarquia.

---

## 4. Orquestração (`__main__`)

O bloco principal do script coordena todo o processo:
1.  Define diretórios de entrada (`arquivos/`) e saída (`src/arquivo_tratado/`).
2.  Itera sobre os anos de interesse (2022, 2023, 2024).
3.  Instancia `LeituraArquivos` e `TratamentoDados` para cada ano.
4.  Concatena os resultados.
5.  Chama `create_features` no dataset unificado.
6.  Chama `DataPreprocessor` para gerar a versão final (`df_model_ready.csv`).
7.  Utiliza um sistema de logs (`src.utils.ApplicationLogger`) para monitorar o progresso e erros.
