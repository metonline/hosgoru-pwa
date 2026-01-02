#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub'dan tasarım dosyalarını pull eden script
database.json korunacak (zaten .gitignore'da)
"""

import subprocess
import os
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, 'database.json')
LOG_FILE = os.path.join(SCRIPT_DIR, 'git_sync.log')

def log_message(msg):
    """Log dosyasına yaz"""
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def backup_database():
    """database.json'ı yedekle"""
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8-sig') as f:
                db_content = f.read()
            return db_content
        return None
    except Exception as e:
        log_message(f"⚠️ Database yedeklenemiyor: {e}")
        return None

def restore_database(db_content):
    """database.json'ı geri yükle"""
    try:
        if db_content:
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                f.write(db_content)
            log_message("✅ Database geri yüklendi")
            return True
    except Exception as e:
        log_message(f"❌ Database restore hatası: {e}")
    return False

def sync_design_files():
    """GitHub'dan tasarım dosyalarını pull et"""
    try:
        os.chdir(SCRIPT_DIR)
        log_message("🔄 Git pull başlanıyor...")
        
        # Git pull çalıştır
        result = subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            capture_output=True,
            timeout=60,
            text=True
        )
        
        if result.returncode == 0:
            log_message("✅ Git pull başarılı")
            if "Already up to date" in result.stdout:
                log_message("ℹ️ Tasarım dosyaları zaten güncel")
            else:
                log_message(f"📦 Dosyalar güncellendi: {result.stdout[:100]}")
            return True
        else:
            log_message(f"❌ Git pull hatası: {result.stderr[:200]}")
            return False
            
    except subprocess.TimeoutExpired:
        log_message("⚠️ Git pull timeout (60s)")
        return False
    except Exception as e:
        log_message(f"❌ Hata: {str(e)[:100]}")
        return False

def main():
    log_message("="*60)
    log_message("🚀 GitHub Tasarım Senkronizasyon Başladı")
    
    # Database'i yedekle
    db_backup = backup_database()
    
    # Git pull yap
    success = sync_design_files()
    
    # Database'i geri yükle (korunacak)
    if db_backup:
        restore_database(db_backup)
    
    log_message("="*60)
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
