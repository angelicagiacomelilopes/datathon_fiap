#!/usr/bin/env python
import joblib
import os
import sys

sys.path.insert(0, 'src')

# Verificar artefatos
scaler_path = 'app/model/scaler.pkl'
model_path = 'app/model/model.pkl'
config_path = 'app/model/model_config.pkl'

print('\n📋 VERIFICAÇÃO DE ARTEFATOS DO MODELO\n' + '='*50)
print(f'Scaler salvo:       {"✅ SIM" if os.path.exists(scaler_path) else "❌ NÃO"}')
print(f'Modelo salvo:       {"✅ SIM" if os.path.exists(model_path) else "❌ NÃO"}')
print(f'Config salva:       {"✅ SIM" if os.path.exists(config_path) else "❌ NÃO"}')

if os.path.exists(config_path):
    config = joblib.load(config_path)
    print(f'\n📝 CONFIGURAÇÃO DO MODELO:')
    for key, value in config.items():
        if key != 'feature_names_out':
            print(f'  • {key}: {value}')

# Verificar como o modelo foi treinado
print(f'\n🔍 ANÁLISE:')
print(f'  - RandomForest: Não requer normalização (tree-based)')
print(f'  - Mas dados foram normalizados no preprocessing.py')
print(f'  - Status: INCONSISTÊNCIA POTENCIAL')

if not os.path.exists(scaler_path):
    print(f'\n⚠️  PROBLEMA IDENTIFICADO:')
    print(f'  - Scaler não foi salvo')
    print(f'  - Treino pode ter normalizado, predição usa dados brutos')
    print(f'  - Solução: Salvar e usar o scaler na predição')
