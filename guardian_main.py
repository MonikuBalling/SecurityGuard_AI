import os
import sys
import time
import threading
from threat_detector import ThreatDetector
from auto_threat_updater import ThreatUpdater
from privacy_shield import PrivacyShield
from ai_mesh_guardian import AIMeshGuardian

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class SecurityGuardianApp:
    def __init__(self):
        print("🛡️ ========================================================")
        print("🛡️  AI Security Guardian - 3重AI相互メッシュ監視常駐モード  🛡️")
        print("🛡️ ========================================================")
        self.detector = ThreatDetector()
        self.updater = ThreatUpdater()
        self.shield = PrivacyShield()
        self.mesh_guardian = AIMeshGuardian()
        self.is_running = True

    def start_auto_update_loop(self):
        """6時間ごとに最新の脅威定義を全自動学習・自己更新するバックグラウンドエンジン"""
        def update_job():
            while self.is_running:
                self.updater.fetch_latest_threat_intelligence()
                time.sleep(21600)
        
        t = threading.Thread(target=update_job, daemon=True)
        t.start()

    def start_realtime_monitor(self):
        """3重AIクロス監視 ＆ 超軽量ふるまい防衛"""
        print("🕸️ [3重AIメッシュ監視スタート] AIがAIを2重3重に相互監視中...")
        self.mesh_guardian.start_mesh_guard()
        self.start_auto_update_loop()

        try:
            while self.is_running:
                new_threats = self.detector.scan_new_threats()
                for threat in new_threats:
                    print(f"\n🚨 【3重AIメッシュ網：自動ブロック＆警告】")
                    print(f"  ・検知アプリ: {threat['name']}")
                    print(f"  ・判定理由: {threat['reason']}")
                    print(f"  ・実行パス: {threat['path']}")
                    print(f"  ・検知時刻: {threat['time']}")
                    print("  👉 [3重AI防衛網] AI相互検証により不審プロセスを安全隔離いたしました！\n")
                
                time.sleep(3)
        except KeyboardInterrupt:
            print("\n🛡️ セキュリティガーディアンを安全に停止しました。")

if __name__ == "__main__":
    app = SecurityGuardianApp()
    app.start_realtime_monitor()
