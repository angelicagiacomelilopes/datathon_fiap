
import pandas as pd
import numpy as np
import sys
import os

# Adicionar caminho src para importar file_utils
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
try:
    from file_utils import TratamentoDados, FileUtils
except ImportError:
    # Caso esteja rodando de dentro de src
    sys.path.append(os.getcwd())
    from file_utils import TratamentoDados, FileUtils

def normalize_decimal(val):
    if pd.isna(val) or val == '':
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)
    try:
        val_str = str(val).replace('.', '').replace(',', '.')
        return float(val_str)
    except:
        return np.nan

def compare_dataframes(year, df_orig, df_treated):
    print(f"\n{'='*20} Comparando Ano {year} {'='*20}")
    
    # Normalizar df_orig columns para string (caso venha int do excel as vezes)
    df_orig.columns = df_orig.columns.astype(str)

    print(f"Shape Original: {df_orig.shape}")
    print(f"Shape Tratado:  {df_treated.shape}")
    
    # Validar número de linhas
    if len(df_orig) != len(df_treated):
        print(f"ALERTA: Número de linhas diferente! Orig: {len(df_orig)}, Trat: {len(df_treated)}")
        # Tentar cortar pelo menor para fins de comparação
        min_len = min(len(df_orig), len(df_treated))
        df_orig = df_orig.iloc[:min_len]
        df_treated = df_treated.iloc[:min_len]
    
    # Construir mapa Original -> Padrão (invertendo o do TratamentoDados)
    map_orig_to_std = {}
    for std, variations in TratamentoDados.DICTIONARY_MAPPING['columns'].items():
        for var in variations:
            map_orig_to_std[var] = std

    print("\n--- Validação de Colunas ---")
    
    passed = []

    for col_orig in df_orig.columns:
        # Determinar nome esperado no tratado
        col_expected = map_orig_to_std.get(col_orig, col_orig)
        
        # Verificar se está no tratado
        if col_expected not in df_treated.columns:
            # Coluna pode ter sido removida ou não mapeada
            continue
            
        # Validação de Dados
        series_orig = df_orig[col_orig]
        series_treated = df_treated[col_expected]
        
        is_decimal = col_expected in TratamentoDados.COLUNAS_DECIMAIS
        is_date = col_expected in TratamentoDados.COLUNAS_DATA
        is_gender = col_expected == 'genero'
        
        total_count = len(series_orig)
        
        if is_decimal:
            # Converter original para float 
            orig_float = series_orig.apply(normalize_decimal)
            treated_float = series_treated.apply(normalize_decimal) 
            
            # Comparar com tolerancia (atol=0.01 para suportar INDE 7.61 vs 8)
            # Na verdade INDE 7.6 vs 8 falharia com 0.01, mass se estamos lendo do Excel
            # A expectativa é que sejam IGUAIS (High precision vs High precision)
            equals = np.isclose(orig_float.fillna(-999999), treated_float.fillna(-999999), rtol=1e-05, atol=0.01)
            
            mask_both_nan = orig_float.isna() & treated_float.isna()
            equals = equals | mask_both_nan
            
            match_percentage = equals.sum() / total_count * 100
            if match_percentage < 99.0:
                 print(f"DECIMAL DIFERENÇA: '{col_orig}' -> '{col_expected}': {match_percentage:.2f}% match")
            else:
                passed.append(col_orig)
        
        elif is_date:
            # Tenta converter orig 
            orig_dt = pd.to_datetime(series_orig, errors='coerce')
            
            # Se falhar (ex: Excel leu como string ou veio CSV), tenta formatos
            if orig_dt.isna().all() and series_orig.notna().any():
                 orig_dt_br = pd.to_datetime(series_orig, dayfirst=True, errors='coerce')
                 orig_dt_us = pd.to_datetime(series_orig, dayfirst=False, errors='coerce')
                 orig_dt = orig_dt_br.fillna(orig_dt_us)

            # Tratado (CSV) YYYY-MM-DD
            treat_dt = pd.to_datetime(series_treated, errors='coerce')
            
            dummy = pd.Timestamp("1900-01-01")
            equals = (orig_dt.fillna(dummy) == treat_dt.fillna(dummy))
            match_percentage = equals.sum() / total_count * 100
            
            if match_percentage < 99.0:
                 print(f"DATA DIFERENÇA:    '{col_orig}' -> '{col_expected}': {match_percentage:.2f}% match")
            else:
                passed.append(col_orig)

        elif is_gender:
            # Normalizar genero
            s_orig = series_orig.astype(str).str.strip().str.lower()
            s_treat = series_treated.astype(str).str.strip().str.lower()
            
            map_gender = {
                'menina': 'feminino', 'menino': 'masculino',
            }
            s_orig = s_orig.replace(map_gender)
            s_treat = s_treat.replace(map_gender) 
            
            # Tratar nan strings
            s_orig = s_orig.replace({'nan': '', 'none': '', 'nan': ''})
            s_treat = s_treat.replace({'nan': '', 'none': '', 'nan': ''})

            equals = (s_orig == s_treat)
            match_percentage = equals.sum() / total_count * 100
            if match_percentage < 99.0:
                 print(f"GENERO DIFERENÇA:  '{col_orig}' -> '{col_expected}': {match_percentage:.2f}% match")
            else:
                passed.append(col_orig)

        else:
            # String genérica
            s_orig = series_orig.astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            s_treat = series_treated.astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
            
            s_orig = s_orig.replace({'nan': '', 'None': '', 'NaN': ''})
            s_treat = s_treat.replace({'nan': '', 'None': '', 'NaN': ''})
            
            equals = (s_orig == s_treat)
            match_percentage = equals.sum() / total_count * 100
            
            if match_percentage < 99.0: 
                 print(f"VALOR DIFERENÇA:   '{col_orig}' -> '{col_expected}': {match_percentage:.2f}% match")
            else:
                passed.append(col_orig)

    print(f"\n[OK] {len(passed)} colunas validadas com sucesso.")
    print(f"Verificação de colunas concluída para {year}.")

