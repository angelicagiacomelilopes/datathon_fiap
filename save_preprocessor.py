#!/usr/bin/env python
"""
Script para salvar o preprocessor (com scaler) que foi usado no treinamento
Isso garante consistência entre treino e predição
"""
import sys
import os
import pandas as pd
import joblib
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.preprocessing import DataPreprocessor, TratamentoDados, create_features, LeituraArquivos

def save_preprocessor():
    """Cria e salva o preprocessor com base nos dados de treinamento"""
    
    print("Carregando e processando dados brutos...")
    
    # Processar os arquivos 2022, 2023, 2024
    processed_dfs = []
    
    for ano in [2022, 2023, 2024]:
        try:
            file_path = f'arquivos/{ano}.csv'
            print(f"   >> {file_path}")
            
            leitor = LeituraArquivos(file_path)
            df_raw = leitor.ler_arquivo()
            
            if df_raw is not None:
                tratador = TratamentoDados(df_raw)
                df_tratado = tratador.executar_tratamento()
                processed_dfs.append(df_tratado)
                print(f"   OK - {ano}: {len(df_tratado)} registros")
        except Exception as e:
            print(f"   AVISO - {ano}: {e}")
    
    if not processed_dfs:
        raise ValueError("Nenhum dado foi processado!")
    
    # Concatenar dados
    print("Concatenando dados...")
    df_concatenado = pd.concat(processed_dfs, ignore_index=True)
    print(f"   Total: {len(df_concatenado)} registros")
    
    # Feature Engineering
    print("Gerando features...")
    df_features = create_features(df_concatenado)
    
    # Remover coluna de target se existir
    if 'atingiu_pv' in df_features.columns:
        y = df_features['atingiu_pv']
        X = df_features.drop('atingiu_pv', axis=1)
    else:
        X = df_features
        y = None
    
    print(f"Shape dos dados: {X.shape}")
    
    # Criar e treinar preprocessor
    print("Criando preprocessor com StandardScaler...")
    preprocessor = DataPreprocessor()
    preprocessor.fit(X, y)
    
    # Salvar preprocessor
    model_dir = 'app/model'
    os.makedirs(model_dir, exist_ok=True)
    
    preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
    joblib.dump(preprocessor, preprocessor_path)
    
    print(f"[OK] Preprocessor salvo: {preprocessor_path}")
    print(f"     - Colunas numericas: {preprocessor.numerical_cols}")
    print(f"     - Colunas categoricas: {preprocessor.categorical_cols}")
    
    return preprocessor_path

if __name__ == '__main__':
    try:
        save_preprocessor()
        print("\n[SUCESSO] Preprocessor configurado com sucesso!")
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
