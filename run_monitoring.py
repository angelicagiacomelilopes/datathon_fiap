#!/usr/bin/env python
"""
Script para executar monitoramento contínuo de drift
Opção 2 do Quick Start
"""
import sys
import os

# Mudar para o diretório src
os.chdir('src')
sys.path.insert(0, os.getcwd())

from drift_dashboard import DriftMonitoringDashboard

def main():
    baseline_path = 'arquivo_tratado/df_model_ready.csv'
    config_path = '../app/model/model_config.pkl'
    
    if not os.path.exists(baseline_path):
        print(f"❌ Erro: Arquivo baseline não encontrado: {baseline_path}")
        print(f"   Verificar em: {os.path.abspath(baseline_path)}")
        return
    
    if not os.path.exists(config_path):
        print(f"⚠️  Warning: Config não encontrada: {config_path}")
        print(f"   Continuando com config padrão...")
    
    try:
        dashboard = DriftMonitoringDashboard(baseline_path, config_path)
        
        print("\n" + "="*60)
        print("🔄 MONITORAMENTO CONTÍNUO DE DRIFT")
        print("="*60)
        
        interval = 60  # 60 minutos
        duration = 2   # 2 horas
        
        print(f"\n📊 Configuração:")
        print(f"  • Intervalo entre checks: {interval} minutos")
        print(f"  • Duração total: {duration} horas")
        print(f"  • Relatórios salvos em: logs/drift_reports/")
        print(f"\n✅ Iniciando monitoramento...\n")
        print("   Pressione CTRL+C para interromper\n")
        
        dashboard.run_continuous_monitoring(
            interval_minutes=interval,
            duration_hours=duration
        )
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
