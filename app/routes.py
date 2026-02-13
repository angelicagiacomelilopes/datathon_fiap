from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import sys

# Garantir que src seja importável
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.preprocessing import clean_data, DataPreprocessor # DataPreprocessor precisa estar disponível para o pickle carregar a classe
from src.feature_engineering import create_features

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/model.pkl')
PREPROC_PATH = os.path.join(os.path.dirname(__file__), 'model/preprocessor.pkl')

model = None
preprocessor = None

def load_artifacts():
    global model, preprocessor
    if model is None:
        if os.path.exists(MODEL_PATH) and os.path.exists(PREPROC_PATH):
            model = joblib.load(MODEL_PATH)
            preprocessor = joblib.load(PREPROC_PATH)
        else:
            # Em produção, isso deveria logar um erro crítico, mas não crashar import
            print(f"Modelos não encontrados em {MODEL_PATH}")

class StudentData(BaseModel):
    # Aceita um dicionário livre para flexibilidade com as colunas do dataset
    # Exemplo: {"INDE_2020": 7.5, "PEDRA_2020": "Ametista", ...}
    data: dict

@router.on_event("startup")
async def startup_event():
    load_artifacts()

@router.get("/")
def read_root():
    return {"message": "API de Previsão Passos Mágicos está online."}

@router.post("/predict")
def predict(student: StudentData):
    global model, preprocessor
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado ou não encontrado.")

    try:
        # Converter input para DataFrame
        df = pd.DataFrame([student.data])
        
        # 1. Limpeza
        df_clean = clean_data(df)
        
        # 2. Engenharia de Features
        df_features = create_features(df_clean)
        
        # 3. Transformação
        # O preprocessor espera as colunas usadas no treino. 
        # Se 'create_features' gerar colunas que não existiam no input, ok.
        X_processed = preprocessor.transform(df_features)
        
        # 4. Predição
        prediction = model.predict(X_processed)
        
        try:
            proba = model.predict_proba(X_processed).tolist()
        except:
            proba = None
        
        return {
            "prediction": int(prediction[0]),
            "probability": proba[0] if proba else None,
            "defasagem_risk": "Alto" if prediction[0] == 0 else "Baixo" # Ajustar lógica conforme target
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")
