import os
import sys
import re

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class PrivacyShield:
    def __init__(self):
        # メールアドレス・パスワード・個人情報パターンの検出正規表現
        self.email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        self.ip_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    def sanitize_text(self, text):
        """テキスト内のメールアドレスやIPアドレスなどの個人情報を自動マスク"""
        sanitized = self.email_regex.sub("[*** 個人情報保護: メールアドレス ***]", text)
        sanitized = self.ip_regex.sub("[*** 個人情報保護: IPアドレス ***]", sanitized)
        return sanitized

if __name__ == "__main__":
    shield = PrivacyShield()
    sample = "私のメールアドレスは testuser123@gmail.com で、IPは 192.168.1.1 です。"
    print("原版:", sample)
    print("保護後:", shield.sanitize_text(sample))
