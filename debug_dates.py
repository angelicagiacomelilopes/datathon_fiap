
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.preprocessing import TratamentoDados, create_features, clean_data

def debug_data():
    print("DEBUG: Checking data for date strings...")
    
    # Load raw data (just one year to be fast)
    processed_dfs = []
    for ano in [2022, 2023, 2024]:
        try:
            print(f"Loading {ano}...")
            df = pd.read_csv(f'arquivos/{ano}.csv')
            leitor = TratamentoDados(df)
            df_raw = leitor.executar_tratamento()
            processed_dfs.append(df_raw)
        except Exception as e:
            print(f"Error loading {ano}: {e}")

    df_concatenado = pd.concat(processed_dfs, ignore_index=True)
    print(f"Concatenated shape: {df_concatenado.shape}")
    
    # Apply cleaning
    df_clean = clean_data(df_concatenado)
    print(f"Cleaned shape: {df_clean.shape}")
    
    # Apply features
    df_features = create_features(df_clean)
    print(f"Features shape: {df_features.shape}")

    # Check for object columns that might contain '1/7/1900'
    print("\nChecking object columns for bad values:")
    for col in df_features.columns:
        if df_features[col].dtype == 'object':
            print(f"Column: {col}")
            # Check unique values
            uniques = df_features[col].unique()
            print(f"  Uniques (first 5): {uniques[:5]}")
            
            # Check for bad values
            if any(isinstance(x, str) and (x == 'ALFA') for x in uniques):
                print(f"  -> FOUND 'ALFA' IN: {col}")
                
            # Check for dates
            if any('1/7/1900' in str(x) for x in uniques):
                print(f"  -> FOUND DATE IN: {col}")

if __name__ == "__main__":
    debug_data()
