import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
from pathlib import Path


class DriftDetector:
    def __init__(self, baseline_df: pd.DataFrame, features: List[str], threshold: float = 0.05):
        self.baseline_df = baseline_df
        self.features = features
        self.threshold = threshold
        self.baseline_stats = self._compute_baseline_stats()
        self.drift_history = []
        
    def _compute_baseline_stats(self) -> Dict:
        stats_dict = {}
        for feature in self.features:
            if feature in self.baseline_df.columns:
                col_data = self.baseline_df[feature].dropna()
                stats_dict[feature] = {
                    'mean': float(col_data.mean()),
                    'std': float(col_data.std()),
                    'min': float(col_data.min()),
                    'max': float(col_data.max()),
                    'median': float(col_data.median()),
                    'q25': float(col_data.quantile(0.25)),
                    'q75': float(col_data.quantile(0.75))
                }
        return stats_dict
    
    def detect_kolmogorov_smirnov(self, current_data: pd.DataFrame) -> Dict[str, float]:
        results = {}
        for feature in self.features:
            if feature in self.baseline_df.columns and feature in current_data.columns:
                baseline = self.baseline_df[feature].dropna()
                current = current_data[feature].dropna()
                
                if len(current) > 0 and len(baseline) > 0:
                    statistic, pvalue = stats.ks_2samp(baseline, current)
                    results[feature] = {
                        'statistic': float(statistic),
                        'pvalue': float(pvalue),
                        'drift_detected': pvalue < self.threshold
                    }
        return results
    
    def detect_wasserstein(self, current_data: pd.DataFrame) -> Dict[str, float]:
        results = {}
        for feature in self.features:
            if feature in self.baseline_df.columns and feature in current_data.columns:
                baseline = self.baseline_df[feature].dropna().values
                current = current_data[feature].dropna().values
                
                if len(current) > 0 and len(baseline) > 0:
                    distance = stats.wasserstein_distance(baseline, current)
                    baseline_range = np.std(baseline) if len(baseline) > 1 else 1
                    normalized_distance = distance / max(baseline_range, 1e-6)
                    
                    results[feature] = {
                        'distance': float(distance),
                        'normalized': float(normalized_distance),
                        'drift_detected': normalized_distance > self.threshold * 10
                    }
        return results
    
    def detect_chi_square(self, current_data: pd.DataFrame, bins: int = 10) -> Dict[str, float]:
        results = {}
        for feature in self.features:
            if feature in self.baseline_df.columns and feature in current_data.columns:
                baseline = self.baseline_df[feature].dropna().values
                current = current_data[feature].dropna().values
                
                if len(current) > 0 and len(baseline) > 0:
                    try:
                        baseline_hist, bin_edges = np.histogram(baseline, bins=bins)
                        current_hist, _ = np.histogram(current, bins=bin_edges)
                        
                        baseline_hist = baseline_hist + 1
                        current_hist = current_hist + 1
                        
                        chi2_stat = np.sum((baseline_hist - current_hist) ** 2 / (current_hist + baseline_hist))
                        pvalue = 1 - stats.chi2.cdf(chi2_stat, df=bins - 1)
                        
                        results[feature] = {
                            'chi2_statistic': float(chi2_stat),
                            'pvalue': float(pvalue),
                            'drift_detected': pvalue < self.threshold
                        }
                    except Exception as e:
                        results[feature] = {'error': str(e)}
        return results
    
    def compute_psi(self, current_data: pd.DataFrame, bins: int = 10) -> Dict[str, float]:
        results = {}
        for feature in self.features:
            if feature in self.baseline_df.columns and feature in current_data.columns:
                baseline = self.baseline_df[feature].dropna().values
                current = current_data[feature].dropna().values
                
                if len(current) > 0 and len(baseline) > 0:
                    try:
                        baseline_hist, bin_edges = np.histogram(baseline, bins=bins)
                        current_hist, _ = np.histogram(current, bins=bin_edges)
                        
                        baseline_pct = (baseline_hist + 1) / (baseline_hist.sum() + bins)
                        current_pct = (current_hist + 1) / (current_hist.sum() + bins)
                        
                        psi = np.sum((current_pct - baseline_pct) * np.log(current_pct / baseline_pct))
                        
                        results[feature] = {
                            'psi': float(psi),
                            'drift_detected': psi > 0.1
                        }
                    except Exception as e:
                        results[feature] = {'error': str(e)}
        return results
    
    def analyze_drift(self, current_data: pd.DataFrame) -> Dict:
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'sample_size': len(current_data),
            'ks_test': self.detect_kolmogorov_smirnov(current_data),
            'wasserstein': self.detect_wasserstein(current_data),
            'chi_square': self.detect_chi_square(current_data),
            'psi': self.compute_psi(current_data)
        }
        
        overall_drift = self._assess_overall_drift(analysis)
        analysis['overall_drift_detected'] = overall_drift
        
        self.drift_history.append(analysis)
        return analysis
    
    def _assess_overall_drift(self, analysis: Dict) -> bool:
        drift_signals = 0
        total_tests = 0
        
        for test_name in ['ks_test', 'chi_square']:
            for feature, result in analysis[test_name].items():
                if 'drift_detected' in result:
                    total_tests += 1
                    if result['drift_detected']:
                        drift_signals += 1
        
        return drift_signals / max(total_tests, 1) > 0.3
    
    def get_drift_summary(self) -> Dict:
        if not self.drift_history:
            return {'status': 'No drift checks performed yet'}
        
        latest = self.drift_history[-1]
        history_length = len(self.drift_history)
        
        drift_count = sum(1 for h in self.drift_history if h.get('overall_drift_detected', False))
        
        return {
            'total_checks': history_length,
            'drift_detected_count': drift_count,
            'drift_rate': f"{(drift_count / history_length * 100):.1f}%",
            'latest_check': latest['timestamp'],
            'current_status': 'DRIFT_DETECTED' if latest.get('overall_drift_detected') else 'STABLE',
            'last_5_checks': [h.get('overall_drift_detected', False) for h in self.drift_history[-5:]]
        }