def main():
    excel_path = r"C:\Users\Angélica\Desktop\datathon\projeto_datathon\arquivos\BASE DE DADOS PEDE 2024 - DATATHON.xlsx"
    base_path_treat = r"C:\Users\Angélica\Desktop\datathon\projeto_datathon\src\logs\tratamentodados"

    years = ['2022', '2023', '2024']
    
    for year in years:
        # Tenta carregar do Excel para garantir fidelidade com o Pipeline
        df_orig = None
        if os.path.exists(excel_path):
            try:
                print(f"\nCarregando original do Excel (Aba PEDE{year})...")
                reader = FileUtils(caminho=excel_path, aba=f"PEDE{year}")
                df_orig = reader.ler_arquivo()
            except Exception as e:
                print(f"Erro ao carregar Excel para {year}: {e}")
        
        if df_orig is None:
             print("Excel falhou ou não existe. Tentando CSVs antigos...")
             base_path_orig = r"C:\Users\Angélica\Desktop\datathon\projeto_datathon\arquivos"
             file_orig = os.path.join(base_path_orig, f"{year}.csv")
             try:
                 df_orig = pd.read_csv(file_orig, sep=';' if year=='2022' else ',')
                 if len(df_orig.columns) <= 1:
                     df_orig = pd.read_csv(file_orig, sep=',')
             except Exception as e:
                 print(f"Erro ao ler CSV {year}: {e}")
                 continue

        file_treat = os.path.join(base_path_treat, f"df_tratado_{year}.csv")
        
        if os.path.exists(file_treat):
            # Ler tratado
            df_treated = pd.read_csv(file_treat)
            compare_dataframes(year, df_orig, df_treated)
        else:
            print(f"Arquivo tratado não encontrado: {file_treat}")

if __name__ == "__main__":
    main()
