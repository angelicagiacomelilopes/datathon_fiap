import pandas as pd
import numpy as np

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria novas features a partir dos dados existentes.
    """
    df = df.copy()
    
    # Feature Engineering: Comparação entre anos
    # Variação do INDE (se existirem colunas de diferentes anos)
    if 'INDE_2021' in df.columns and 'INDE_2020' in df.columns:
        df['DELTA_INDE_20_21'] = df['INDE_2021'] - df['INDE_2020']
    
    if 'INDE_2022' in df.columns and 'INDE_2021' in df.columns:
        df['DELTA_INDE_21_22'] = df['INDE_2022'] - df['INDE_2021']

    # Converter colunas booleanas/string para int de forma robusta
    # Exemplo: PONTO_VIRADA_2020
    for col in df.columns:
        if 'PONTO_VIRADA' in col or 'BOLSISTA' in col:
            df[col] = df[col].astype(str).apply(lambda x: 1 if x.lower() in ['sim', 'true', '1', 's'] else 0)

    # Tratamento de Pedras para numérico (Label Encoding manual para manter ordem)
    pedra_map = {'Quartzo': 1, 'Ágata': 2, 'Ametista': 3, 'Topázio': 4}
    for col in df.columns:
        if 'PEDRA' in col:
            df[f'{col}_NUM'] = df[col].map(pedra_map).fillna(0)

    return df
