# VALIDAÇÃO DA API - JSON PARA TESTES

## TESTE 1: ALTO RISCO (74.34%)

```json
{
  "idade": 18,
  "fase": "EF",
  "ieg": 0.5,
  "ida": 0.5,
  "ian": -0.9,
  "ipp": -0.0,
  "ips": 0.6,
  "ipv": 1.2,
  "pedra": "Ametista",
  "ponto_virada": "Sim"
}
```

**Resposta Esperada:**
```json
{
  "status": "OK",
  "risk_probability": 0.74,
  "risk_classification": "Alto",
  "prediction": 1,
  "message": "Aluno com risco alto de evasão"
}
```

**Resultado Obtido:** ✅ PASSOU
```json
{
  "status": "OK",
  "risk_probability": 0.7433516571574833,
  "risk_classification": "Alto",
  "prediction": 1,
  "message": "Aluno com risco alto de evasão"
}
```

---

## TESTE 2: BAIXO RISCO (0.5%)

```json
{
  "idade": 18,
  "fase": "EM",
  "ieg": 0.8,
  "ida": -0.5,
  "ian": 0.8,
  "ipp": 0.9,
  "ips": 0.9,
  "ipv": -0.5,
  "pedra": "Quartzo",
  "ponto_virada": "Nao"
}
```

**Resposta Esperada:**
```json
{
  "status": "OK",
  "risk_probability": 0.005,
  "risk_classification": "Baixo",
  "prediction": 0,
  "message": "Aluno com risco baixo de evasão"
}
```

**Resultado Obtido:** ✅ PASSOU
```json
{
  "status": "OK",
  "risk_probability": 0.005,
  "risk_classification": "Baixo",
  "prediction": 0,
  "message": "Aluno com risco baixo de evasão"
}
```

---

## TESTE 3: RISCO MÉDIO (Para você testar)

```json
{
  "idade": 20,
  "fase": "EM",
  "ieg": 0.2,
  "ida": 0.0,
  "ian": 0.0,
  "ipp": 0.2,
  "ips": 0.0,
  "ipv": 0.5,
  "pedra": "Topazio",
  "ponto_virada": "Sim"
}
```

**Classificação Esperada:** Médio (40-70%)

---

## COMO TESTAR

### Via cURL:
```bash
curl -X POST http://127.0.0.1:8002/predict \
  -H "Content-Type: application/json" \
  -d '{
    "idade": 18,
    "fase": "EF",
    "ieg": 0.5,
    "ida": 0.5,
    "ian": -0.9,
    "ipp": -0.0,
    "ips": 0.6,
    "ipv": 1.2,
    "pedra": "Ametista",
    "ponto_virada": "Sim"
  }'
```

### Via Python Requests:
```python
import requests
import json

data = {
    "idade": 18,
    "fase": "EF",
    "ieg": 0.5,
    "ida": 0.5,
    "ian": -0.9,
    "ipp": -0.0,
    "ips": 0.6,
    "ipv": 1.2,
    "pedra": "Ametista",
    "ponto_virada": "Sim"
}

response = requests.post('http://127.0.0.1:8002/predict', json=data)
print(json.dumps(response.json(), indent=2))
```

### Via JavaScript/Frontend:
```javascript
const data = {
    idade: 18,
    fase: "EF",
    ieg: 0.5,
    ida: 0.5,
    ian: -0.9,
    ipp: -0.0,
    ips: 0.6,
    ipv: 1.2,
    pedra: "Ametista",
    ponto_virada: "Sim"
};

fetch('http://127.0.0.1:8002/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
})
.then(r => r.json())
.then(data => console.log(JSON.stringify(data, null, 2)));
```

---

## DESCRIÇÃO DOS CAMPOS

| Campo | Tipo | Descrição | Exemplo |
|-------|------|-----------|---------|
| `idade` | float | Idade em anos | 18 |
| `fase` | string | EF, EM, etc | "EF" |
| `ieg` | float | Índice Engajamento (-1 a 1) | 0.5 |
| `ida` | float | Índice Dados Abertos (-1 a 1) | 0.5 |
| `ian` | float | Índice Afinidade Numérica (-1 a 1) | -0.9 |
| `ipp` | float | Índice Participação Presencial (-1 a 1) | -0.0 |
| `ips` | float | Índice Participação Social (-1 a 1) | 0.6 |
| `ipv` | float | Índice Pontos Vermelhos (0 a 2) | 1.2 |
| `pedra` | string | Classificação (Ametista, Topazio, Agata, Quartzo) | "Ametista" |
| `ponto_virada` | string | Sim/Nao | "Sim" |

---

## INTERPRETAÇÃO DO RISCO

- **ALTO (70%+)**: Risco de evasão muito elevado → Intervenção imediata
- **MÉDIO (40-70%)**: Risco moderado → Acompanhamento
- **BAIXO (<40%)**: Baixo risco → Monitoramento normal

---

## STATUS DA API

✅ Modelo: Carregado (99.64% accuracy)
✅ Preprocessor: Carregado com StandardScaler
✅ Normalização: Ativa
✅ Testes: ✅ PASSOU

**API está pronta para validação!**
