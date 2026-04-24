#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script rápido para regenerar a planilha Excel
"""

import os
import subprocess
import sys
from datetime import datetime

PROJECT_ROOT = r"c:\Users\Wesley\Desktop\meu jogo 3d 3 os assets\🌍 MYTHARA Gurra de Raças 17-10-2025"
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
EXCEL_SCRIPT = os.path.join(SCRIPTS_DIR, "create_excel_database.py")
EXCEL_FILE = os.path.join(PROJECT_ROOT, "MYTHARA_Items_Database.xlsx")

def main():
    print("\n" + "=" * 70)
    print("🔄 REGENERADOR DE PLANILHA EXCEL - MYTHARA".center(70, "="))
    print("=" * 70)
    
    print(f"\n⏱️  Iniciando regeneração da planilha...")
    print(f"📅 Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Verifica se arquivo existe
        if os.path.exists(EXCEL_FILE):
            print(f"\n💾 Arquivo existente encontrado")
            arquivo_tamanho = os.path.getsize(EXCEL_FILE) / (1024 * 1024)
            print(f"   Tamanho: {arquivo_tamanho:.2f} MB")
        
        # Executa script
        print(f"\n⚙️  Executando script de criação...")
        result = subprocess.run(
            [sys.executable, EXCEL_SCRIPT],
            cwd=SCRIPTS_DIR,
            capture_output=True,
            text=True
        )
        
        # Verifica resultado
        if result.returncode == 0:
            print(f"\n✅ SUCESSO!")
            print(result.stdout)
            
            if os.path.exists(EXCEL_FILE):
                novo_tamanho = os.path.getsize(EXCEL_FILE) / (1024 * 1024)
                print(f"\n✓ Arquivo final: {novo_tamanho:.2f} MB")
                print(f"📁 Localização: {EXCEL_FILE}")
        else:
            print(f"\n❌ ERRO durante a execução!")
            print(result.stderr)
            return 1
        
        print("\n" + "=" * 70)
        print("✅ Regeneração concluída com sucesso!".center(70, "="))
        print("=" * 70)
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
