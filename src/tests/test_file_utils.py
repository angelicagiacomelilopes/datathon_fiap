import pytest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import MagicMock, patch

# Adjust path to find src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.file_utils import FileUtils, TratamentoDados

# --- Mocking Logger to avoid creating files during tests ---
@pytest.fixture(autouse=True)
def mock_logger():
    with patch('src.file_utils.LoggerConfig'), \
         patch('src.file_utils.ApplicationLogger') as MockLogger:
        # Configure the mock to have a .logger attribute that is also a mock
        instance = MockLogger.return_value
        instance.logger = MagicMock()
        instance.log_method_call = MagicMock()
        yield instance

# --- Tests for FileUtils ---

class TestFileUtils:
    def test_init(self):
        fu = FileUtils(name="TestApp", caminho="dummy.xlsx", aba="Sheet1")
        assert fu.caminho == "dummy.xlsx"
        assert fu.aba == "Sheet1"

    @patch('pandas.read_excel')
    @patch('os.path.exists')
    def test_ler_arquivo_xlsx_sucesso(self, mock_exists, mock_read_excel):
        mock_exists.return_value = True
        
        # Mock DataFrame return
        df_mock = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_excel.return_value = df_mock
        
        fu = FileUtils(caminho="dados.xlsx", aba="PEDE2023")
        df_result = fu.ler_arquivo()
        
        mock_read_excel.assert_called_once()
        # Verify if ano_referencia was created based on tab name
        assert 'ano_referencia' in df_result.columns
        assert df_result['ano_referencia'].iloc[0] == "2023"

    @patch('os.path.exists')
    def test_ler_arquivo_nao_encontrado(self, mock_exists):
        mock_exists.return_value = False
        fu = FileUtils(caminho="ghost.xlsx", aba="Sheet1")
        with pytest.raises(FileNotFoundError):
            fu.ler_arquivo()

    @patch('os.path.exists')
    def test_ler_arquivo_formato_invalido(self, mock_exists):
        mock_exists.return_value = True
        fu = FileUtils(caminho="dados.txt", aba="Sheet1")
        with pytest.raises(ValueError, match="Formato de arquivo não suportado"):
            fu.ler_arquivo()

    @patch('joblib.dump')
    @patch('os.makedirs')
    def test_save_model(self, mock_makedirs, mock_dump):
        fu = FileUtils()
        model = MagicMock()
        fu.save_model(model, "models/model.pkl")
        
        mock_makedirs.assert_called_once()
        mock_dump.assert_called_once_with(model, "models/model.pkl")

    @patch('joblib.load')
    @patch('os.path.exists')
    def test_load_model_sucesso(self, mock_exists, mock_load):
        mock_exists.return_value = True
        mock_load.return_value = "dummy_model"
        
        fu = FileUtils()
        model = fu.load_model("models/model.pkl")
        
        assert model == "dummy_model"
        mock_load.assert_called_once_with("models/model.pkl")

    @patch('os.path.exists')
    def test_load_model_nao_encontrado(self, mock_exists):
        mock_exists.return_value = False
        fu = FileUtils()
        with pytest.raises(FileNotFoundError):
            fu.load_model("models/ghost.pkl")

# --- Tests for TratamentoDados ---

