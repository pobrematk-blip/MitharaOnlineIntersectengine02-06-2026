#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inspecionar e consultar o banco de dados do MYTHARA
"""

import sqlite3
import os
import sys

PROJECT_ROOT = r"c:\Users\Wesley\Desktop\meu jogo 3d 3 os assets\🌍 MYTHARA Gurra de Raças 17-10-2025"
DB_PATH = os.path.join(PROJECT_ROOT, "Server", "gamedata.db")

def print_header(title):
    """Imprime um cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(title.center(80, "="))
    print("=" * 80)

def show_menu():
    """Exibe menu de opções"""
    print_header("🎮 GERENCIADOR DE BANCO DE DADOS - MYTHARA")
    print("\n1. 📊 Ver estatísticas gerais")
    print("2. 🔍 Listar todos os itens (com paginação)")
    print("3. 📂 Listar itens por categoria")
    print("4. ⭐ Listar itens por raridade")
    print("5. 🎁 Listar itens de equipamento")
    print("6. ⚔️  Listar armas")
    print("7. 🍔 Listar consumíveis")
    print("8. 💎 Itens mais valiosos")
    print("9. 📜 Ver estrutura do banco de dados")
    print("0. ❌ Sair")
    print("\n" + "-" * 80)

def view_statistics(conn):
    """Exibe estatísticas gerais"""
    cursor = conn.cursor()
    
    print_header("📊 ESTATÍSTICAS GERAIS")
    
    # Total
    cursor.execute("SELECT COUNT(*) FROM Items")
    total = cursor.fetchone()[0]
    print(f"\n✓ Total de itens: {total}")
    
    # Por categoria
    print("\n📂 Itens por categoria:")
    cursor.execute("""
    SELECT Category, COUNT(*) as qty 
    FROM Items 
    GROUP BY Category 
    ORDER BY qty DESC
    """)
    for cat, qty in cursor.fetchall():
        print(f"   • {cat}: {qty}")
    
    # Por raridade
    print("\n⭐ Itens por raridade:")
    cursor.execute("""
    SELECT Rarity, COUNT(*) as qty 
    FROM Items 
    GROUP BY Rarity 
    ORDER BY qty DESC
    """)
    for rarity, qty in cursor.fetchall():
        print(f"   • {rarity}: {qty}")
    
    # Valor
    cursor.execute("SELECT SUM(Value), AVG(Value), MAX(Value) FROM Items")
    total_value, avg_value, max_value = cursor.fetchone()
    print(f"\n💰 Valores:")
    print(f"   • Total: {total_value:,}")
    print(f"   • Média: {avg_value:,.2f}")
    print(f"   • Máximo: {max_value:,}")

def list_all_items(conn, page=1):
    """Lista todos os itens com paginação"""
    cursor = conn.cursor()
    items_per_page = 20
    offset = (page - 1) * items_per_page
    
    # Conta total
    cursor.execute("SELECT COUNT(*) FROM Items")
    total = cursor.fetchone()[0]
    total_pages = (total + items_per_page - 1) // items_per_page
    
    print_header(f"📋 TODOS OS ITENS (Página {page}/{total_pages})")
    
    cursor.execute("""
    SELECT Id, Name, Category, Rarity, Value 
    FROM Items 
    ORDER BY Category, Rarity DESC, Name 
    LIMIT ? OFFSET ?
    """, (items_per_page, offset))
    
    print(f"\n{'ID':<6} {'Nome':<35} {'Categoria':<20} {'Raridade':<12} {'Valor':<8}")
    print("-" * 80)
    
    for item_id, name, category, rarity, value in cursor.fetchall():
        print(f"{item_id:<6} {name:<35} {category:<20} {rarity:<12} {value:<8,}")
    
    print(f"\n← Página {page}/{total_pages} → (Digite número da página, ou '0' para voltar)")

def list_by_category(conn):
    """Lista itens por categoria"""
    cursor = conn.cursor()
    
    # Obtém categorias
    cursor.execute("SELECT DISTINCT Category FROM Items ORDER BY Category")
    categories = [row[0] for row in cursor.fetchall()]
    
    print_header("📂 SELECIONE UMA CATEGORIA")
    for idx, cat in enumerate(categories, 1):
        cursor.execute("SELECT COUNT(*) FROM Items WHERE Category = ?", (cat,))
        count = cursor.fetchone()[0]
        print(f"{idx:2}. {cat:<30} ({count} itens)")
    
    try:
        choice = int(input("\nDigite o número da categoria (0 para voltar): "))
        if 0 < choice <= len(categories):
            category = categories[choice - 1]
            cursor.execute("""
            SELECT Id, Name, Rarity, Value 
            FROM Items 
            WHERE Category = ? 
            ORDER BY Rarity DESC, Name
            """, (category,))
            
            items = cursor.fetchall()
            print_header(f"📂 {category} ({len(items)} itens)")
            
            print(f"\n{'ID':<6} {'Nome':<40} {'Raridade':<12} {'Valor':<8}")
            print("-" * 70)
            
            for item_id, name, rarity, value in items:
                print(f"{item_id:<6} {name:<40} {rarity:<12} {value:<8,}")
    except ValueError:
        pass

