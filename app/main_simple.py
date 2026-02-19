from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/model.pkl')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'model/model_config.pkl')
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), 'model/preprocessor.pkl')

model = None
config = None
preprocessor = None

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
    global model, config, preprocessor
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print(f"[OK] Modelo carregado: {MODEL_PATH}")
        if os.path.exists(CONFIG_PATH):
            config = joblib.load(CONFIG_PATH)
            print(f"[OK] Config carregada: {CONFIG_PATH}")
        if os.path.exists(PREPROCESSOR_PATH):
            preprocessor = joblib.load(PREPROCESSOR_PATH)
            print(f"[OK] Preprocessor carregado: {PREPROCESSOR_PATH}")
        else:
            print(f"[AVISO] Preprocessor nao encontrado: {PREPROCESSOR_PATH}")
    except Exception as e:
        print(f"Erro ao carregar artefatos: {e}")

@app.get("/")
def read_root():
    html_path = os.path.join(os.path.dirname(__file__), 'index.html')
    if os.path.exists(html_path):
        return FileResponse(html_path, media_type="text/html")
    
    status = "online" if model else "offline (missing model)"
    return {
        "message": "API Passos Mágicos - Previsão de Evasão",
        "status": status,
        "version": "1.0",
        "note": "Frontend HTML não encontrado"
    }

@app.post("/predict")
def predict_risk(student: StudentInput):
    if not model:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    try:
        # Mapeamento de Pedra
        pedra_map = {'quartzo': 0, 'ágata': 1, 'agata': 1, 'ametista': 2, 'topázio': 3, 'topazio': 3}
        pedra_num = pedra_map.get(str(student.pedra).strip().lower(), 0) # Default Quartzo

        # Mapeamento Ponto de Virada (Sim/Não -> 1/0)
        pv_map = {'sim': 1, 's': 1, 'true': 1, '1': 1, 'nao': 0, 'não': 0, 'n': 0, 'false': 0, '0': 0}
        pv_num = pv_map.get(str(student.ponto_virada).strip().lower(), 0)
        
        # Tratamento de Fase (converter para numérico se possível)
        try:
            fase_num = float(student.fase)
        except:
            fase_num = 0.0

        # Dicionário completo de features disponíveis
        features_dict = {
            'idade': student.idade,
            'fase': fase_num,
            'ieg': student.ieg,
            'ida': student.ida,
            'ian': student.ian,
            'ipp': student.ipp,
            'ips': student.ips,
            'ipv': student.ipv,
            'pedra_num': pedra_num,
            'ponto_virada': pv_num,
            'defasagem': pv_num, # defasagem muitas vezes é correlacionada ou usada similarmente
            'delta_ieg': student.ieg - student.ieg_anterior,
            'delta_ida': student.ida - student.ida_anterior
        }

        # Obter a ordem correta das features do modelo
        # Se não houver config, usamos fallback, mas idealmente deve vir do config
        model_features = config['features'] if config and 'features' in config else [
             'idade', 'fase', 'ieg', 'ida', 'ian', 'ipp', 'ips', 'ipv', 
             'delta_ieg', 'delta_ida', 'pedra_num', 'ponto_virada', 'defasagem'
        ]
        
        # Construir lista ordenada de valores
        input_values = []
        feature_vector_dict = {}
        for feature in model_features:
            val = features_dict.get(feature, 0) # 0 como default seguro para features numéricas faltantes
            # Ensure float conversion for model
            try:
                val = float(val)
            except:
                val = 0.0
            input_values.append(val)
            feature_vector_dict[feature] = val
        
        print(f"DEBUG: Vector: {feature_vector_dict}")
            
        # Criar DataFrame com a ordem correta
        X = pd.DataFrame([input_values], columns=model_features)
        
        # Aplicar normalização se preprocessor está disponível (apenas se foi treinado com scaler)
        # O novo modelo Random Forest NÃO usa Scaler, então essa etapa pode ser pulada ou ajustada
        if preprocessor and hasattr(preprocessor, 'pipeline'):
            pass # Lógica de scaler removida para evitar conflito com modelo RF não escalado

        # Fazer a predição
        prediction = model.predict(X)[0]
        # predict_proba retorna [prob_0, prob_1]
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
            "message": f"Aluno com risco {risk_level.lower()} de evasão",
            "debug_features": feature_vector_dict  # Added debug info
        }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro na predição: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model and preprocessor else "unhealthy",
        "model_loaded": model is not None,
        "config_loaded": config is not None,
        "preprocessor_loaded": preprocessor is not None
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
