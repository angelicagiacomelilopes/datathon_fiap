from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI(
    title="Passos Mágicos Prediction API",
    version="1.0",
    description="API para previsão de risco de defasagem escolar"
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/model.pkl')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'model/model_config.pkl')

model = None
config = None

class StudentInput(BaseModel):
    idade: float
    fase: str = Field(..., description="Fase escolar")
    ieg: float
    ida: float
    ian: float
    ipp: float
    ips: float
    ipv: float
    pedra: str = Field(..., description="Classificação Pedra")
    ponto_virada: str = Field(..., description="Sim/Não")
    ieg_anterior: float = Field(0.0, description="IEG anterior")
    ida_anterior: float = Field(0.0, description="IDA anterior")

@app.on_event("startup")
def load_artifacts():
    global model, config
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        if os.path.exists(CONFIG_PATH):
            config = joblib.load(CONFIG_PATH)
    except Exception as e:
        print(f"Erro ao carregar artefatos: {e}")

@app.get("/")
def read_root():
    status = "online" if model else "offline (missing model)"
    return {
        "message": "API Passos Mágicos - Previsão de Evasão",
        "status": status,
        "version": "1.0"
    }

@app.post("/predict")
def predict_risk(student: StudentInput):
    if not model:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    try:
        pv_map = {'Sim': 1, 'SIM': 1, 'sim': 1, 'True': 1, 'true': 1, '1': 1,
                  'Nao': 0, 'NAO': 0, 'nao': 0, 'False': 0, 'false': 0, '0': 0}
        defasagem_num = pv_map.get(str(student.ponto_virada).strip(), 0)
        
        features_order = config['features'] if config else [
            'idade', 'ieg', 'ida', 'ian', 'ipp', 'ips', 'ipv', 'defasagem'
        ]
        
        X = pd.DataFrame([[
            student.idade, student.ieg, student.ida, student.ian,
            student.ipp, student.ips, student.ipv, defasagem_num
        ]], columns=features_order)
        
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]
        
        if probability >= 0.7:
            risk_level = "Alto"
        elif probability >= 0.4:
            risk_level = "Médio"
        else:
            risk_level = "Baixo"
        
        return {
            "status": "OK",
            "risk_probability": float(probability),
            "risk_classification": risk_level,
            "prediction": int(prediction),
            "message": f"Aluno com risco {risk_level.lower()} de evasão"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model else "unhealthy",
        "model_loaded": model is not None,
        "config_loaded": config is not None
    }

@app.get("/info")
def get_info():
    if not config:
        return {"error": "Configuração não disponível"}
    
    return {
        "model_type": config.get("model_type", "RandomForestClassifier"),
        "features_count": config.get("feature_count", "Unknown"),
        "f1_score_cv": config.get("f1_score_cv_mean", "Unknown"),
        "sklearn_version": config.get("sklearn_version", "1.3.0"),
        "available_endpoints": {
            "GET /": "Status da API",
            "GET /health": "Health check",
            "GET /info": "Informações do modelo",
            "POST /predict": "Fazer predição",
            "GET /docs": "Documentação (Swagger)"
        }
    }
