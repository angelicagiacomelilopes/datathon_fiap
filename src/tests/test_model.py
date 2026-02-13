import pytest
import pandas as pd
import sys
import os
from sklearn.ensemble import RandomForestClassifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils import save_model, load_model

def test_save_load_model(tmp_path):
    # Cria modelo dummy
    model = RandomForestClassifier(n_estimators=5)
    X = [[0, 0], [1, 1]]
    y = [0, 1]
    model.fit(X, y)
    
    # Caminho temporário
    file_path = str(tmp_path / "test_model.pkl")
    
    # Teste Save
    save_model(model, file_path)
    assert os.path.exists(file_path)
    
    # Teste Load
    loaded_model = load_model(file_path)
    assert isinstance(loaded_model, RandomForestClassifier)
    
    # Verifica validade
    assert loaded_model.predict([[0, 0]])[0] == 0
