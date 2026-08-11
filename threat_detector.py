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

# 信頼できるホワイトリスト（標準Windowsプロセスおよび安全アプリ）
KNOWN_SAFE_PROCESSES = {
    "svchost.exe", "explorer.exe", "system", "idle", "taskhostw.exe",
    "csrss.exe", "smss.exe", "wininit.exe", "services.exe", "lsass.exe",
    "spoolsv.exe", "python.exe", "powershell.exe", "cmd.exe", "chrome.exe",
    "firefox.exe", "discord.exe", "antigravity.exe", "obs64.exe"
}

class ThreatDetector:
    def __init__(self):
        self.known_pids = set()
        self.scan_count = 0
        self._init_baseline()

    def _init_baseline(self):
        """現在のベースライン（起動中プロセス）を記録"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                self.known_pids.add(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        print(f"🛡️ [Security Guardian] ベースライン構築完了: {len(self.known_pids)} 個のプロセスを登録")

    def scan_new_threats(self):
        """新しく起動した未知のプロセスや不審な挙動を検知"""
        self.scan_count += 1
        new_threats = []
        current_pids = set()

        for proc in psutil.process_iter(['pid', 'name', 'exe', 'cpu_percent', 'memory_percent']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                exe_path = proc.info['exe'] or "Unknown"
                current_pids.add(pid)

                # 未知の新プロセスが起動した場合
                if pid not in self.known_pids:
                    name_lower = name.lower() if name else ""
                    is_suspicious = False
                    reason = "新規プロセス検出"

                    # 判定ロジック1: ホワイトリスト外の未知アプリ
                    if name_lower not in KNOWN_SAFE_PROCESSES:
                        is_suspicious = True
                        reason = "未登録の未知アプリケーション"

                    # 判定ロジック2: システムディレクトリ以外からの怪しい起動
                    if "temp" in exe_path.lower() or "appdata\\local\\temp" in exe_path.lower():
                        is_suspicious = True
                        reason = "一時フォルダ(Temp)からの不審な自動起動"

                    new_threats.append({
                        "pid": pid,
                        "name": name,
                        "path": exe_path,
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
    print("🔍 [リアルタイムスキャンテスト開始]")
    threats = detector.scan_new_threats()
    print(f"✅ スキャン結果: 新規検出 {len(threats)} 件")
