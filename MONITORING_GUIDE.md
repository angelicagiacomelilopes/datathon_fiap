# 📊 Monitoramento de Drift - Guia de Uso

## Visão Geral

Sistema completo de monitoramento de drift (data drift, concept drift e model drift) para o modelo de previsão de evasão escolar.

```
┌─────────────────────┐
│   Novo Dados        │
│   (Production)      │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────┐
│  Drift Detector              │
│  - Kolmogorov-Smirnov        │
│  - Wasserstein Distance      │
│  - Chi-Square Test           │
│  - Population Stability Idx  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Alert System                │
│  - Gera alertas              │
│  - Log persistente           │
│  - Histórico de eventos      │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Performance Monitor         │
│  - Rastreia predições        │
│  - Calcula acurácia          │
│  - Detecta degradação        │
└──────────────────────────────┘
```

---

## 1. Instalação

```bash
pip install scipy
```

---

## 2. Endpoints da API com Monitoramento

### Iniciar API com Monitoramento

```bash
cd app
python -m uvicorn main_monitoring:app --host 127.0.0.1 --port 8002 --reload
```

### GET `/`
Status da API com monitoramento

```json
{
  "message": "API Passos Mágicos - Previsão de Evasão",
  "status": "online",
  "version": "1.1",
  "monitoring": "enabled"
}
```

### GET `/drift/status`
Status resumido do drift

```json
{
  "total_checks": 5,
  "drift_detected_count": 1,
  "drift_rate": "20.0%",
  "latest_check": "2026-02-18T10:30:45.123456",
  "current_status": "STABLE",
  "last_5_checks": [false, false, true, false, false]
}
```

### POST `/drift/check`
Executar análise de drift completa

```bash
curl -X POST http://127.0.0.1:8002/drift/check
```

Resposta:
```json
{
  "status": "OK",
  "drift_detected": false,
  "analysis": {
    "timestamp": "2026-02-18T10:32:15.654321",
    "sample_size": 100,
    "ks_test": {
      "idade": {
        "statistic": 0.12,
        "pvalue": 0.45,
        "drift_detected": false
      },
      "ieg": {...}
    },
    "wasserstein": {...},
    "chi_square": {...},
    "psi": {...},
    "overall_drift_detected": false
  }
}
```

### GET `/performance/metrics`
Métricas de performance do modelo

```json
{
  "total_predictions": 1250,
  "avg_confidence": 0.35,
  "accuracy": 0.92,
  "recent_accuracy_100": 0.94,
  "prediction_distribution": {
    "0": 1180,
    "1": 70
  },
  "performance_status": "HEALTHY",
  "last_update": "2026-02-18T10:35:22.789012"
}
```

### GET `/alerts/summary`
Resumo de alertas

```json
{
  "total_alerts": 8,
  "by_type": {
    "DATA_DRIFT": 5,
    "PERFORMANCE_DEGRADATION": 2,
    "MODEL_DRIFT": 1
  },
  "by_severity": {
    "INFO": 2,
    "WARNING": 4,
    "CRITICAL": 2
  },
  "recent_alerts": [...]
}
```

### GET `/alerts/recent?limit=10`
Últimos alertas

```json
{
  "recent_alerts": [
    {
      "timestamp": "2026-02-18T09:45:12.345678",
      "type": "DATA_DRIFT",
      "severity": "WARNING",
      "message": "Drift detectado nos dados",
      "details": {...}
    },
    ...
  ]
}
```

---

## 3. Monitoramento Contínuo em Background

### Execução Simples

```bash
python src/drift_dashboard.py
```

Opções:
```
1. Executar single check
2. Executar monitoramento contínuo (1 hora)
3. Visualizar dashboard
```

### Opção 1: Single Check
Executa uma verificação única de drift

```bash
# Escolher opção 1
# Resultado: JSON com análise completa
```

### Opção 2: Monitoramento Contínuo
Verifica drift periodicamente

```bash
# Escolher opção 2
# Intervalo (min): 60
# Duração (horas): 24
# 
# Executa por 24 horas, verificando a cada 60 minutos
# Salva relatórios em logs/drift_reports/
```

### Opção 3: Dashboard
Visualiza status atual

```bash
# Escolher opção 3
# Mostra resumo de drift, performance e alertas
```

---

## 4. Exemplo de Uso em Python

```python
import pandas as pd
import joblib
from src.drift_monitor import DriftDetector, ModelPerformanceMonitor, DriftAlert

# Carregar dados baseline
baseline = pd.read_csv('src/arquivo_tratado/df_model_ready.csv')
config = joblib.load('app/model/model_config.pkl')

# Inicializar detector
features = config['features']
detector = DriftDetector(baseline, features, threshold=0.05)

# Simular novos dados
new_data = baseline.sample(n=100, random_state=42)

# Analisar drift
analysis = detector.analyze_drift(new_data)

print(f"Drift detectado: {analysis['overall_drift_detected']}")
print(f"KS Test - pvalues: {analysis['ks_test']}")
print(f"Wasserstein: {analysis['wasserstein']}")
print(f"PSI: {analysis['psi']}")

# Rastrear performance
performance = ModelPerformanceMonitor()
performance.log_prediction(
    prediction=0,
    probability=0.25,
    actual=0,
    metadata={'student_id': '12345'}
)

metrics = performance.get_model_metrics()
print(f"Acurácia: {metrics['accuracy']:.2%}")
```

