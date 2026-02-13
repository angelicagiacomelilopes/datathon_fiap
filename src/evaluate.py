import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import load_data, load_model
from src.preprocessing import clean_data, DataPreprocessor
from src.feature_engineering import create_features

# Reutilizar constantes (idealmente estariam num config.py)
DATA_PATH = r'c:\Users\Angélica\Desktop\datathon\BASE DE DADOS PEDE 2024 - DATATHON.xlsx'
TARGET_COL = 'PONTO_VIRADA_2022'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def evaluate_model():
    logger.info("Iniciando avaliação do modelo...")
    
    # Carregar modelo e preprocessor
    try:
        model = load_model('app/model/model.pkl')
        preprocessor = load_model('app/model/preprocessor.pkl')
    except Exception as e:
        logger.error(f"Erro ao carregar modelos: {e}")
        logger.error("Certifique-se de que executou src/train.py primeiro.")
        return

    # Carregar dados
    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError:
        logger.error("Arquivo de dados original não encontrado para avaliação.")
        return

    df_clean = clean_data(df)
    df_features = create_features(df_clean)
    
    # Target Handling
    if TARGET_COL not in df_features.columns:
        if 'PONTO_VIRADA_2021' in df_features.columns:
            target = 'PONTO_VIRADA_2021'
        else:
            logger.error("Coluna alvo não encontrada.")
            return
    else:
        target = TARGET_COL
        
    df_model = df_features.dropna(subset=[target])
    X = df_model.drop(columns=[target])
    y = df_model[target].astype(int)

    # Recriar o split para obter o conjunto de teste (mesmo random_state de train.py)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Transformar dados
    try:
        X_test_processed = preprocessor.transform(X_test)
    except Exception as e:
        logger.error(f"Erro ao preprocessar dados de teste: {e}")
        return
    
    # Previsões
    y_pred = model.predict(X_test_processed)
    
    # Métricas
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    logger.info(f"--- Resultados da Avaliação ---")
    logger.info(f"Acurácia: {acc:.4f}")
    
    try:
        y_proba = model.predict_proba(X_test_processed)[:, 1]
        auc = roc_auc_score(y_test, y_proba)
        logger.info(f"AUC-ROC: {auc:.4f}")
    except:
        pass

    logger.info("\nRelatório de Classificação:\n" + report)
    logger.info("\nMatriz de Confusão:\n" + str(cm))
    
    # Salvar métricas (opcional)
    # with open('metrics.txt', 'w') as f: f.write(report)

if __name__ == "__main__":
    evaluate_model()
