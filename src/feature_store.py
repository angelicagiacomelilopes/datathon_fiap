import pandas as pd

def build_feature_store(file_path):
    df = pd.read_csv(file_path)
    
    def converter_fase(val):
        val_str = str(val).upper()
        if 'ALFA' in val_str:
            return 0
        elif 'FASE' in val_str:
            digits = ''.join(filter(str.isdigit, val_str))
            return int(digits) if digits else 0
        else:
            digits = ''.join(filter(str.isdigit, val_str))
            return int(digits) if digits else 0

    df['fase'] = df['fase'].apply(converter_fase)
    
    df_2023 = df[df['ano_referencia'] == 2023].copy()
    
    alunos_2024 = set(df[df['ano_referencia'] == 2024]['ra'])
    df_2023['target_evasao'] = df_2023['ra'].apply(lambda x: 1 if x not in alunos_2024 else 0)
    
    df_2022 = df[df['ano_referencia'] == 2022].set_index('ra')
    
    df_2023['ieg_2022'] = df_2023['ra'].map(df_2022['ieg'])
    df_2023['ida_2022'] = df_2023['ra'].map(df_2022['ida'])
    
    df_2023['delta_ieg'] = (df_2023['ieg'] - df_2023['ieg_2022']).fillna(0)
    df_2023['delta_ida'] = (df_2023['ida'] - df_2023['ida_2022']).fillna(0)
    
    mapa_pedra = {
        'QUARTZO': 1, 'ÁGATA': 2, 'AMETISTA': 3, 'TOPÁZIO': 4,
        'Quartzo': 1, 'Ágata': 2, 'Ametista': 3, 'Topázio': 4
    }
    col_pedra = 'pedra_2023' if 'pedra_2023' in df_2023.columns else 'pedra_23'
    if col_pedra in df_2023.columns:
        df_2023['pedra_num'] = df_2023[col_pedra].map(mapa_pedra).fillna(0)
    else:
        df_2023['pedra_num'] = 0

    df_2023['ponto_virada'] = df_2023['atingiu_pv'].apply(lambda x: 1 if str(x).lower() in ['sim', 'true'] else 0)

    df_2023['defasagem'] = df_2023.apply(lambda row: row['idade'] - (row['fase'] + 6) if row['fase'] > 0 else 0, axis=1)

    cols_psico = ['ipp', 'ips', 'ipv', 'ian']
    for col in cols_psico:
        if col not in df_2023.columns:
            df_2023[col] = 0
            
    return df_2023.fillna(0)