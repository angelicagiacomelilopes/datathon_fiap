#!/usr/bin/env python
"""
Script para retrainer o modelo com os dados mais recentes
Uso: python retrain.py
"""
import sys
import os
import pandas as pd
import joblib
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.preprocessing import TratamentoDados, create_features, DataPreprocessor, clean_data
from src.model import train_dropout_model, save_model
from src.utils import LoggerConfig, ApplicationLogger

def retrain_model():
    """Retrain o modelo com dados recentes"""
    
    print("\n" + "="*80)
    print("RETREINAMENTO DO MODELO")
    print("="*80 + "\n")
    
    try:
        # Configurar logger
        config = LoggerConfig(app_name="ModelTraining", log_dir="logs")
        logger = ApplicationLogger("Retrain", config).logger
        
        # 1. Carregar e processar dados
        print("1. Carregando dados brutos...")
        processed_dfs = []
        
        # Leitura dos arquivos da pasta arquivos (conforme solicitado)
        # Verificando se existem arquivos CSV na pasta 'arquivos/'
        # Caso nao existam, tenta a pasta data/raw (caso o usuario tenha movido novamente ou em outro contexto)
        
        search_paths = ['arquivos', os.path.join('data', 'raw')]
        
        for ano in [2022, 2023, 2024]:
            file_found = False
            for base_dir in search_paths:
                file_path = os.path.join(base_dir, f'{ano}.csv')
                if os.path.exists(file_path):
                    print(f"   >> {file_path}")
                    try:
                        leitor = TratamentoDados(pd.read_csv(file_path))
                        df_raw = leitor.executar_tratamento()
                        processed_dfs.append(df_raw)
                        print(f"   OK - {ano}: {len(df_raw)} registros")
                        file_found = True
                        break # Encontrou, proximo ano
                    except Exception as e:
                        print(f"   ERRO ao processar {file_path}: {e}")
            
            if not file_found:
                 print(f"   AVISO - Arquivo nao encontrado para o ano {ano} nas pastas: {search_paths}")

        if not processed_dfs:
            raise ValueError("Nenhum dado foi processado!")
        
        # Concatenar dados
        print("\n2. Concatenando dados...")
        df_concatenado = pd.concat(processed_dfs, ignore_index=True)
        print(f"   Total: {len(df_concatenado)} registros")
        
        # Limpar dados (remover colunas com datas e IDs)
        print("\n2.5. Limpando dados...")
        df_concatenado = clean_data(df_concatenado)
        print(f"   Dados limpos: {df_concatenado.shape}")
        
        # Feature Engineering
        print("\n3. Gerando features...")
        df_features = create_features(df_concatenado)
        print(f"   Shape: {df_features.shape}")
        
        # Preparar dados para modelo
        print("\n4. Separando Train/Test e Preparando features...")
        
        # Split Train/Test (80/20)
        from sklearn.model_selection import train_test_split
        
        # Garantir que 'fase' esteja presente se for usada
        # A lista de features deve ser consistente com o modelo
        # features_cols = [c for c in df_features.columns if c != 'atingiu_pv'] # Alternativa automatica
        
        if 'atingiu_pv' in df_features.columns:
            y = df_features['atingiu_pv']
            X = df_features
            # Stratified Split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            print(f"   Train set: {X_train.shape}")
            print(f"   Test set:  {X_test.shape}")
            
            # Salvar datasets divididos
            train_path = os.path.join('data', 'train', 'train.csv')
            test_path = os.path.join('data', 'test', 'test.csv')
            
            X_train.to_csv(train_path, index=False)
            X_test.to_csv(test_path, index=False)
            print(f"   Train salvo: {train_path}")
            print(f"   Test salvo: {test_path}")
            
            # Usar apenas Train para treinar
            df_train_model = X_train # train_dropout_model espera dataframe com target e features
        else:
            X = df_features
            y = None
            df_train_model = df_features
            print("   AVISO: Target 'atingiu_pv' nao encontrado. Usando todo dataset (sem split valido).")

        # Treinar modelo
        print("\n5. Treinando modelo RandomForest (apenas com dados de treino)...")
        # Passamos apenas o conjunto de treino
        model, f1_cv, X_used = train_dropout_model(df_train_model)
        print(f"   F1-Score CV: {f1_cv:.4f}")
        
        # Salvar modelo
        print("\n6. Salvando artefatos...")
        model_path = 'app/model/model.pkl'
        save_model(model, model_path)
        
        # Salvar config
        config_data = {
            'model_type': 'RandomForestClassifier',
            'features': [col for col in X_used.columns if col in df_features.columns][:10],
            'f1_score_cv_mean': float(f1_cv),
            'sklearn_version': '1.3.0',
            'feature_count': len(X_used.columns)
        }
        config_path = 'app/model/model_config.pkl'
        joblib.dump(config_data, config_path)
        print(f"   Config salvo: {config_path}")
        
        # Recriar preprocessor
        print("\n7. Recriando preprocessor com StandardScaler...")
        preprocessor = DataPreprocessor()
        preprocessor.fit(X, y)
        
        preprocessor_path = 'app/model/preprocessor.pkl'
        joblib.dump(preprocessor, preprocessor_path)
        print(f"   Preprocessor salvo: {preprocessor_path}")
        print(f"   - Features numericas: {len(preprocessor.numerical_cols)}")
        print(f"   - Features categoricas: {len(preprocessor.categorical_cols)}")
        
        # Salvar dados processados para analise
        processed_data_path = 'src/arquivo_tratado/df_model_ready.csv'
        os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
        # Salva o dataframe de features completo (incluindo target se existir)
        df_features.to_csv(processed_data_path, index=False)
        print(f"   Dados processados salvos: {processed_data_path}")
        
        print("\n" + "="*80)
        print("[SUCESSO] MODELO RETREINADO COM SUCESSO!")
        print("="*80)
        print(f"\nArtefatos salvos em:")
        print(f"  1. {model_path}")
        print(f"  2. {config_path}")
        print(f"  3. {preprocessor_path}")
        print("\nPróximas ações:")
        print("  - Reiniciar API: python -m uvicorn app.main_simple:app --port 8002")
        print("  - Executar análise: python analise_alunos_risco.py")
        print("\n")
        
        return True
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = retrain_model()
    sys.exit(0 if success else 1)
