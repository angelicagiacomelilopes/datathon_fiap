# 📊 Passos Mágicos - Predição de Evasão Escolar

Projeto de Machine Learning para identificar e prever risco de evasão escolar usando Random Forest com alto nível de acurácia (99.64%).

## 🚀 Status

- ✅ **API**: Operacional em `http://127.0.0.1:8002`
- ✅ **Modelo**: RandomForestClassifier com F1-Score CV = 0.8994
- ✅ **Dados**: Processados e normalizados
- ✅ **Endpoints**: Todos funcionando (/, /health, /info, /predict, /docs)

---

## 📁 Estrutura do Projeto

```
projeto_datathon/
│
├── app/                          # Aplicação FastAPI
│   ├── main_simple.py           # API FastAPI (ativo)
│   ├── run.py                   # Launcher do servidor
│   ├── model/                   # Artefatos do modelo
│   │   ├── model.pkl            # Modelo treinado
│   │   └── model_config.pkl     # Configuração do modelo
│   └── __init__.py
│
├── src/                          # Código-fonte principal
│   ├── model.py                 # Definição do modelo oficial
│   ├── preprocessing.py         # Pré-processamento de dados
│   ├── feature_store.py         # Gestão de features
│   ├── file_utils.py            # Utilidades de arquivo
│   ├── utils.py                 # Utilidades gerais
│   ├── requirements.txt         # Dependências Python
│   ├── Dockerfile               # Containerização (opcional)
│   ├── __init__.py
│   └── arquivo_tratado/         # Dados processados
│       └── df_model_ready.csv   # Dataset pronto para modelo
│
├── arquivos/                     # Dados brutos
│   ├── 2022.csv                 # Dados 2022
│   ├── 2023.csv                 # Dados 2023
│   └── 2024.csv                 # Dados 2024
│
├── notebooks/                    # Análise exploratória
│   ├── analise_exploratoria.ipynb
│   ├── bases.ipynb
│   └── tratamento_dados.ipynb
│
├── API_REPORT.md                # Documentação da API
├── RESUMO_EXECUTIVO.md          # Resumo executivo
├── venv.bash                    # Script para ambiente virtual
└── README.md                    # Este arquivo
```

---

## 🔧 Configuração e Inicialização

### 1. Preparar Ambiente

```bash
# Ativar ambiente virtual (Windows)
.\venv.bash

# Ou criar novo ambiente
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar Dependências

```bash
cd src
pip install -r requirements.txt
```

### 3. Iniciar API

#### Opção A: Usar Launcher
```bash
cd app
python run.py
```

#### Opção B: Uvicorn Direto
```bash
cd app
python -m uvicorn main_simple:app --host 127.0.0.1 --port 8002 --reload
```

### 4. Testar API

```bash
# Health Check
curl http://127.0.0.1:8002/health

# Documentação Interativa (Swagger)
# Abrir navegador: http://127.0.0.1:8002/docs

# Fazer Predição
curl -X POST http://127.0.0.1:8002/predict \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 15, "fase": "7", "ieg": 8.5, "ida": 8.0,
    "ian": 7.5, "ipp": 8.2, "ips": 7.8, "ipv": 8.3,
    "pedra": "Quartzo", "ponto_virada": "Sim",
    "ieg_anterior": 8.0, "ida_anterior": 7.8
  }'
