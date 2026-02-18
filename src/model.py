from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os


def train_dropout_model(df):
    features = [
        'idade', 'fase', 'ieg', 'ida', 'ian',
        'ipp', 'ips', 'ipv',
        'delta_ieg', 'delta_ida',
        'pedra_num', 'ponto_virada',
        'defasagem'
    ]
    features_existentes = [col for col in features if col in df.columns]
    
    X = df[features_existentes]
    y = df['atingiu_pv']
    y = (y > 0).astype(int)
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring='f1')
    
    model.fit(X, y)
    print(f"Modelo treinado: {len(X)} registros")

    y_pred = model.predict(X)
    print("\n--- Performance ---")
    print(classification_report(y, y_pred))
    print(confusion_matrix(y, y_pred))

    return model, scores.mean(), X


def save_model(model, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"Modelo salvo: {filepath}")