def list_by_rarity(conn):
    """Lista itens por raridade"""
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT DISTINCT Rarity FROM Items 
    ORDER BY 
        CASE Rarity
            WHEN 'Legendary' THEN 1
            WHEN 'Divine' THEN 2
            WHEN 'Mystic' THEN 3
            WHEN 'Epic' THEN 4
            WHEN 'Rare' THEN 5
            WHEN 'Uncommon' THEN 6
            WHEN 'Common' THEN 7
        END
    """)
    
    rarities = [row[0] for row in cursor.fetchall()]
    
    print_header("⭐ SELECIONE UMA RARIDADE")
    for idx, rarity in enumerate(rarities, 1):
        cursor.execute("SELECT COUNT(*) FROM Items WHERE Rarity = ?", (rarity,))
        count = cursor.fetchone()[0]
        print(f"{idx}. {rarity:<20} ({count} itens)")
    
    try:
        choice = int(input("\nDigite o número (0 para voltar): "))
        if 0 < choice <= len(rarities):
            rarity = rarities[choice - 1]
            cursor.execute("""
            SELECT Id, Name, Category, Value 
            FROM Items 
            WHERE Rarity = ? 
            ORDER BY Value DESC, Name
            """, (rarity,))
            
            items = cursor.fetchall()
            print_header(f"⭐ {rarity} ({len(items)} itens)")
            
            print(f"\n{'ID':<6} {'Nome':<40} {'Categoria':<20} {'Valor':<8}")
            print("-" * 78)
            
            for item_id, name, category, value in items:
                print(f"{item_id:<6} {name:<40} {category:<20} {value:<8,}")
    except ValueError:
        pass

def list_equipments(conn):
    """Lista itens de equipamento"""
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT Id, Name, Rarity, Value 
    FROM Items 
    WHERE Category = 'Equipment' 
    ORDER BY Rarity DESC, Value DESC
    """)
    
    items = cursor.fetchall()
    print_header(f"🎁 EQUIPAMENTOS ({len(items)} itens)")
    
    print(f"\n{'ID':<6} {'Nome':<40} {'Raridade':<12} {'Valor':<8}")
    print("-" * 70)
    
    for item_id, name, rarity, value in items:
        print(f"{item_id:<6} {name:<40} {rarity:<12} {value:<8,}")

def list_weapons(conn):
    """Lista armas"""
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT Id, Name, Rarity, Value 
    FROM Items 
    WHERE Category = 'Weapons' 
    ORDER BY Rarity DESC, Value DESC
    """)
    
    items = cursor.fetchall()
    print_header(f"⚔️ ARMAS ({len(items)} itens)")
    
    print(f"\n{'ID':<6} {'Nome':<40} {'Raridade':<12} {'Valor':<8}")
    print("-" * 70)
    
    for item_id, name, rarity, value in items:
        print(f"{item_id:<6} {name:<40} {rarity:<12} {value:<8,}")

def list_consumables(conn):
    """Lista consumíveis"""
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT Id, Name, Rarity, Value 
    FROM Items 
    WHERE Category = 'Consumables' 
    ORDER BY Rarity DESC, Value DESC
    """)
    
    items = cursor.fetchall()
    print_header(f"🍔 CONSUMÍVEIS ({len(items)} itens)")
    
    print(f"\n{'ID':<6} {'Nome':<40} {'Raridade':<12} {'Valor':<8}")
    print("-" * 70)
    
    for item_id, name, rarity, value in items:
        print(f"{item_id:<6} {name:<40} {rarity:<12} {value:<8,}")

def most_valuable_items(conn):
    """Lista os itens mais valiosos"""
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT Id, Name, Category, Rarity, Value 
    FROM Items 
    ORDER BY Value DESC 
    LIMIT 50
    """)
    
    items = cursor.fetchall()
    print_header("💎 50 ITENS MAIS VALIOSOS")
    
    print(f"\n{'ID':<6} {'Nome':<35} {'Categoria':<20} {'Raridade':<12} {'Valor':<8}")
    print("-" * 83)
    
    for idx, (item_id, name, category, rarity, value) in enumerate(items, 1):
        print(f"{item_id:<6} {name:<35} {category:<20} {rarity:<12} {value:<8,}")

def show_database_structure(conn):
    """Mostra a estrutura do banco de dados"""
    cursor = conn.cursor()
    
    print_header("📜 ESTRUTURA DO BANCO DE DADOS")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    for table_name, in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"\n📋 Tabela: {table_name}")
        print("-" * 60)
        print(f"{'Coluna':<20} {'Tipo':<15} {'Propriedades':<25}")
        print("-" * 60)
        
        for col_id, name, type_, notnull, dflt_value, pk in columns:
            props = []
            if pk:
                props.append("PRIMARY KEY")
            if notnull:
                props.append("NOT NULL")
            if dflt_value:
                props.append(f"DEFAULT {dflt_value}")
            
            props_str = ", ".join(props) if props else "-"
            print(f"{name:<20} {type_:<15} {props_str:<25}")

def main():
    """Função principal"""
    try:
        if not os.path.exists(DB_PATH):
            print("❌ Banco de dados não encontrado!")
            print(f"Localização esperada: {DB_PATH}")
            return
        
        conn = sqlite3.connect(DB_PATH)
        page = 1
        
        while True:
            show_menu()
            choice = input("Escolha uma opção: ").strip()
            
            if choice == "0":
                print("\n✅ Até logo!")
                break
            elif choice == "1":
                view_statistics(conn)
            elif choice == "2":
                list_all_items(conn, page)
                page_input = input("\nDigite a página: ").strip()
                if page_input.isdigit() and int(page_input) > 0:
                    page = int(page_input)
            elif choice == "3":
                list_by_category(conn)
            elif choice == "4":
                list_by_rarity(conn)
            elif choice == "5":
                list_equipments(conn)
            elif choice == "6":
                list_weapons(conn)
            elif choice == "7":
                list_consumables(conn)
            elif choice == "8":
                most_valuable_items(conn)
            elif choice == "9":
                show_database_structure(conn)
            
            input("\nPressione ENTER para continuar...")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