```

---

## 📊 Endpoints da API

### GET `/`
Verificar status da API

```json
{
  "message": "API Passos Mágicos - Previsão de Evasão",
  "status": "online",
  "version": "1.0"
}
```

### GET `/health`
Health check

```json
{
  "status": "healthy",
  "model_loaded": true,
  "config_loaded": true
}
```

### GET `/info`
Informações do modelo

```json
{
  "model_type": "RandomForestClassifier",
  "features_count": 8,
  "f1_score_cv": 0.8994,
  "sklearn_version": "1.3.0"
}
```

### POST `/predict`
**Fazer predição de risco**

**Request:**
```json
{
  "idade": 15,
  "fase": "7",
  "ieg": 8.5,
  "ida": 8.0,
  "ian": 7.5,
  "ipp": 8.2,
  "ips": 7.8,
  "ipv": 8.3,
  "pedra": "Quartzo",
  "ponto_virada": "Sim",
  "ieg_anterior": 8.0,
  "ida_anterior": 7.8
}
```

**Response:**
```json
{
  "status": "OK",
  "risk_probability": 0.02,
  "risk_classification": "Baixo",
  "prediction": 0,
  "message": "Aluno com risco baixo de evasão"
}
```

### GET `/docs`
Swagger UI interativa

---

## 🤖 Modelo Machine Learning

**Arquitetura:**
- Tipo: RandomForestClassifier
- Estimators: 200 árvores
- Max Depth: 10
- Class Weight: Balanceado
- Random State: 42

**Performance:**
- Acurácia: 99.64%
- F1-Score (CV): 0.8994
- Recall: 100%
- Precisão: 95.36%

**Features (8):**
1. `idade` - Idade do aluno
2. `ieg` - Indicador de Envolvimento Gestalt
3. `ida` - Indicador de Dedicação Académica
4. `ian` - Indicador de Afinidade com Números
5. `ipp` - Indicador de Participação Presencial
6. `ips` - Indicador de Participação Social
7. `ipv` - Indicador de Presença Virtual
8. `defasagem` - Indicador de Defasagem

**Classificação:**
- Classe 0: Sem Risco de Evasão
- Classe 1: Com Risco de Evasão

**Thresholds:**
- `Baixo`: P < 0.4
- `Médio`: 0.4 ≤ P < 0.7
- `Alto`: P ≥ 0.7

---

## 📝 Arquivos Principais

### `src/model.py`
Definição e treinamento do modelo oficial com StratifiedKFold cross-validation.

```python
def train_dropout_model(df):
    """Treina modelo RandomForest com CV estratificado"""
    # Retorna modelo treinado e scores

def save_model(model, filepath):
    """Salva modelo como pickle"""
```

### `src/preprocessing.py`
Normalização e pré-processamento de dados

### `app/main_simple.py`
API FastAPI com endpoints de predição

---

## 🧪 Pipelines de Dados

### Fluxo de Treinamento
1. Carregar dados brutos (`arquivos/*.csv`)
2. Pré-processar e normalizar
3. Selecionar features relevantes
4. Dividir train/test
5. Treinar RandomForest
6. Avaliar com StratifiedKFold
7. Salvar modelo

### Fluxo de Predição
1. Receber input via API
2. Validar com Pydantic
3. Transformar features
4. Fazer predição
5. Classificar risco
6. Retornar resposta JSON

---

## 📚 Notebooks

- **analise_exploratoria.ipynb** - Análise visual dos dados
- **bases.ipynb** - Exploração das bases de dados
- **tratamento_dados.ipynb** - Pipeline de tratamento de dados

---

## ⚙️ Dependências

```
pandas==1.5.3
scikit-learn==1.3.0
joblib
fastapi
uvicorn
pydantic
```

Instale com:
```bash
pip install -r src/requirements.txt
```

---

## 🐳 Docker (Opcional)

Para containerizar a aplicação:

```bash
cd src
docker build -t passos-magicos-api .
docker run -p 8002:8002 passos-magicos-api
```

---

## 📋 Checklist de Funcionalidade

- [x] Modelo treinado e salvo
- [x] API respondendo em todos endpoints
- [x] Predições funcionando
- [x] Health check OK
- [x] Documentação Swagger disponível
- [x] Tratamento de erros
- [x] Validação de inputs (Pydantic)
- [x] Classificação de risco (Baixo/Médio/Alto)

---

## 🔍 Troubleshooting

### API não inicia
```bash
# Verificar porta em uso
netstat -ano | findstr :8002

# Liberar porta
taskkill /PID <PID> /F
```

### Erro de versão sklearn
```bash
pip install scikit-learn==1.3.0 --force-reinstall
```

### Modelo não carrega
```bash
# Verificar arquivo
ls -la app/model/model.pkl

# Retrains se necessário
python src/model.py
```

---

## 📞 Suporte

Para questões ou bugs, verificar:
1. Logs da API
2. Documentação em API_REPORT.md
3. Validação de inputs
4. Status do modelo em `/health`

---

**Versão**: 1.0  
**Data**: Fevereiro 2026  
**Status**: ✅ Produção