class ModelPerformanceMonitor:
    def __init__(self, reference_threshold: float = 0.85):
        self.reference_threshold = reference_threshold
        self.predictions_history = []
        
    def log_prediction(self, prediction: int, probability: float, 
                      actual: Optional[int] = None, metadata: Dict = None):
        record = {
            'timestamp': datetime.now().isoformat(),
            'prediction': prediction,
            'probability': probability,
            'actual': actual,
            'metadata': metadata or {}
        }
        if actual is not None:
            record['correct'] = (prediction == actual)
        
        self.predictions_history.append(record)
    
    def get_model_metrics(self) -> Dict:
        if not self.predictions_history:
            return {'status': 'No predictions yet'}
        
        predictions = self.predictions_history
        total = len(predictions)
        
        avg_probability = np.mean([p['probability'] for p in predictions])
        
        with_actuals = [p for p in predictions if p.get('actual') is not None]
        if with_actuals:
            accuracy = np.mean([p['correct'] for p in with_actuals])
            recent_accuracy = np.mean([p['correct'] for p in with_actuals[-100:]])
        else:
            accuracy = None
            recent_accuracy = None
        
        prediction_dist = pd.Series([p['prediction'] for p in predictions]).value_counts().to_dict()
        
        return {
            'total_predictions': total,
            'avg_confidence': float(avg_probability),
            'accuracy': float(accuracy) if accuracy else None,
            'recent_accuracy_100': float(recent_accuracy) if recent_accuracy else None,
            'prediction_distribution': prediction_dist,
            'performance_status': self._assess_performance(accuracy, recent_accuracy),
            'last_update': predictions[-1]['timestamp']
        }
    
    def _assess_performance(self, accuracy: Optional[float], recent_accuracy: Optional[float]) -> str:
        if accuracy is None:
            return 'INSUFFICIENT_DATA'
        
        if recent_accuracy is not None and recent_accuracy < accuracy - 0.1:
            return 'DEGRADING'
        
        if accuracy < self.reference_threshold:
            return 'BELOW_THRESHOLD'
        
        return 'HEALTHY'


class DriftAlert:
    def __init__(self, alert_log_path: str = 'logs/drift_alerts.json'):
        self.alert_log_path = Path(alert_log_path)
        self.alert_log_path.parent.mkdir(parents=True, exist_ok=True)
        self.alerts = []
    
    def create_alert(self, alert_type: str, severity: str, message: str, 
                    details: Dict = None) -> Dict:
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity,
            'message': message,
            'details': details or {}
        }
        self.alerts.append(alert)
        self._save_alert(alert)
        return alert
    
    def _save_alert(self, alert: Dict):
        with open(self.alert_log_path, 'a') as f:
            f.write(json.dumps(alert) + '\n')
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        return self.alerts[-limit:]
    
    def get_alert_summary(self) -> Dict:
        by_type = {}
        by_severity = {}
        
        for alert in self.alerts:
            alert_type = alert['type']
            severity = alert['severity']
            
            by_type[alert_type] = by_type.get(alert_type, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
        
        return {
            'total_alerts': len(self.alerts),
            'by_type': by_type,
            'by_severity': by_severity,
            'recent_alerts': self.get_recent_alerts(5)
        }
