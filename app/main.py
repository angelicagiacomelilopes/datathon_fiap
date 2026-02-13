from fastapi import FastAPI
import sys
import os

# Adicionar raiz do projeto ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes import router

app = FastAPI(title="Passos Mágicos Prediction API", version="1.0", description="API para previsão de risco de defasagem escolar.")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
