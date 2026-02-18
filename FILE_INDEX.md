# 📑 ÍNDICE DE ARQUIVOS - Guia de Navegação

**Encontre rapidamente o que você precisa!**

---

## 🎯 POR OBJETIVO

### Quero... Fazer uma Predição
- 📍 **API Endpoint**: `app/main_monitoring.py` (linha ~100)
- 📍 **Documentação**: `QUICKSTART.md` (Opção 1)
- 🔗 **Command**: `curl -X POST http://127.0.0.1:8002/predict`

### Quero... Monitorar Drift
- 📍 **Core System**: `src/drift_monitor.py` (DriftDetector class)
- 📍 **API Endpoint**: `app/main_monitoring.py` (GET /drift/status)
- 📍 **Documentação**: `MONITORING_GUIDE.md` (Seção: Usando o Sistema)
- 📍 **Quick Guide**: `QUICKSTART.md` (Opção 1 - Passo 3)

### Quero... Ver Dashboard Interativo
- 📍 **Dashboard Code**: `src/drift_dashboard.py`
- 📍 **Documentação**: `QUICKSTART.md` (Opção 2)
- 🔗 **Command**: `python src/drift_dashboard.py`

### Quero... Entender o Código
- 📍 **Arquitetura**: `DRIFT_IMPLEMENTATION.md` (Seção: Fluxo de Execução)
- 📍 **API Endpoints**: `MONITORING_GUIDE.md` (Seção: API Rest Endpoints)
- 📍 **Código Fonte**: `src/drift_monitor.py` (Classes com comentários)

### Quero... Rodar Testes
- 📍 **Test Suite**: `test_monitoring.py`
- 📍 **Documentação**: `MONITORING_GUIDE.md` (Seção: Validação e Testes)
- 🔗 **Command**: `python test_monitoring.py`

### Quero... Integrar em Meu App
- 📍 **Python Examples**: `MONITORING_GUIDE.md` (Seção: Exemplo Python)
- 📍 **API Docs**: `MONITORING_GUIDE.md` (Seção: API Rest Endpoints)
- 📍 **Quick Start**: `QUICKSTART.md` (Opção 3)

### Quero... Implementar em Produção
- 📍 **Guia Deployment**: `MONITORING_GUIDE.md` (Seção: Deployment)
- 📍 **Status Projeto**: `PROJECT_STATUS.md` (Seção: Próximos Passos)
- 📍 **Requisitos**: `src/requirements.txt`

---

## 📁 ESTRUTURA DE ARQUIVOS

### 📊 Documentação (Você deve ler estes!)
```
✨ QUICKSTART.md ..................... Comece aqui! (5 minutos)
✨ MONITORING_GUIDE.md .............. Guia técnico completo
✨ DRIFT_IMPLEMENTATION.md .......... Detalhes da implementação
✨ PROJECT_STATUS.md ................ Status e checklist final
📄 README.md ........................ Documentação geral (src/)
```

### 🐍 Código do Monitoramento (Novo!)
```
✨ src/drift_monitor.py ............ Classes: DriftDetector, Monitor, Alert
✨ src/drift_dashboard.py ......... Dashboard e CLI
✨ app/main_monitoring.py ......... API v1.1 com endpoints
✨ test_monitoring.py ............. Suite de testes (7 testes)
```

### 🤖 Modelo e Processamento
```
📌 src/model.py ................... Modelo oficial (99.64% accuracy)
📌 src/preprocessing.py ........... Preprocessamento de dados
📌 src/feature_engineering.py .... Feature engineering
📌 src/tratamento_dados.py ....... Tratamento de dados
```

### 📦 Arquivos de Dados
```
💾 src/arquivo_tratado/df_tratado_concatenado.csv ... Baseline (referência)
💾 src/arquivo_tratado/df_tratado_2022.csv
💾 src/arquivo_tratado/df_tratado_2023.csv
💾 src/arquivo_tratado/df_tratado_2024.csv
```

### 📝 Logs e Alertas
```
🔔 logs/drift_alerts.json ................. Alertas persistentes
📊 logs/drift_reports/*.json ............. Relatórios automáticos
📋 logs/leituraarquivos/ ................. Logs de leitura
📋 logs/tratamentodados/ ................. Logs de processamento
```

### 🧪 Testes
```
✅ test_monitoring.py .................... Testes do monitoramento
🔗 src/tests/ ........................... Testes unitários
```

