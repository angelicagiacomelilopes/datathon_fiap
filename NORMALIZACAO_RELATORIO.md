# 📊 RELATÓRIO: Normalização de Dados

**Data**: 18 de Fevereiro de 2026  
**Status**: ⚠️ PARCIALMENTE IMPLEMENTADO

---

## ✅ O QUE FOI NORMALIZADO

### 1. Dados de Treino ✅
**Arquivo**: `src/preprocessing.py`

```python
# StandardScaler aplicado aos dados numéricos
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())  # ← NORMALIZAÇÃO
])
```

**Características**:
- ✅ Imputação de valores faltantes (mediana)
- ✅ Normalização z-score (StandardScaler)
- ✅ Aplicado durante o treinamento do modelo

**Features Normalizadas**:
- `idade`, `ieg`, `ida`, `ian`, `ipp`, `ips`, `ipv`, `defasagem`

### 2. Dados de Predição ❌
**Arquivo**: `app/main_simple.py`

```python
# Dados de predição NÃO estão sendo normalizados!
X = pd.DataFrame([[
    student.idade, student.ieg, student.ida, student.ian,
    student.ipp, student.ips, student.ipv, defasagem_num
]], columns=features_order)

# Falta normalizar os dados aqui
```

---

## 🔍 PROBLEMA IDENTIFICADO

```
TREINO:    Dados Normalizados (StandardScaler)
           ↓
MODELO:    Aprende com dados normalizados
           ↓
PREDIÇÃO:  Dados NÃO NORMALIZADOS ❌
           ↓
RESULTADO: INCONSISTÊNCIA
```

**Consequência**: As predições podem estar **incorretas** porque:
1. O modelo foi treinado com dados **normalizados** (média=0, desvio=1)
2. As predições usam dados **brutos** (valores originais)
3. A distribuição é completamente diferente

---

## ✨ SOLUÇÃO RECOMENDADA

### Opção 1: Normalizar na Predição (RECOMENDADO)
```python
# Carregar o scaler junto com o modelo
scaler = joblib.load('app/model/scaler.pkl')

# Normalizar dados antes de predizer
X_normalized = scaler.transform(X)
prediction = model.predict(X_normalized)
```

### Opção 2: Não Normalizar em Nenhum Lugar
```python
# Treinar o modelo sem normalização
# Random Forest não precisa de normalização (tree-based)
# Mas deve ser consistente!
```

---

## 📋 CHECKLIST DE NORMALIZAÇÃO

| Componente | Status | Ação |
|-----------|--------|------|
| Preprocessing (treino) | ✅ | Mantém |
| Model.py (treino) | ✅ | Mantém |
| main_simple.py (predição) | ❌ | CORRIGIR |
| Scaler salvo | ❌ | CRIAR |
| Documentação | ⚠️  | ATUALIZAR |

---

## 🎯 IMPLEMENTAÇÃO NECESSÁRIA

1. **Salvar o scaler** durante o treinamento
   ```python
   # Em src/model.py
   joblib.dump(scaler, 'app/model/scaler.pkl')
   ```

2. **Usar o scaler na predição**
   ```python
   # Em app/main_simple.py
   scaler = joblib.load('app/model/scaler.pkl')
   X_normalized = scaler.transform(X)
   prediction = model.predict(X_normalized)
   ```

3. **Testar a consistência**
   - Comparar resultados antes/depois
   - Validar que predições fazem sentido

---

## 📊 ESTADO ATUAL

```
✅ TREINO:     Dados normalizados corretamente
✅ MODELO:     Aprende com distribuição Z (média=0, std=1)
❌ PREDIÇÃO:   Dados não normalizados
⚠️  RISCO:     Resultados podem ser incorretos
```

---

## 🔧 RECOMENDAÇÃO URGENTE

✨ **IMPLEMENTAR NORMALIZAÇÃO NA PREDIÇÃO**

Para garantir que o modelo está fazendo predições corretas, é essencial aplicar **o mesmo scaler** que foi usado no treinamento.

---

**Prioridade**: 🔴 ALTA  
**Impacto**: Acurácia das predições  
**Esforço**: 15 minutos

