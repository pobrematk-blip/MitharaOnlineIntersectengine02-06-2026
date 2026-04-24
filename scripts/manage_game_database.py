#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para adicionar/modificar itens e exportar dados do banco de dados
"""

import sqlite3
import os
import json
from datetime import datetime
import shutil

PROJECT_ROOT = r"c:\Users\Wesley\Desktop\meu jogo 3d 3 os assets\🌍 MYTHARA Gurra de Raças 17-10-2025"
DB_PATH = os.path.join(PROJECT_ROOT, "Server", "gamedata.db")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "Server", "database_backups")

def ensure_backup_dir():
    """Cria diretório de backups se não existir"""
    os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_database():
    """Cria backup do banco de dados"""
    ensure_backup_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"gamedata_backup_{timestamp}.db")
    
    try:
        shutil.copy2(DB_PATH, backup_path)
        print(f"✓ Backup criado: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return None

def export_items_to_json(conn, output_file=None):
    """Exporta todos os itens para JSON"""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(PROJECT_ROOT, f"items_export_{timestamp}.json")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items")
    
    columns = [description[0] for description in cursor.description]
    items = []
    
    for row in cursor.fetchall():
        item_dict = dict(zip(columns, row))
        items.append(item_dict)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    
    print(f"✓ {len(items)} itens exportados para: {output_file}")
    return output_file

def add_custom_item(conn, name, category, rarity="Common", value=0, description=""):
    """Adiciona um item customizado"""
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO Items (Name, Description, Category, Value, Rarity)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, description, category, value, rarity))
        
        conn.commit()
        print(f"✓ Item '{name}' adicionado com sucesso!")
        
    except sqlite3.IntegrityError:
        print(f"⚠ Item com nome '{name}' já existe!")
    except Exception as e:
        print(f"❌ Erro ao adicionar item: {e}")

def search_item(conn, search_term):
    """Procura por itens"""
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT Id, Name, Category, Rarity, Value 
    FROM Items 
    WHERE Name LIKE ? 
    ORDER BY Name
    """, (f"%{search_term}%",))
    
    results = cursor.fetchall()
    
    if results:
        print(f"\n🔍 Resultados para '{search_term}' ({len(results)} encontrados):\n")
        print(f"{'ID':<6} {'Nome':<40} {'Categoria':<20} {'Raridade':<12} {'Valor':<8}")
        print("-" * 90)
        
        for item_id, name, category, rarity, value in results:
            print(f"{item_id:<6} {name:<40} {category:<20} {rarity:<12} {value:<8,}")
    else:
        print(f"❌ Nenhum item encontrado para '{search_term}'")
    
    return results

def update_item_value(conn, item_id, new_value):
    """Atualiza o valor de um item"""
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE Items SET Value = ? WHERE Id = ?", (new_value, item_id))
        conn.commit()
        print(f"✓ Valor do item {item_id} atualizado para {new_value:,}")
    except Exception as e:
        print(f"❌ Erro ao atualizar item: {e}")

def get_item_details(conn, item_id):
    """Obtém detalhes de um item"""
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM Items WHERE Id = ?
    """, (item_id,))
    
    result = cursor.fetchone()
    if result:
        columns = [description[0] for description in cursor.description]
        item = dict(zip(columns, result))
        
        print(f"\n📦 Detalhes do Item #{item_id}:")
        print("-" * 50)
        for key, value in item.items():
            print(f"   {key}: {value}")
    else:
        print(f"❌ Item #{item_id} não encontrado")

def database_info(conn):
    """Exibe informações sobre o banco de dados"""
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("📊 INFORMAÇÕES DO BANCO DE DADOS".center(60, "="))
    print("=" * 60)
    
    # Localização
    print(f"\n📍 Localização: {DB_PATH}")
    
    # Tamanho
    db_size = os.path.getsize(DB_PATH) / (1024 * 1024)  # em MB
    print(f"💾 Tamanho: {db_size:.2f} MB")
    
    # Data de criação
    creation_time = os.path.getctime(DB_PATH)
    from datetime import datetime as dt
    creation_date = dt.fromtimestamp(creation_time).strftime("%d/%m/%Y %H:%M:%S")
    print(f"📅 Criado em: {creation_date}")
    
    # Contagens
    cursor.execute("SELECT COUNT(*) FROM Items")
    items_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM Recipes")
    recipes_count = cursor.fetchone()[0]
    
    print(f"\n✓ Total de itens: {items_count}")
    print(f"✓ Total de receitas: {recipes_count}")

def main():
    """Menu principal"""
    try:
        if not os.path.exists(DB_PATH):
            print("❌ Banco de dados não encontrado!")
            return
        
        conn = sqlite3.connect(DB_PATH)
        
        while True:
            print("\n" + "=" * 60)
            print("🛠️  GERENCIADOR AVANÇADO - MYTHARA DATABASE".center(60, "="))
            print("=" * 60)
            print("\n1. 📦 Ver informações do banco de dados")
            print("2. 💾 Criar backup")
            print("3. 📤 Exportar itens para JSON")
            print("4. 🔍 Procurar item")
            print("5. ➕ Adicionar item customizado")
            print("6. 💰 Alterar valor de um item")
            print("7. 📋 Ver detalhes de um item")
            print("0. ❌ Sair")
            print("-" * 60)
            
            choice = input("Escolha uma opção: ").strip()
            
            if choice == "0":
                print("✅ Até logo!")
                break
            elif choice == "1":
                database_info(conn)
            elif choice == "2":
                backup_database()
            elif choice == "3":
                export_items_to_json(conn)
            elif choice == "4":
                search_term = input("Digite o nome do item: ").strip()
                if search_term:
                    search_item(conn, search_term)
            elif choice == "5":
                print("\n➕ Adicionar novo item:")
                name = input("   Nome: ").strip()
                category = input("   Categoria (Equipment/Weapons/Consumables/etc): ").strip()
                rarity = input("   Raridade (Common/Uncommon/Rare/Epic/Legendary/Divine/Mystic): ").strip()
                value = input("   Valor (padrão 0): ").strip()
                description = input("   Descrição (opcional): ").strip()
                
                if name and category:
                    try:
                        value = int(value) if value else 0
                        add_custom_item(conn, name, category, rarity, value, description)
                    except ValueError:
                        print("❌ Valor deve ser um número!")
            elif choice == "6":
                try:
                    item_id = int(input("ID do item: "))
                    new_value = int(input("Novo valor: "))
                    update_item_value(conn, item_id, new_value)
                except ValueError:
                    print("❌ Valores devem ser números!")
            elif choice == "7":
                try:
                    item_id = int(input("ID do item: "))
                    get_item_details(conn, item_id)
                except ValueError:
                    print("❌ ID deve ser um número!")
            
            input("\nPressione ENTER para continuar...")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