### ⚙️ Configuração
```
🔧 src/requirements.txt ................. Dependências Python
🐳 src/Dockerfile ...................... Container Docker
🌐 app/routes.py ....................... Rotas adicionais
```

---

## 🔍 POR ARQUIVO

### `QUICKSTART.md`
```
📍 Localização: projeto_datathon/QUICKSTART.md
⏱️ Tempo de leitura: 5 minutos
🎯 Para quem: Iniciante, quer começar já
📚 Conteúdo:
  - Opção 1: API REST (recomendado)
  - Opção 2: Dashboard Interativo
  - Opção 3: Python Script
  - Troubleshooting rápido
  - Exemplos de uso
```

### `MONITORING_GUIDE.md`
```
📍 Localização: projeto_datathon/MONITORING_GUIDE.md
⏱️ Tempo de leitura: 20 minutos
🎯 Para quem: Dev, quer entender tudo
📚 Conteúdo:
  - Arquitetura completa
  - Explicação de cada método
  - API endpoints detalhados
  - Exemplos Python
  - Deployment guide
  - Troubleshooting avançado
```

### `DRIFT_IMPLEMENTATION.md`
```
📍 Localização: projeto_datathon/DRIFT_IMPLEMENTATION.md
⏱️ Tempo de leitura: 15 minutos
🎯 Para quem: Tech lead, quer conhecer detalhes técnicos
📚 Conteúdo:
  - O que foi implementado
  - Estrutura de dados
  - Fluxo de execução
  - Interpretação de resultados
  - Segurança e privacidade
  - Melhorias futuras
```

### `PROJECT_STATUS.md`
```
📍 Localização: projeto_datathon/PROJECT_STATUS.md
⏱️ Tempo de leitura: 10 minutos
🎯 Para quem: Manager, quer status geral
📚 Conteúdo:
  - Objetivos alcançados
  - Componentes implementados
  - Resultados dos testes
  - Estrutura final
  - Checklist de funcionamento
```

### `src/drift_monitor.py`
```
📍 Localização: projeto_datathon/src/drift_monitor.py
📊 Linhas: 320+
🎯 Para quem: Dev, quer estudar o código
📚 Classes:
  1. DriftDetector
     - analyze_drift() - Análise completa
     - ks_test() - Teste KS
     - wasserstein_distance() - Distância
     - psi_scores() - PSI
     - chi_square_test() - Chi-square
  
  2. ModelPerformanceMonitor
     - log_prediction() - Registrar predição
     - get_model_metrics() - Métricas
     - check_performance_degradation() - Degradação
  
  3. DriftAlert
     - create_alert() - Criar alerta
     - get_alert_summary() - Resumo
     - get_recent_alerts() - Recentes
```

### `app/main_monitoring.py`
```
📍 Localização: projeto_datathon/app/main_monitoring.py
📊 Linhas: 180+
🎯 Para quem: Dev, quer usar a API
📚 Endpoints:
  - GET / - Status
  - POST /predict - Fazer predição
  - GET /health - Health check
  - GET /drift/status - Status drift
  - POST /drift/check - Análise completa
  - GET /performance/metrics - Métricas
  - GET /alerts/summary - Resumo alertas
  - GET /alerts/recent - Alertas recentes
```

### `src/drift_dashboard.py`
```
📍 Localização: projeto_datathon/src/drift_dashboard.py
📊 Linhas: 200+
🎯 Para quem: Usuário/Analista
📚 Modos:
  1. Single Check - Análise pontual
  2. Continuous - Monitoramento contínuo
  3. Display - Ver dados salvos
```

### `test_monitoring.py`
```
📍 Localização: projeto_datathon/test_monitoring.py
📊 Linhas: 250+
🎯 Para quem: QA, quer validar sistema
📚 7 Testes:
  1. test_ks_test() - Teste KS
  2. test_wasserstein() - Wasserstein
  3. test_psi_calculation() - PSI
  4. test_performance_monitor() - Performance
  5. test_alert_system() - Alertas
  6. test_drift_history_and_summary() - Histórico
  7. test_compute_baseline() - Baseline
```

