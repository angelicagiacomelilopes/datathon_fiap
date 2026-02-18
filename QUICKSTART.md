# 🚀 QUICK START GUIDE - Monitoramento de Drift

**Comece agora em 5 minutos!**

---

## ⚡ Opção 1: API REST (Recomendado)

### Passo 1: Iniciar o Servidor
```bash
cd projeto_datathon/app
python -m uvicorn main_monitoring:app --host 127.0.0.1 --port 8002
```

**Esperado**:
```
Uvicorn running on http://127.0.0.1:8002
Press CTRL+C to quit
```

### Passo 2: Fazer uma Predição
```bash
curl -X POST http://127.0.0.1:8002/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

**Resposta esperada**:
```json
{
  "prediction": "A1",
  "probability": 0.9834,
  "message": "Predição realizada com sucesso"
}
```

### Passo 3: Verificar Status de Drift
```bash
curl http://127.0.0.1:8002/drift/status
```

**Resposta esperada**:
```json
{
  "total_checks": 3,
  "drift_detected_count": 3,
  "drift_rate": "100%",
  "current_status": "DRIFT_DETECTED"
}
```

### Passo 4: Executar Análise Completa
```bash
curl -X POST http://127.0.0.1:8002/drift/check
```

**Resposta esperada** (análise com 4 métodos):
```json
{
  "timestamp": "2026-02-18T17:19:10",
  "ks_test": {
    "overall_drift": true,
    "features_with_drift": 3,
    "total_features": 8
  },
  "wasserstein_distance": {
    "overall_drift": false,
    "distances": {"idade": 0.183, "ieg": 0.095}
  },
  "psi_scores": {
    "drift_detected": true,
    "critical_features": ["ieg"]
  },
  "overall_status": "DRIFT_DETECTED"
}
```

### Passo 5: Ver Métricas
```bash
curl http://127.0.0.1:8002/performance/metrics
```

---

## ⚡ Opção 2: Dashboard Interativo

### Passo 1: Executar Dashboard
```bash
cd projeto_datathon
python src/drift_dashboard.py
```

### Passo 2: Escolher Modo

**Menu**:
```
╔════════════════════════════════════════════╗
║  MONITORAMENTO DE DRIFT - MENU PRINCIPAL   ║
╚════════════════════════════════════════════╝

1. 📊 Single Check - Análise pontual
2. 🔄 Continuous Monitoring - Monitoramento contínuo
3. 📈 Display Dashboard - Ver dashboard

Escolha uma opção (1-3): 
```

**Opção 1**: Análise rápida (~5 seg)  
**Opção 2**: Monitorar por X minutos  
**Opção 3**: Visualizar resultados

---

## ⚡ Opção 3: Python Script

### Usar Diretamente no Código
```python
from src.drift_monitor import DriftDetector, ModelPerformanceMonitor
import pandas as pd

# 1. Carregar dados base
baseline = pd.read_csv('src/arquivo_tratado/df_tratado_concatenado.csv')
features = ['idade', 'fase', 'ieg', 'ida', 'ian', 'ipp', 'ips', 'ipv']

# 2. Inicializar detector
detector = DriftDetector(baseline, features, threshold=0.05)

# 3. Analisar novos dados
new_data = pd.read_csv('novo_dados.csv')
analysis = detector.analyze_drift(new_data)

# 4. Ver resultado
print(f"Drift Detected: {analysis['overall_status']}")
print(f"KS Test: {analysis['ks_test']['overall_drift']}")
print(f"Wasserstein: {analysis['wasserstein_distance']}")
print(f"PSI: {analysis['psi_scores']}")
```

---

## 📊 Interpretando Resultados

### Quando Ver 🚨 DRIFT_DETECTED

```
✅ SITUAÇÃO NORMAL (STABLE):
- KS Test: overall_drift = false
- Wasserstein: overall_drift = false
- PSI: drift_detected = false
➜ Ação: Continuar monitorando

⚠️ ATENÇÃO (1-2 métodos com drift):
- Alguns testes indicam mudança
- Possível anomalia nos dados
➜ Ação: Investigar features com drift

