import sys
import os
import pandas as pd
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from drift_monitor import DriftDetector, ModelPerformanceMonitor, DriftAlert
import joblib


class DriftMonitoringDashboard:
    def __init__(self, baseline_path: str, model_config_path: str):
        self.baseline_data = pd.read_csv(baseline_path)
        self.config = joblib.load(model_config_path)
        self.features = self.config.get('features', [
            'idade', 'ieg', 'ida', 'ian', 'ipp', 'ips', 'ipv', 'defasagem'
        ])
        
        self.drift_detector = DriftDetector(self.baseline_data, self.features, threshold=0.05)
        self.performance_monitor = ModelPerformanceMonitor()
        self.drift_alert = DriftAlert()
        
        self.report_dir = Path('logs/drift_reports')
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def check_data_drift(self, sample_size: int = 100) -> Dict:
        sample = self.baseline_data.sample(
            n=min(sample_size, len(self.baseline_data)), 
            random_state=None
        )
        
        analysis = self.drift_detector.analyze_drift(sample)
        
        if analysis['overall_drift_detected']:
            self.drift_alert.create_alert(
                alert_type="DATA_DRIFT",
                severity="WARNING",
                message="Possible data drift detected",
                details={
                    'timestamp': datetime.now().isoformat(),
                    'sample_size': len(sample)
                }
            )
        
        return analysis
    
    def generate_report(self) -> str:
        report = {
            'timestamp': datetime.now().isoformat(),
            'drift_summary': self.drift_detector.get_drift_summary(),
            'performance_summary': self.performance_monitor.get_model_metrics(),
            'alerts_summary': self.drift_alert.get_alert_summary()
        }
        
        report_file = self.report_dir / f"monitoring_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return str(report_file)
    
    def run_continuous_monitoring(self, interval_minutes: int = 60, duration_hours: int = None):
        print(f"[{datetime.now()}] Iniciando monitoramento contínuo (intervalo: {interval_minutes}min)")
        
        start_time = time.time()
        check_count = 0
        
        while True:
            try:
                print(f"\n[{datetime.now()}] Executando check #{check_count + 1}")
                
                analysis = self.check_data_drift()
                
                if analysis['overall_drift_detected']:
                    print("⚠️  DRIFT DETECTADO!")
                else:
                    print("✓ Dados estáveis")
                
                drift_summary = self.drift_detector.get_drift_summary()
                print(f"  Taxa de drift: {drift_summary['drift_rate']}")
                print(f"  Status: {drift_summary['current_status']}")
                
                perf_summary = self.performance_monitor.get_model_metrics()
                if perf_summary.get('accuracy'):
                    print(f"  Acurácia: {perf_summary['accuracy']:.2%}")
                    print(f"  Status performance: {perf_summary['performance_status']}")
                
                report_file = self.generate_report()
                print(f"  Relatório salvo: {report_file}")
                
                check_count += 1
                
                if duration_hours:
                    elapsed_hours = (time.time() - start_time) / 3600
                    if elapsed_hours >= duration_hours:
                        print(f"\n[{datetime.now()}] Duração limite atingida. Encerrando.")
                        break
                
                print(f"Próximo check em {interval_minutes} minutos...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                print(f"\n[{datetime.now()}] Monitoramento interrompido pelo usuário")
                break
            except Exception as e:
                print(f"Erro durante monitoramento: {e}")
                time.sleep(60)
    
    def print_dashboard(self):
        print("\n" + "="*80)
        print("DASHBOARD - MONITORAMENTO DE DRIFT")
        print("="*80)
        
        print("\n📊 DRIFT STATUS:")
        drift_summary = self.drift_detector.get_drift_summary()
        for key, value in drift_summary.items():
            print(f"  {key}: {value}")
        
        print("\n📈 PERFORMANCE:")
        perf_summary = self.performance_monitor.get_model_metrics()
        for key, value in perf_summary.items():
            if key not in ['prediction_distribution', 'last_update']:
                print(f"  {key}: {value}")
        
        print("\n🚨 ALERTS:")
        alert_summary = self.drift_alert.get_alert_summary()
        for key, value in alert_summary.items():
            if key != 'recent_alerts':
                print(f"  {key}: {value}")
        
        print("\n" + "="*80)


def main():
    baseline_path = 'arquivo_tratado/df_model_ready.csv'
    config_path = '../app/model/model_config.pkl'
    
    if not os.path.exists(baseline_path):
        print(f"Erro: Arquivo baseline não encontrado: {baseline_path}")
        return
    
    if not os.path.exists(config_path):
        print(f"Erro: Config não encontrada: {config_path}")
        return
    
    try:
        dashboard = DriftMonitoringDashboard(baseline_path, config_path)
        
        print("Opções:")
        print("1. Executar single check")
        print("2. Executar monitoramento contínuo (1 hora)")
        print("3. Visualizar dashboard")
        
        choice = input("Escolha (1-3): ").strip()
        
        if choice == "1":
            print("Executando single check...")
            analysis = dashboard.check_data_drift()
            print(json.dumps(analysis, indent=2))
            dashboard.print_dashboard()
        
        elif choice == "2":
            interval = int(input("Intervalo em minutos (padrão 60): ") or "60")
            duration = int(input("Duração em horas (0 para infinito): ") or "0")
            dashboard.run_continuous_monitoring(
                interval_minutes=interval,
                duration_hours=duration if duration > 0 else None
            )
        
        elif choice == "3":
            dashboard.print_dashboard()
        
        else:
            print("Opção inválida")
    
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
