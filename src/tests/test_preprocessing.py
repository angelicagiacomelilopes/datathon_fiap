import pytest
import pandas as pd
import numpy as np
import sys
import os

# Ajuste de path para encontrar o módulo src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.preprocessing import clean_data, DataPreprocessor

def test_clean_data():
    df = pd.DataFrame({
        'NOME': ['João', 'Maria'],
        'IDADE': [10, 12],
        'INSTITUICAO_ENSINO_ALUNO_2020': ['Escola A', 'Escola B']
    })
    
    df_clean = clean_data(df)
    
    # Verifica se colunas sensíveis foram removidas
    assert 'NOME' not in df_clean.columns
    assert 'INSTITUICAO_ENSINO_ALUNO_2020' not in df_clean.columns
    assert 'IDADE' in df_clean.columns

def test_data_preprocessor():
    df = pd.DataFrame({
        'NUM_COL': [1.0, 2.0, np.nan],
        'CAT_COL': ['A', 'B', 'A']
    })
    
    preprocessor = DataPreprocessor()
    preprocessor.fit(df)
    transformed = preprocessor.transform(df)
    
    # Verifica dimensões
    assert transformed.shape[0] == 3
    
    # Verifica se a imputação numérica funcionou (sem NaNs)
    assert not transformed.isnull().values.any()
    
    # Verifica colunas expected
    # Esperamos NUM_COL e one-hot cols para CAT_COL
    cols = transformed.columns.tolist()
    assert 'NUM_COL' in cols
    # Verifica se existe alguma coluna derivada de CAT_COL
    assert any('CAT_COL' in c for c in cols)
