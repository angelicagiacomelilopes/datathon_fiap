#!/usr/bin/env python
"""
Script para identificar alunos com maior índice de evasão
Executa o modelo em todos os alunos e retorna os com maior risco
"""
import sys
import os
import pandas as pd
import joblib
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

def load_model_and_config():
    """Carrega modelo e configuração"""
    model_path = 'app/model/model.pkl'
    config_path = 'app/model/model_config.pkl'
    preprocessor_path = 'app/model/preprocessor.pkl'
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")
    
    model = joblib.load(model_path)
    config = joblib.load(config_path) if os.path.exists(config_path) else {}
    preprocessor = joblib.load(preprocessor_path) if os.path.exists(preprocessor_path) else None
    
    return model, config, preprocessor

def load_data():
    """Carrega dados de entrada"""
    data_path = 'src/arquivo_tratado/df_model_ready.csv'
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dados não encontrados: {data_path}")
    
    df = pd.read_csv(data_path)
    return df

def predict_all_students(model, config, df):
    """Executa predições para todos os alunos"""
    
    features = config.get('features', [
        'idade', 'ieg', 'ida', 'ian', 'ipp', 'ips', 'ipv', 'defasagem'
    ])
    
    # Selecionar apenas as features necessárias
    if all(f in df.columns for f in features):
        X = df[features]
    else:
        print("⚠️ Aviso: Nem todas as features estão disponíveis")
        available_features = [f for f in features if f in df.columns]
        X = df[available_features]
    
    # Fazer predições
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]  # Probabilidade de evasão (classe 1)
    
    return predictions, probabilities

def classify_risk(probability):
    """Classifica risco baseado na probabilidade"""
    if probability >= 0.7:
        return "Alto"
    elif probability >= 0.4:
        return "Médio"
    else:
        return "Baixo"

def main():
    print("\n" + "="*80)
    print("ANALISE DE RISCO DE EVASAO - TODOS OS ALUNOS")
    print("="*80 + "\n")
    
    try:
        # Carregar modelo e dados
        print("Carregando modelo e dados...")
        model, config, preprocessor = load_model_and_config()
        df = load_data()
        print(f"OK - Dados carregados: {len(df)} alunos\n")
        
        # Executar predições
        print("Executando predicoes...")
        predictions, probabilities = predict_all_students(model, config, df)
        print(f"OK - Predicoes completas\n")
        
        # Criar DataFrame de resultados
        results_df = df.copy()
        results_df['risco_evasao'] = probabilities
        results_df['classificacao'] = results_df['risco_evasao'].apply(classify_risk)
        results_df['predicao'] = predictions
        
        # Ordenar por risco de evasão (decrescente)
        results_df = results_df.sort_values('risco_evasao', ascending=False)
        
        # Estatísticas gerais
        print("📊 ESTATÍSTICAS GERAIS:")
        print("-" * 80)
        print(f"Total de alunos: {len(results_df)}")
        print(f"Alunos com Alto Risco: {len(results_df[results_df['classificacao'] == 'Alto'])} ({len(results_df[results_df['classificacao'] == 'Alto'])/len(results_df)*100:.1f}%)")
        print(f"Alunos com Médio Risco: {len(results_df[results_df['classificacao'] == 'Médio'])} ({len(results_df[results_df['classificacao'] == 'Médio'])/len(results_df)*100:.1f}%)")
        print(f"Alunos com Baixo Risco: {len(results_df[results_df['classificacao'] == 'Baixo'])} ({len(results_df[results_df['classificacao'] == 'Baixo'])/len(results_df)*100:.1f}%)")
        print(f"\nProbabilidade Média de Evasão: {results_df['risco_evasao'].mean():.2%}")
        print(f"Probabilidade Máxima: {results_df['risco_evasao'].max():.2%}")
        print(f"Probabilidade Mínima: {results_df['risco_evasao'].min():.2%}")
        
        # Top 10 alunos com maior risco
        print("\n" + "="*80)
        print("🚨 TOP 10 ALUNOS COM MAIOR RISCO DE EVASÃO")
        print("="*80)
        
        top_10 = results_df.head(10)
        
        for idx, (i, row) in enumerate(top_10.iterrows(), 1):
            print(f"\n{idx}. ALUNO #{i+1}")
            print(f"   Risco de Evasão: {row['risco_evasao']:.2%}")
            print(f"   Classificação: {row['classificacao']}")
            
            # Mostrar indicadores
            indicators = {
                'Idade': row.get('idade', 'N/A'),
                'Fase': row.get('fase', 'N/A'),
                'IEG': f"{row.get('ieg', 'N/A'):.1f}" if pd.notna(row.get('ieg')) else 'N/A',
                'IDA': f"{row.get('ida', 'N/A'):.1f}" if pd.notna(row.get('ida')) else 'N/A',
                'IAN': f"{row.get('ian', 'N/A'):.1f}" if pd.notna(row.get('ian')) else 'N/A',
                'IPP': f"{row.get('ipp', 'N/A'):.1f}" if pd.notna(row.get('ipp')) else 'N/A',
                'IPS': f"{row.get('ips', 'N/A'):.1f}" if pd.notna(row.get('ips')) else 'N/A',
                'IPV': f"{row.get('ipv', 'N/A'):.1f}" if pd.notna(row.get('ipv')) else 'N/A',
            }
            
            for key, value in indicators.items():
                print(f"   {key}: {value}")
        
        # Salvar resultados em CSV
        print("\n" + "="*80)
        output_file = 'alunos_risco_evasao.csv'
        results_df.to_csv(output_file, index=False)
        print(f"[OK] Resultados salvos em: {output_file}")
        
        # Salvar apenas alunos com alto risco
        high_risk_file = 'alunos_alto_risco.csv'
        high_risk = results_df[results_df['classificacao'] == 'Alto']
        high_risk.to_csv(high_risk_file, index=False)
        print(f"[ALERTA] Alunos com alto risco salvos em: {high_risk_file} ({len(high_risk)} alunos)")
        
        print("\n" + "="*80)
        print("[SUCESSO] ANALISE CONCLUIDA!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
