import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import logging
import sys
import os

# Adicionar o diretório pai ao system path para permitir importações relativas quando rodar como script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_data, save_model
from src.preprocessing import clean_data, DataPreprocessor
from src.feature_engineering import create_features

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações
# Caminho absoluto para garantir que encontre o arquivo
DATA_PATH = r'c:\Users\Angélica\Desktop\datathon\BASE DE DADOS PEDE 2024 - DATATHON.xlsx'
TARGET_COL = 'PONTO_VIRADA_2022'  # Ajustar conforme o objetivo do modelo (ex: 'Ficou_De_Recuperacao')

def train_model():
    logger.info("Iniciando pipeline de treinamento...")
    
    # 1. Carregar dados
    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError:
        logger.error(f"Arquivo de dados não encontrado em {DATA_PATH}")
        return

    # 2. Limpeza
    df_clean = clean_data(df)
    
    # 3. Feature Engineering
    df_features = create_features(df_clean)
    
    # Definir Target
    # Verificação simples para garantir que a coluna target existe
    if TARGET_COL not in df_features.columns:
        logger.warning(f"Target '{TARGET_COL}' não encontrado no dataset. Tentando identificar um target alternativo...")
        # Lógica de fallback ou erro
        # Se não tiver 2022, tenta 2021
        if 'PONTO_VIRADA_2021' in df_features.columns:
            target = 'PONTO_VIRADA_2021'
            logger.info(f"Usando target alternativo: {target}")
        else:
            logger.error("Nenhum target válido encontrado. Abortando.")
            return
    else:
        target = TARGET_COL

    # Remover linhas com target nulo
    df_model = df_features.dropna(subset=[target])
    
    # Separar X e y
    X = df_model.drop(columns=[target])
    y = df_model[target]
    
    # Garantir que y é numérico (0 ou 1) se for classificação
    y = y.astype(int)

    # 4. Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Preprocessamento (Fit no treino)
    preprocessor = DataPreprocessor()
    preprocessor.fit(X_train, y_train)
    
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # 6. Treinamento
    # Exemplo com RandomForest
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train_processed, y_train)
    
    # 7. Avaliação rápida
    logger.info("Avaliando modelo...")
    y_pred = model.predict(X_test_processed)
    acc = accuracy_score(y_test, y_pred)
    logger.info(f"Acurácia: {acc:.4f}")
    logger.info("\n" + classification_report(y_test, y_pred))
    
    # 8. Salvar Modelo e Preprocessor
    # Cria pasta se não existir
    os.makedirs('app/model', exist_ok=True)
    
    save_model(model, 'app/model/model.pkl')
    save_model(preprocessor, 'app/model/preprocessor.pkl')
    
    logger.info("Pipeline finalizada com sucesso.")

if __name__ == "__main__":
    train_model()