---

## 5. Métodos de Detecção de Drift

### Kolmogorov-Smirnov (KS Test)
- **O quê**: Testa se duas distribuições são diferentes
- **Como**: Compara a máxima diferença entre CDFs
- **Quando usar**: Excelente para detectar mudanças na distribuição
- **Threshold**: pvalue < 0.05

### Wasserstein Distance
- **O quê**: Mede a "distância" entre duas distribuições
- **Como**: Calcula o custo mínimo para transformar uma em outra
- **Quando usar**: Mais sensível a mudanças graduais
- **Threshold**: > 0.5 (normalizado)

### Chi-Square Test
- **O quê**: Testa independência entre variáveis categóricas
- **Como**: Compara frequências observadas vs esperadas
- **Quando usar**: Para dados categóricos/discretos
- **Threshold**: pvalue < 0.05

### Population Stability Index (PSI)
- **O quê**: Mede mudança na distribuição de um feature
- **Como**: Soma ponderada das log-razões de proporções
- **Quando usar**: Para monitoramento contínuo de features
- **Threshold**: PSI > 0.1 (drift detectado)

---

## 6. Interpretação de Alertas

### Status Codes

| Status | Significado |
|--------|-------------|
| `STABLE` | Sem drift detectado |
| `DRIFT_DETECTED` | Drift em ≥30% dos testes |
| `HEALTHY` | Model performance normal |
| `DEGRADING` | Acurácia recente < baseline - 10% |
| `BELOW_THRESHOLD` | Acurácia < 85% |

### Severidade de Alertas

| Nível | Descrição | Ação |
|-------|-----------|------|
| `INFO` | Informativo | Monitorar |
| `WARNING` | Possível problema | Revisar dados |
| `CRITICAL` | Action required | Retrainer modelo |

---

## 7. Configuração e Customização

### Ajustar Threshold de Drift

```python
detector = DriftDetector(baseline, features, threshold=0.01)  # Mais sensível
detector = DriftDetector(baseline, features, threshold=0.10)  # Menos sensível
```

### Ajustar Threshold de Performance

```python
monitor = ModelPerformanceMonitor(reference_threshold=0.90)
```

---

## 8. Relatórios Gerados

### Estrutura de Diretórios

```
logs/
├── drift_alerts.json          # Histórico de alertas
├── drift_reports/
│   ├── monitoring_report_20260218_100000.json
│   ├── monitoring_report_20260218_110000.json
│   └── ...
```

### Exemplo de Relatório

```json
{
  "timestamp": "2026-02-18T10:30:00.123456",
  "drift_summary": {
    "total_checks": 5,
    "drift_detected_count": 1,
    "drift_rate": "20.0%",
    "latest_check": "2026-02-18T10:30:00",
    "current_status": "STABLE",
    "last_5_checks": [false, false, true, false, false]
  },
  "performance_summary": {
    "total_predictions": 1250,
    "avg_confidence": 0.35,
    "accuracy": 0.92,
    "performance_status": "HEALTHY"
  },
  "alerts_summary": {
    "total_alerts": 8,
    "by_type": {"DATA_DRIFT": 5},
    "by_severity": {"WARNING": 4}
  }
}
```

---

## 9. Troubleshooting

### Erro: "Drift detector não inicializado"
```
Solução: Verificar se os arquivos de dados estão no lugar certo
         - src/arquivo_tratado/df_model_ready.csv
         - app/model/model_config.pkl
```

### Erro: "scipy not installed"
```bash
pip install scipy==1.12.0
```

### Muitos Falsos Positivos
```python
# Aumentar threshold
detector = DriftDetector(baseline, features, threshold=0.10)
```

---

## 10. Integração com Produção

### Monitoramento Contínuo com Cron (Linux/Mac)

```bash
# Executar check a cada hora
0 * * * * cd /path/projeto_datathon && python src/drift_dashboard.py << EOF
1
EOF
```

### Monitoramento com Scheduler (Windows)

```batch
# Task Scheduler - Ação:
# Program: python
# Args: src/drift_dashboard.py
# Recorrência: Cada hora
```

### Monitoramento com Docker

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r src/requirements.txt
CMD ["python", "src/drift_dashboard.py"]
```

---

## Checklist de Implementação

- [x] DriftDetector com múltiplos testes estatísticos
- [x] ModelPerformanceMonitor para rastrear acurácia
- [x] Sistema de alertas persistente
- [x] API com endpoints de monitoramento
- [x] Dashboard interativo
- [x] Relatórios automáticos
- [x] Documentação completa

---

**Versão**: 1.1  
**Data**: Fevereiro 2026  
**Status**: ✅ Pronto para Produção
