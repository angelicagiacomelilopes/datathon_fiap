import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

class DataPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.pipeline = None
        self.numerical_cols = []
        self.categorical_cols = []

    def fit(self, X, y=None):
        # Identificar colunas numéricas e categóricas automaticamente se não definidas
        self.numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

        # Pipeline para variáveis numéricas
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        # Pipeline para variáveis categóricas
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        # Combinação das pipelines
        self.pipeline = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numerical_cols),
                ('cat', categorical_transformer, self.categorical_cols)
            ])

        self.pipeline.fit(X, y)
        return self

    def transform(self, X):
        return pd.DataFrame(self.pipeline.transform(X), columns=self._get_feature_names())

    def _get_feature_names(self):
        # Helper para recuperar nomes das features após OneHotEncoder
        output_features = []
        
        # Nomes das features numéricas (mantém os originais)
        if 'num' in self.pipeline.named_transformers_:
             output_features.extend(self.numerical_cols)
        
        # Nomes das features categóricas (gera novos nomes)
        if 'cat' in self.pipeline.named_transformers_:
            cat_transformer = self.pipeline.named_transformers_['cat']
            onehot = cat_transformer.named_steps['onehot']
            cat_features = onehot.get_feature_names_out(self.categorical_cols)
            output_features.extend(cat_features)
            
        return output_features

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza limpeza básica dos dados antes do processamento.
    Remove colunas irrelevantes como nomes.
    """
    df = df.copy()
    
    # Remover colunas de identificação pessoal ou irrelevantes para o modelo
    cols_to_drop = ['NOME', 'INSTITUICAO_ENSINO_ALUNO_2020', 'INSTITUICAO_ENSINO_ALUNO_2021'] 
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')
    
    return df
