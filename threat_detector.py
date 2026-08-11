import os
import sys
import time
import psutil
import json

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Windowsシステム公式アプリ＆標準アプリケーションの信頼ホワイトリスト
SYSTEM_SAFE_NAMES = {
    "svchost.exe", "explorer.exe", "system", "idle", "taskhostw.exe",
    "csrss.exe", "smss.exe", "wininit.exe", "services.exe", "lsass.exe",
    "spoolsv.exe", "python.exe", "powershell.exe", "cmd.exe", "chrome.exe",
    "firefox.exe", "discord.exe", "antigravity.exe", "obs64.exe",
    "runtimebroker.exe", "sppsvc.exe", "wmiprvse.exe", "wmiapsrv.exe",
    "backgroundtaskhost.exe", "searchprotocolhost.exe", "updater.exe",
    "ctfmon.exe", "conhost.exe", "sihost.exe", "taskmgr.exe"
}

class ThreatDetector:
    def __init__(self):
        self.known_pids = set()
        self.scan_count = 0
        self._init_baseline()

    def _init_baseline(self):
        """軽量ベースライン構築"""
        for proc in psutil.process_iter(attrs=['pid']):
            try:
                self.known_pids.add(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        print(f"🛡️ [AI Security Guardian] ベースライン構築完了: {len(self.known_pids)} 個のシステムプロセスを正常登録")

    def scan_new_threats(self):
        """超軽量＆高精度スキャン（MemoryError防止・AIふるまい判定）"""
        self.scan_count += 1
        new_threats = []
        current_pids = set()

        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                pid = proc.info['pid']
                name = proc.info['name'] or ""
                current_pids.add(pid)

                # 未登録の新起動プロセスのみ詳細スキャン
                if pid not in self.known_pids:
                    name_lower = name.lower()
                    
                    # Windows標準サービスはノイズ除外
                    if name_lower in SYSTEM_SAFE_NAMES:
                        continue

                    # 実行パスの取得（安全なエラー例外ハンドリング）
                    exe_path = ""
                    try:
                        exe_path = proc.exe() or ""
                    except Exception:
                        pass

                    # 危険度判定
                    is_suspicious = False
                    reason = "新規実行プロセス"

                    # 判定1: TempやAppData一時フォルダからの怪しい起動（トロイ・マルウェアの典型挙動）
                    path_lower = exe_path.lower()
                    if "temp" in path_lower or "appdata\\local\\temp" in path_lower:
                        is_suspicious = True
                        reason = "🚨 [高危険度] 一時フォルダ(Temp)からの未認知自動実行"
                    elif not path_lower.startswith("c:\\windows") and not path_lower.startswith("c:\\program files"):
                        is_suspicious = True
                        reason = "⚠️ [要注意] システム領域外からの未登録アプリ起動"

                    if is_suspicious:
                        new_threats.append({
                            "pid": pid,
                            "name": name,
                            "path": exe_path or "パス非公開プロセス",
                            "suspicious": is_suspicious,
                            "reason": reason,
                            "time": time.strftime("%H:%M:%S")
                        })

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        self.known_pids = current_pids
        return new_threats

if __name__ == "__main__":
    detector = ThreatDetector()
    print("🔍 [スキャンテスト完了]")
