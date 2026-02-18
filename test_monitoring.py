import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
import joblib
import numpy as np
from src.drift_monitor import DriftDetector, ModelPerformanceMonitor, DriftAlert


def test_drift_detector():
    print("\n" + "="*80)
    print("TEST 1: DriftDetector - Kolmogorov-Smirnov Test")
    print("="*80)
    
    baseline = pd.read_csv('src/arquivo_tratado/df_model_ready.csv')
    config = joblib.load('app/model/model_config.pkl')
    features = config['features']
    
    detector = DriftDetector(baseline, features, threshold=0.05)
    
    sample = baseline.sample(n=100, random_state=42)
    analysis = detector.analyze_drift(sample)
    
    print(f"✓ Análise executada com sucesso")
    print(f"  - Overall drift: {analysis['overall_drift_detected']}")
    print(f"  - Testes por feature: {len(analysis['ks_test'])} features testadas")
    print(f"  - Timestamp: {analysis['timestamp']}")
    
    return detector


def test_wasserstein():
    print("\n" + "="*80)
    print("TEST 2: DriftDetector - Wasserstein Distance")
    print("="*80)
    
    baseline = pd.read_csv('src/arquivo_tratado/df_model_ready.csv')
    config = joblib.load('app/model/model_config.pkl')
    features = config['features']
    
    detector = DriftDetector(baseline, features)
    sample = baseline.sample(n=100, random_state=42)
    
    results = detector.detect_wasserstein(sample)
    
    print("✓ Wasserstein distance calculado")
    for feature, result in list(results.items())[:3]:
        print(f"  - {feature}: distance={result.get('distance', 'N/A'):.4f}")


def test_psi():
    print("\n" + "="*80)
    print("TEST 3: DriftDetector - Population Stability Index (PSI)")
    print("="*80)
    
    baseline = pd.read_csv('src/arquivo_tratado/df_model_ready.csv')
    config = joblib.load('app/model/model_config.pkl')
    features = config['features']
    
    detector = DriftDetector(baseline, features)
    sample = baseline.sample(n=100, random_state=42)
    
    results = detector.compute_psi(sample)
    
    print("✓ PSI calculado")
    for feature, result in list(results.items())[:3]:
        if 'psi' in result:
            print(f"  - {feature}: PSI={result['psi']:.4f}, drift={result.get('drift_detected', False)}")


def test_performance_monitor():
    print("\n" + "="*80)
    print("TEST 4: ModelPerformanceMonitor")
    print("="*80)
    
    monitor = ModelPerformanceMonitor(reference_threshold=0.85)
    
    np.random.seed(42)
    for _ in range(100):
        prediction = np.random.randint(0, 2)
        probability = np.random.uniform(0.1, 0.9)
        actual = prediction if np.random.random() > 0.15 else 1 - prediction
        
        monitor.log_prediction(prediction, probability, actual)
    
    metrics = monitor.get_model_metrics()
    
    print("✓ Performance monitorado")
    print(f"  - Total predictions: {metrics['total_predictions']}")
    print(f"  - Avg confidence: {metrics['avg_confidence']:.2%}")
    if metrics['accuracy']:
        print(f"  - Accuracy: {metrics['accuracy']:.2%}")
    print(f"  - Performance status: {metrics['performance_status']}")


def test_drift_alert():
    print("\n" + "="*80)
    print("TEST 5: DriftAlert System")
    print("="*80)
    
    alert_system = DriftAlert()
    
    alert1 = alert_system.create_alert(
        alert_type="DATA_DRIFT",
        severity="WARNING",
        message="Drift detected in feature 'idade'",
        details={"feature": "idade", "pvalue": 0.02}
    )
    
    alert2 = alert_system.create_alert(
        alert_type="PERFORMANCE_DEGRADATION",
        severity="CRITICAL",
        message="Model accuracy dropped below threshold",
        details={"current_accuracy": 0.82, "threshold": 0.85}
    )
    
    print("✓ Alertas criados")
    print(f"  - Alert 1 type: {alert1['type']} ({alert1['severity']})")
    print(f"  - Alert 2 type: {alert2['type']} ({alert2['severity']})")
    
    summary = alert_system.get_alert_summary()
    print(f"\n✓ Alert Summary:")
    print(f"  - Total alerts: {summary['total_alerts']}")
    print(f"  - By type: {summary['by_type']}")
    print(f"  - By severity: {summary['by_severity']}")


def test_drift_history():
    print("\n" + "="*80)
    print("TEST 6: Drift History and Summary")
    print("="*80)
    
    baseline = pd.read_csv('src/arquivo_tratado/df_model_ready.csv')
    config = joblib.load('app/model/model_config.pkl')
    features = config['features']
    
    detector = DriftDetector(baseline, features)
    
    for i in range(3):
        sample = baseline.sample(n=100, random_state=42+i)
        detector.analyze_drift(sample)
        print(f"  - Check {i+1} completed")
    
    summary = detector.get_drift_summary()
    
    print("\n✓ Drift Summary:")
    for key, value in summary.items():
        print(f"  - {key}: {value}")


def test_baseline_stats():
    print("\n" + "="*80)
    print("TEST 7: Baseline Statistics")
    print("="*80)
    
    baseline = pd.read_csv('src/arquivo_tratado/df_model_ready.csv')
    config = joblib.load('app/model/model_config.pkl')
    features = config['features']
    
    detector = DriftDetector(baseline, features)
    
    print("✓ Baseline statistics computed")
    for feature in list(features)[:3]:
        stats = detector.baseline_stats.get(feature, {})
        print(f"  - {feature}:")
        print(f"    mean={stats.get('mean', 'N/A'):.2f}, std={stats.get('std', 'N/A'):.2f}")


def run_all_tests():
    print("\n" + "█"*80)
    print("█ MONITORAMENTO DE DRIFT - TEST SUITE")
    print("█"*80)
    
    try:
        test_drift_detector()
        test_wasserstein()
        test_psi()
        test_performance_monitor()
        test_drift_alert()
        test_drift_history()
        test_baseline_stats()
        
        print("\n" + "█"*80)
        print("█ ✅ TODOS OS TESTES PASSARAM COM SUCESSO")
        print("█"*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