### `logs/drift_alerts.json`
```
📍 Localização: projeto_datathon/logs/drift_alerts.json
📊 Formato: JSONL (JSON Lines)
🎯 Para quem: Quer ver alertas registrados
📚 Conteúdo:
  {"timestamp": "...", "type": "DATA_DRIFT", "severity": "WARNING", ...}
  {"timestamp": "...", "type": "PERFORMANCE", "severity": "CRITICAL", ...}
```

### `src/requirements.txt`
```
📍 Localização: projeto_datathon/src/requirements.txt
📊 Dependências: 11 pacotes
🎯 Para quem: Dev ops, quer instalar dependências
📚 Principal novo:
  scipy==1.12.0 (para cálculos estatísticos)
```

---

## 🗺️ MAPA DE NAVEGAÇÃO

### Para Iniciantes
```
1. Leia: QUICKSTART.md (5 min)
2. Execute: python src/drift_dashboard.py (opção 1)
3. Veja resultados em: logs/drift_alerts.json
4. Se tudo OK → Use para monitorar seu modelo!
```

### Para Desenvolvedores
```
1. Leia: MONITORING_GUIDE.md (20 min)
2. Estude: src/drift_monitor.py (10 min)
3. Teste: python test_monitoring.py (5 min)
4. Integre: Adicione à seu projeto
5. Deploy: Siga seção "Deployment"
```

### Para Arquitetos
```
1. Leia: DRIFT_IMPLEMENTATION.md (15 min)
2. Revise: PROJECT_STATUS.md (10 min)
3. Estude: Arquitetura em MONITORING_GUIDE.md
4. Planeje: Integração com infra existente
5. Implemente: Seguindo guia de deployment
```

### Para Analistas
```
1. Execute: python src/drift_dashboard.py
2. Escolha: Opção 2 (Monitoramento contínuo)
3. Aguarde: Resultados em logs/drift_reports/
4. Analise: JSON reports gerados
5. Reporte: Findings ao time
```

---

## 🔗 LINKS RÁPIDOS

### Documentação
- [Quick Start (5 min)](QUICKSTART.md)
- [Guia Completo (20 min)](MONITORING_GUIDE.md)
- [Detalhes Técnicos (15 min)](DRIFT_IMPLEMENTATION.md)
- [Status do Projeto (10 min)](PROJECT_STATUS.md)

### Código
- [DriftDetector](src/drift_monitor.py#L1)
- [Monitor Performance](src/drift_monitor.py#L150)
- [Alert System](src/drift_monitor.py#L280)
- [API Endpoints](app/main_monitoring.py#L30)

### Dados
- [Baseline](src/arquivo_tratado/df_tratado_concatenado.csv)
- [Alertas](logs/drift_alerts.json)
- [Relatórios](logs/drift_reports/)

### Testes
- [Suite de Testes](test_monitoring.py)
- [Rodar: `python test_monitoring.py`]

---

## 📞 COMO USAR ESTE ÍNDICE

**Exemplo 1**: "Quero fazer uma predição"
- Vá para: **"POR OBJETIVO"**
- Procure: **"Quero... Fazer uma Predição"**
- Resultado: 3 links para ajuda

**Exemplo 2**: "Preciso entender drift_monitor.py"
- Vá para: **"POR ARQUIVO"**
- Procure: **"src/drift_monitor.py"**
- Resultado: Descrição e conteúdo

**Exemplo 3**: "Sou iniciante, por onde começo?"
- Vá para: **"MAPA DE NAVEGAÇÃO"**
- Escolha: **"Para Iniciantes"**
- Resultado: Passos ordenados

---

## ✅ Arquivo Recomendado por Papel

| Papel | Primeiro | Segundo | Terceiro |
|-------|----------|---------|----------|
| **Iniciante** | QUICKSTART.md | MONITORING_GUIDE.md | test_monitoring.py |
| **Developer** | MONITORING_GUIDE.md | src/drift_monitor.py | app/main_monitoring.py |
| **Data Scientist** | QUICK start.md | DRIFT_IMPLEMENTATION.md | notebooks |
| **DevOps** | src/requirements.txt | MONITORING_GUIDE.md (Deploy) | app/main_monitoring.py |
| **Manager** | PROJECT_STATUS.md | DRIFT_IMPLEMENTATION.md | - |
| **QA/Tester** | test_monitoring.py | MONITORING_GUIDE.md | QUICKSTART.md |

---

**Versão**: 1.0  
**Última Atualização**: 18 de Fevereiro de 2026  
**Mantido por**: Datathon Team

Boa navegação! 🚀