🚨 CRÍTICO (>2 métodos com drift):
- Múltiplos sinais de drift
- Dados significativamente diferentes
➜ Ação: Revisar dados de entrada, considerar retraining
```

### Interpretação por Método

| Método | Drift=True | Drift=False |
|--------|-----------|-----------|
| **KS Test** | Distribuição mudou | Distribuição estável |
| **Wasserstein** | Distância > threshold | Distribuição similar |
| **PSI** | PSI > 0.1 | Mudança pequena |
| **Chi-Square** | Independência violada | Independência OK |

---

## 🔧 Troubleshooting

### ❌ Erro: "ModuleNotFoundError: No module named 'scipy'"
```bash
# Solução
pip install scipy==1.12.0
```

### ❌ Erro: "Port 8002 already in use"
```bash
# Solução 1: Usar porta diferente
python -m uvicorn app.main_monitoring:app --port 8003

# Solução 2: Matar processo
# Windows
netstat -ano | findstr :8002
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8002
kill -9 <PID>
```

### ❌ Erro: "CSV file not found"
```bash
# Verificar se o arquivo existe
ls src/arquivo_tratado/df_tratado_concatenado.csv

# Se não existir, precisa rodar o preprocessamento
python src/preprocessing.py
```

### ❌ Alerts não aparecem
```bash
# Verificar arquivo de alertas
cat logs/drift_alerts.json

# Se vazio, resetar
echo "[]" > logs/drift_alerts.json
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Monitorar Uma Cliente
```bash
# Fazer predição
curl -X POST http://127.0.0.1:8002/predict \
  -H "Content-Type: application/json" \
  -d '{"idade": 15, "fase": "7", ...}'

# Ver drift após 10 predições
curl http://127.0.0.1:8002/drift/status

# Se drift detectado, ver análise completa
curl -X POST http://127.0.0.1:8002/drift/check
```

### Exemplo 2: Monitoramento Noturno
```bash
# Windows - Task Scheduler
# Agendar: python src/drift_dashboard.py (opção 2)
# Frequência: Diariamente 22:00 às 06:00

# Linux - Cron
# crontab -e
# 0 22 * * * cd /path/to/projeto && python src/drift_dashboard.py
```

### Exemplo 3: Integração com Seu App
```python
import requests

# Fazer predição
response = requests.post(
    'http://127.0.0.1:8002/predict',
    json={
        'idade': 15,
        'fase': '7',
        # ... outros campos
    }
)

if response.status_code == 200:
    pred = response.json()
    prediction = pred['prediction']
    confidence = pred['probability']

# Verificar drift a cada 100 predições
if prediction_count % 100 == 0:
    drift_response = requests.post(
        'http://127.0.0.1:8002/drift/check'
    )
    drift_status = drift_response.json()
    
    if drift_status['overall_status'] == 'DRIFT_DETECTED':
        print("⚠️ Drift detectado! Revisar dados.")
        alerts = requests.get(
            'http://127.0.0.1:8002/alerts/recent?limit=5'
        )
        print(alerts.json())
```

---

## 📚 Recursos Adicionais

- 📖 [Guia Completo](MONITORING_GUIDE.md)
- 🔧 [Documentação Técnica](DRIFT_IMPLEMENTATION.md)
- 📊 [Status do Projeto](PROJECT_STATUS.md)
- ✅ [Testes](test_monitoring.py)

---

## 🎯 Checklist - Primeiro Uso

- [ ] Passei por uma das 3 opções acima
- [ ] API está rodando em http://127.0.0.1:8002
- [ ] Consegui fazer uma predição com /predict
- [ ] /drift/status retornou resultados
- [ ] /drift/check executou análise completa
- [ ] Li a documentação adicional (opcional)

---

## ❓ Dúvidas Comuns

**P: Onde os alertas são salvos?**  
R: Em `logs/drift_alerts.json`

**P: Como resetar o monitoramento?**  
R: Delete `logs/drift_alerts.json` e reinicie a API

**P: Qual a frequência recomendada?**  
R: A cada 100 predições ou 1 hora (o que vier primeiro)

**P: Como mudar threshold de drift?**  
R: Edite `src/drift_monitor.py`, linha onde `DriftDetector` é criada

**P: Posso mudar a porta?**  
R: Sim! Use `--port 8003` no comando uvicorn

---

## 🚀 Próximos Passos

1. ✅ Teste a API (este guia)
2. ⏭️ Leia o [Guia Completo](MONITORING_GUIDE.md)
3. ⏭️ Configure monitoramento contínuo
4. ⏭️ Setup alertas por email/Slack
5. ⏭️ Deploy em produção

---

**Sucesso! 🎉**

Se tudo funcionou, você tem um sistema de monitoramento de drift pronto para produção!

Para dúvidas, consulte [MONITORING_GUIDE.md](MONITORING_GUIDE.md) ou [PROJECT_STATUS.md](PROJECT_STATUS.md).
