#!/usr/bin/env python3
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'Server', 'resources', 'gamedata.db')

print(f"📂 Conectando ao banco: {db_path}\n")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Listar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"📊 Tabelas encontradas: {len(tables)}\n")
    for table in tables:
        table_name = table[0]
        print(f"📋 {table_name}")
        
        # Mostrar estrutura
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   ├─ {col[1]}: {col[2]}")
        
        # Contar registros
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"   └─ Registros: {count}\n")
    
    conn.close()
    print("✅ Inspeção concluída!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
