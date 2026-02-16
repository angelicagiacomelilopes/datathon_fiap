from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import os
import sys
import numpy as np

# Adicionar raiz do projeto ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar o Preprocessor customizado
try:
    from src.preprocessing import DataPreprocessor
except ImportError:
    # Fallback se rodar de dentro de app/
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from src.preprocessing import DataPreprocessor

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model/model.pkl')
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), 'model/preprocessor.pkl')

model = None
preprocessor = None

# Input Model definition
class StudentInput(BaseModel):
    idade: float
    fase: str = Field(..., description="Fase escolar (ex: '7', 'ALFA', 'FASE 1', '1A')")
    ieg: float
    ida: float
    ian: float
    ipp: float
    ips: float
    ipv: float
    pedra: str = Field(..., description="Classificação Pedra (Quartzo, Ágata, etc)")
    ponto_virada: str = Field(..., description="Sim/Não ou True/False")
    ieg_anterior: float = Field(0.0, description="IEG do ano anterior (para cálculo de delta)")
    ida_anterior: float = Field(0.0, description="IDA do ano anterior (para cálculo de delta)")

@router.on_event("startup")
def load_artifacts():
    global model, preprocessor
    
    # Carregar Modelo
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print(f"✅ Modelo carregado: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            
    # Carregar Preprocessor
    if os.path.exists(PREPROCESSOR_PATH):
        try:
            preprocessor = joblib.load(PREPROCESSOR_PATH)
            print(f"✅ Preprocessor carregado: {PREPROCESSOR_PATH}")
        except Exception as e:
            print(f"❌ Erro ao carregar preprocessor: {e}")

    if not model or not preprocessor:
        print("⚠️ Artefatos incompletos. Treine o modelo para gerar model.pkl e preprocessor.pkl")

@router.get("/")
def read_root():
    status = "online" if (model and preprocessor) else "offline (missing artifacts)"
    return {"message": "API Passos Mágicos - Previsão de Evasão", "status": status}

@router.post("/predict")
def predict_risk(student: StudentInput):
    if not model or not preprocessor:
        raise HTTPException(status_code=503, detail="Modelo ou Preprocessor não carregados.")

    try:
        # Prepara os dados conforme o treinamento (feature_store.py)
        # 1. Pedra -> Número
        mapa_pedra = {'QUARTZO': 1, 'ÁGATA': 2, 'AMETISTA': 3, 'TOPÁZIO': 4}
        pedra_ajustada = str(student.pedra).strip().upper()
        # Tratamento para acentos removidos ou mantidos
        if 'AGATA' in pedra_ajustada: pedra_ajustada = 'ÁGATA'
        if 'TOPAZIO' in pedra_ajustada: pedra_ajustada = 'TOPÁZIO'
        
        pedra_num = mapa_pedra.get(pedra_ajustada, 0)
        
        # 2. Ponto de Virada -> Binário
        pv_str = str(student.ponto_virada).strip().lower()
        pv_val = 1 if pv_str in ['sim', 'true', 's', '1'] else 0
        
        # 3. Deltas
        d_ieg = student.ieg - student.ieg_anterior
        d_ida = student.ida - student.ida_anterior
        
        # 4. Defasagem
        defasagem = 0.0
        
        # Tentar converter fase para número para cálculo de defasagem (apenas se possível)
        fase_num = 0
        try:
            # Tratamento simplificado: Se for ALFA, considera 0. Se for texto, tenta extrair numero
            str_fase = str(student.fase).upper()
            if "ALFA" in str_fase:
                fase_num = 0
            elif "FASE" in str_fase:
                fase_num = int(''.join(filter(str.isdigit, str_fase)))
            else:
                # Tenta converter direto, pode ser '7' ou '1A' (pega o 1)
                 fase_num = int(''.join(filter(str.isdigit, str_fase)))
        except:
             fase_num = 0 # Fallback

        if fase_num > 0:
            defasagem = student.idade - (fase_num + 6)

        # Montar input DataFrame na ORDEM EXATA do treino
        # Features usadas: 'idade', 'fase', 'ieg', 'ida', 'ian', 'ipp', 'ips', 'ipv', 'delta_ieg', 'delta_ida', 'pedra_num', 'ponto_virada', 'defasagem'
        input_data = {
            'idade': [student.idade],
            'fase': [fase_num], # Usa o valor numérico convertido
            'ieg': [student.ieg],
            'ida': [student.ida],
            'ian': [student.ian],
            'ipp': [student.ipp],
            'ips': [student.ips],
            'ipv': [student.ipv],
            'delta_ieg': [d_ieg],
            'delta_ida': [d_ida],
            'pedra_num': [pedra_num],
            'ponto_virada': [pv_val],
            'defasagem': [defasagem]
        }
        
        df = pd.DataFrame(input_data)
        
        # Aplicar preprocessamento (Scale, OneHot, etc)
        df_processed = preprocessor.transform(df)
        
        # Predição
        probabilidade = model.predict_proba(df_processed)[0][1]
        classe = int(probabilidade > 0.5)
        
        risk_level = "ALTO" if probabilidade >= 0.7 else "MÉDIO" if probabilidade >= 0.4 else "BAIXO"
        
        return {
            "prediction": classe,
            "probability": round(probabilidade, 4),
            "risk_level": risk_level,
            "input_features": input_data
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
