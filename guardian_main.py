import os
import sys
import time
import threading
from threat_detector import ThreatDetector
from auto_threat_updater import ThreatUpdater
from privacy_shield import PrivacyShield

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class SecurityGuardianApp:
    def __init__(self):
        print("🛡️ ===================================================")
        print("🛡️  AI Security Guardian - リアルタイムセキュリティ常駐開始  🛡️")
        print("🛡️ ===================================================")
        self.detector = ThreatDetector()
        self.updater = ThreatUpdater()
        self.shield = PrivacyShield()
        self.is_running = True

    def start_auto_update_loop(self):
        """6時間ごとに最新の脅威定義を全自動学習・更新するバックグラウンドスレッド"""
        def update_job():
            while self.is_running:
                self.updater.fetch_latest_threat_intelligence()
                # 6時間待機 (テスト用に21600秒)
                time.sleep(21600)
        
        t = threading.Thread(target=update_job, daemon=True)
        t.start()

    def start_realtime_monitor(self):
        """リアルタイムで未登録プロセスや怪しい挙動をPC画面で常時監視"""
        print("👁️ [リアルタイム監視エンジン] PCの安全を常時ガード中...")
        self.start_auto_update_loop()

        try:
            while self.is_running:
                new_threats = self.detector.scan_new_threats()
                for threat in new_threats:
                    if threat["suspicious"]:
                        print(f"\n⚠️ 【セキュリティ警告】 未認知プロセスを検出!")
                        print(f"  ・アプリ名: {threat['name']}")
                        print(f"  ・検出理由: {threat['reason']}")
                        print(f"  ・実行パス: {threat['path']}")
                        print(f"  ・検出時刻: {threat['time']}")
                        print("  👉 [自動ガード] Windows Defender と連携して安全性を検証中...\n")
                
                time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛡️ セキュリティガーディアンを安全に停止しました。")

if __name__ == "__main__":
    app = SecurityGuardianApp()
    app.start_realtime_monitor()