class TestTratamentoDados:
    
    @pytest.fixture
    def df_raw(self):
        """Creates a raw DataFrame simulating typical input data"""
        data = {
            'Nome': ['Alice', 'Bob', 'Charlie'],
            'Gênero': ['Menina', 'Masculino', 'Menino'],
            'Idade 22': [10, 11, 10],  # Will be renamed to 'idade'
            'INDE 23': ['8,5', '7.0', 6.5], # Mixed types for decimal conversion
            'Data de Nasc': ['15/05/2012', '2011-10-20', '01/01/2012'], # Mixed date formats
            'Duplicada': [1, 2, 3],
            'Duplicada.1': [1, 2, 3], # Exact duplicate
            'Nota': [10, 9, 8],
            'ano_referencia': ['2023', '2023', '2023'] # Needed for idade calc
        }
        return pd.DataFrame(data)

    def test_remover_colunas_duplicadas(self, df_raw):
        td = TratamentoDados(df_raw.copy(), ano="2023")
        td._remover_colunas_duplicadas()
        
        # Should remove 'Duplicada.1' as it matches 'Duplicada'
        assert 'Duplicada.1' not in td.df.columns
        assert 'Duplicada' in td.df.columns
        
        # Ensure it didn't remove non-duplicates
        assert 'Nome' in td.df.columns

    def test_padronizar_colunas(self, df_raw):
        td = TratamentoDados(df_raw.copy(), ano="2023")
        td._padronizar_colunas()
        
        # Check renames based on DICTIONARY_MAPPING
        # "Gênero" -> "genero"
        assert 'genero' in td.df.columns
        assert 'Gênero' not in td.df.columns
        
        # "Idade 22" -> "idade"
        assert 'idade' in td.df.columns
        
        # "INDE 23" -> "inde_23"
        assert 'inde_23' in td.df.columns
        
        # "Data de Nasc" -> "data_nascimento"
        assert 'data_nascimento' in td.df.columns
        
        # "Nome" should remain or match if in dict (Nome isn't in the snippet provided but usually stays if not mapped orMapped to itself)
        # Check mapping logic: unmapped columns stay as is? 
        # The implementation keeps unmapped columns.

    def test_converter_decimal_ptbr(self):
        data = {
            'inde_23': ['8,50', '9,10', 7.5, 'invalid'],
            'ips': ['1.000,50', '500,00', None, np.nan]
        }
        df = pd.DataFrame(data)
        
        # Mock class to use constants
        # In actual code, COLUNAS_DECIMAIS contains 'inde_23', 'ips' etc.
        # We need to ensure the columns tested are in TratamentoDados.COLUNAS_DECIMAIS
        
        td = TratamentoDados(df, ano="2023")
        # Force COLUNAS_DECIMAIS for test if needed, or rely on real class
        # Assuming class has 'inde_23' and 'ips' in list. 
        # Let's verify via the real list or mock it if minimal.
        
        # Run conversion
        td._converter_decimal_ptbr()
        
        # Check 'inde_23'
        assert td.df['inde_23'].iloc[0] == 8.5
        assert td.df['inde_23'].iloc[1] == 9.1
        assert td.df['inde_23'].iloc[2] == 7.5
        assert pd.isna(td.df['inde_23'].iloc[3])
        
        # Check 'ips' (1.000,50 -> 1000.5)
        # Assuming conversion logic handles thousand separators if present
        assert td.df['ips'].iloc[0] == 1000.5
        assert td.df['ips'].iloc[1] == 500.0

    def test_converter_colunas_data(self):
        data = {
            'data_nascimento': ['15/08/2012', '2012-08-15', '12/31/2012', 'invalid'] # BR format, ISO, US format (potentially)
        }
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        td._converter_colunas_data()
        
        # 15/08/2012 -> 2012-08-15
        assert td.df['data_nascimento'].iloc[0] == pd.Timestamp('2012-08-15')
        # 2012-08-15 -> 2012-08-15
        assert td.df['data_nascimento'].iloc[1] == pd.Timestamp('2012-08-15')
        # 12/31/2012 -> 2012-12-31 (US format fallback)
        assert td.df['data_nascimento'].iloc[2] == pd.Timestamp('2012-12-31')
        # invalid -> NaT
        assert pd.isna(td.df['data_nascimento'].iloc[3])

    def test_tratar_campo_parametrizado_genero(self):
        data = {'genero': ['Menina', 'Menino', 'Feminino', 'Masculino', 'Outro']}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        td.aba_ano_referencia = "2023" # Mock metadata
        
        td._tratar_campo_parametrizado(['genero'])
        
        values = td.df['genero'].tolist()
        expected = ['Feminino', 'Masculino', 'Feminino', 'Masculino', 'outro']
        assert values == expected

    def test_tratar_campo_parametrizado_idade(self):
        data = {
            'ano_nasc': [2010, 2011, np.nan],
            'ano_referencia': [2023, 2023, 2023]
        }
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        # ano_referencia is normally added by FileUtils, so we added it manually to df
        
        td._tratar_campo_parametrizado(['idade'])
        
        assert td.df['idade'].iloc[0] == 13 # 2023 - 2010
        assert td.df['idade'].iloc[1] == 12 # 2023 - 2011
        assert pd.isna(td.df['idade'].iloc[2])

    def test_ordenar_colunas(self):
        data = {'B': [1], 'A': [2], 'C': [3]}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        td._ordenar_colunas()
        assert td.df.columns.tolist() == ['A', 'B', 'C']

    def test_converter_decimal_sem_colunas(self):
        # Case where no decimal columns exist in DF
        df = pd.DataFrame({'outra': [1, 2]})
        td = TratamentoDados(df, ano="2023")
        td._converter_decimal_ptbr() 
        # Check logs/execution, mainly no error
        assert 'outra' in td.df.columns

    def test_converter_data_sem_colunas(self):
        # Case where no date columns exist in DF
        df = pd.DataFrame({'outra': [1, 2]})
        td = TratamentoDados(df, ano="2023")
        td._converter_colunas_data()
        assert 'outra' in td.df.columns

    def test_tratar_campo_criado_parametrizado_ano_nasc_from_data(self):
        # Create ano_nasc from data_nascimento
        data = {'data_nascimento': ['2012-05-15', '2011-10-20']}
        df = pd.DataFrame(data)
        # Ensure data_nascimento is datetime to trigger first branch
        df['data_nascimento'] = pd.to_datetime(df['data_nascimento'])
        
        td = TratamentoDados(df, ano="2023")
        # Call directly
        td._tratar_campo_criado_parametrizado('ano_nasc')
        
        assert 'ano_nasc' in td.df.columns
        # dt.year returns int, but logic converts to str? 
        # Code: self.df[campo] = self.df['data_nascimento'].dt.year.str (This looks suspicious in source code "dt.year.str"?? dt.year is Series[int], .str accessor might fail if not cast to string first)
        # Wait, let's check source code line 465: `self.df['data_nascimento'].dt.year.str`
        # Actually `dt.year` returns integers (or floats if NaNs). `Series.str` is for string manipulation. 
        # `dt.year` -> Series(int). `.str` accessor -> AttributeError usually unless it's string.
        # Maybe it meant `astype(str)`? 
        
        # NOTE: If the source code has a bug here, the test will reveal it.
        # Let's see if the test fails. if so, I fix the source code too.
        
        # Also test with string date to hit the 'else' branch in _tratar_campo_criado_parametrizado
        
    def test_tratar_campo_criado_parametrizado_data_from_ano(self):
        # Create data_nascimento from ano_nasc
        data = {'ano_nasc': [2012, 2011]}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        td._tratar_campo_criado_parametrizado('data_nascimento')
        
        assert 'data_nascimento' in td.df.columns
        assert td.df['data_nascimento'].iloc[0] == pd.Timestamp('2012-01-01')


    def test_remover_colunas_duplicadas_diferentes(self):
        # Case where name is similar (suffix) but content differs
        data = {'Col': [1, 2], 'Col.1': [3, 4]}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        td._remover_colunas_duplicadas()
        
        # Should keep both (Col.1 might be renamed or kept as is, logic says kept with warning)
        assert 'Col' in td.df.columns
        assert 'Col.1' in td.df.columns

    def test_converter_tipos_falha(self):
        # Force conversion error
        data = {'col_fail': ['abc', 'def']}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        with patch.object(TratamentoDados, 'SCHEMA_DTYPES', {'col_fail': int}):
            td._converter_tipos()
            
        assert td.df['col_fail'].iloc[0] == 'abc'

    def test_converter_tipos(self):
        data = {
            'ra': [123, 456], # int to str
            'fase': ['A', 'B'],
            'col_extra': [1, 2] # Not in schema, should be ignored
        }
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        td._converter_tipos()
        
        assert pd.api.types.is_string_dtype(td.df['ra'])
        assert td.df['ra'].iloc[0] == '123'
    
    def test_converter_tipos_coluna_ausente_criacao(self):
        # Checks if missing columns in SCHEMA_DTYPES are created (via _tratar_campo_criado_parametrizado logic)
        data = {'ra': ['1']}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        with patch.object(TratamentoDados, 'SCHEMA_DTYPES', {'nova_coluna': str}):
             td._converter_tipos()
             assert 'nova_coluna' in td.df.columns
             assert pd.isna(td.df['nova_coluna'].iloc[0])

    def test_converter_valor_decimal_erro(self):
         # Test error handling in decimal conversion
         data = {'inde_23': ['bad_value']} # Not numeric, not recognizable format
         df = pd.DataFrame(data)
         td = TratamentoDados(df, ano="2023")
         
         td._converter_decimal_ptbr() 
         # Should become NaN
         assert pd.isna(td.df['inde_23'].iloc[0])

    def test_pipeline_completo(self):
        data = {
            'Nome': ['Aluno 1'],
            'Gênero': ['Menino'],
            'INDE 23': ['8,5'],
            'ano_referencia': [2023] # Simulating extra col
        }
        df = pd.DataFrame(data)
        
        # Needs to ensure columns in data map to something valid or test won't cover much
        # We rely on defaults in DICTIONARY_MAPPING
        
        td = TratamentoDados(df, ano="2023")
        df_final = td.executar_tratamento()
        
        assert 'genero' in df_final.columns
        assert df_final['genero'].iloc[0] == 'Masculino'
        assert df_final['inde_23'].iloc[0] == 8.5
        
        # Check sorting
        cols = df_final.columns.tolist()
        assert cols == sorted(cols)

    def test_converter_colunas_data_sem_colunas(self):
        df = pd.DataFrame({'a': [1]})
        td = TratamentoDados(df, ano="2023")
        with patch.object(TratamentoDados, 'COLUNAS_DATA', ['nao_existe']):
            with patch.object(td.logger.logger, 'info') as mock_info:
                td._converter_colunas_data()
                # Verify logging call - "Nenhuma coluna de data encontrada..."
                assert any("Nenhuma coluna de data encontrada" in str(c) for c in mock_info.call_args_list)

    def test_converter_colunas_data_fallback(self):
        # Create a mock that raises ValueError on first call (dates_br with format='mixed')
        df = pd.DataFrame({'data': ['01/01/2023']})
        td = TratamentoDados(df, ano="2023")
        
        original_to_datetime = pd.to_datetime
        
        def side_effect(*args, **kwargs):
            # If format='mixed' is passed (1st try), raise ValueError mock
            if 'format' in kwargs and kwargs['format'] == 'mixed':
                raise ValueError("Mock Error")
            return original_to_datetime(*args, **kwargs)

        with patch.object(TratamentoDados, 'COLUNAS_DATA', ['data']):
             with patch('pandas.to_datetime', side_effect=side_effect):
                 td._converter_colunas_data()
                 assert pd.api.types.is_datetime64_any_dtype(td.df['data'])
                 assert td.df['data'].iloc[0].year == 2023

    def test_tratar_campo_parametrizado_genero(self):
        data = {'genero': [' Masculino ', 'menina', 'Outro']}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        td._tratar_campo_parametrizado(['genero'])
        
        expected = ['Masculino', 'Feminino', 'outro']
        assert td.df['genero'].tolist() == expected

    def test_tratar_campo_parametrizado_idade_vazio(self):
         df = pd.DataFrame({'outra_col': [1], 'ano_referencia': [2023]})
         td = TratamentoDados(df, ano="2023")
         
         # Should verify it warns and doesn't crash when ano_nasc/data_nascimento missing
         with patch.object(td.logger.logger, 'warning') as mock_warning:
             td._tratar_campo_parametrizado(['idade'])
             assert any("Campos 'ano_nasc' e 'data_nascimento' vazios" in str(c) for c in mock_warning.call_args_list)

    def test_converter_colunas_data_mixed_formats(self):
        # "20/05/2023" (DD/MM/YYYY) and "05/25/2023" (MM/DD/YYYY - 25th month is invalid, so 25 is day)
        # Wait, 05/25/2023: If BR (DayFirst), Day=05, Month=25 (Error). NaT.
        # Fallback US (DayFirst=False): Month=05, Day=25. Success.
        data = {'data': ['20/05/2023', '05/25/2023']}
        df = pd.DataFrame(data)
        td = TratamentoDados(df, ano="2023")
        
        with patch.object(TratamentoDados, 'COLUNAS_DATA', ['data']):
            td._converter_colunas_data()
            
            assert pd.notna(td.df['data']).all()
            assert td.df['data'].iloc[0].month == 5
            assert td.df['data'].iloc[0].day == 20
            
            assert td.df['data'].iloc[1].month == 5
            assert td.df['data'].iloc[1].day == 25

    def test_converter_decimal_value_error(self):
        td = TratamentoDados(pd.DataFrame(), "2023")
        val = td._converter_valor_decimal("abc") # float("abc") raises ValueError
        assert pd.isna(val)

