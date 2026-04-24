#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar banco de dados SQLite com todos os itens do jogo MYTHARA
"""

import sqlite3
import os
import json
from pathlib import Path
from datetime import datetime

# Paths
PROJECT_ROOT = r"c:\Users\Wesley\Desktop\meu jogo 3d 3 os assets\🌍 MYTHARA Gurra de Raças 17-10-2025"
DB_PATH = os.path.join(PROJECT_ROOT, "Server", "gamedata.db")
ITEMS_PATH = os.path.join(PROJECT_ROOT, "Client", "resources", "items")

# Categorias de itens baseadas no nome das imagens
ITEM_CATEGORIES = {
    "Equipment": [
        "Armor", "Breastplate", "Helmet", "Boots", "Gloves", "Cloak",
        "Escudo", "Shield", "Couraça", "Capacete", "Botas", "Luva", "Manto"
    ],
    "Weapons": [
        "Sword", "Bow", "Staff", "Hammer", "Axe", "Spear", "Mace", "Knife",
        "Espada", "Arco", "Cajado", "Machado", "Martelo", "Lança", "Adaga"
    ],
    "Accessories": [
        "Ring", "Necklace", "Bracelet", "Crown", "Jewel",
        "Anel", "Colar", "Pulseira", "Coroa", "Joia"
    ],
    "Consumables": [
        "Potion", "Food", "Comida", "Poção", "Porção",
        "Pão", "Cerveja", "Vinho", "Alho", "Cebola"
    ],
    "Crafting Materials": [
        "Ore", "Ingot", "Wood", "Paper", "Rope", "Herb", "Mushroom",
        "Minério", "Barra", "Madeira", "Papel", "Corda", "Erva", "Cogumelo",
        "Lamina", "Cola", "Farinha", "Sal"
    ],
    "Quest Items": [
        "Key", "Map", "Scroll", "Pergaminho", "Mapa", "Chave",
        "Pedaço de mapa", "Runa magica"
    ],
    "Resources": [
        "Flower", "Leaf", "Mushroom", "Worm", "Fish",
        "Flor", "Folha", "Cogumelo", "Minhoca", "Peixe",
        "isca", "Linha", "Vara de pesca"
    ],
    "Books": [
        "Book", "Livro", "Receita", "Papyrus"
    ],
    "Misc": [
        "Misc", "Dices", "Vaso", "Vela", "Badges", "Icon",
        "Comum", "Raro", "Incomum", "Epico", "Lendario", "Divino", "Mistico",
        "Vip"
    ]
}

def get_item_category(filename):
    """Determina a categoria de um item baseado no nome do arquivo"""
    filename_lower = filename.lower()
    
    for category, keywords in ITEM_CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in filename_lower:
                return category
    
    return "Misc"

def get_item_rarity(filename):
    """Determina a raridade do item baseado no nome"""
    filename_lower = filename.lower()
    
    if "lendario" in filename_lower or "legendary" in filename_lower:
        return "Legendary"
    elif "divino" in filename_lower or "divine" in filename_lower:
        return "Divine"
    elif "epico" in filename_lower or "epic" in filename_lower:
        return "Epic"
    elif "mistico" in filename_lower or "mystic" in filename_lower:
        return "Mystic"
    elif "raro" in filename_lower or "rare" in filename_lower:
        return "Rare"
    elif "incomum" in filename_lower or "uncommon" in filename_lower:
        return "Uncommon"
    elif "comum" in filename_lower or "common" in filename_lower:
        return "Common"
    else:
        return "Common"

def create_database():
    """Cria o banco de dados SQLite com tabelas"""
    
    # Remove DB existente se houver
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✓ Banco de dados anterior removido")
    
    # Cria o banco de dados
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela de ITEMS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Items (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE,
        Description TEXT,
        ItemType INTEGER DEFAULT 0,
        Category TEXT,
        Value INTEGER DEFAULT 0,
        Rarity TEXT DEFAULT "Common",
        IsStackable INTEGER DEFAULT 1,
        MaxStack INTEGER DEFAULT 99,
        IconId TEXT,
        Icon_Filename TEXT,
        CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela de ITEM_ATTRIBUTES (propriedades equipáveis)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ItemAttributes (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemId INTEGER,
        AttributeName TEXT,
        AttributeValue INTEGER,
        FOREIGN KEY(ItemId) REFERENCES Items(Id)
    )
    ''')
    
    # Tabela de RECIPES (receitas de craft)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Recipes (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        ResultItemId INTEGER,
        ResultQuantity INTEGER DEFAULT 1,
        CraftTime INTEGER DEFAULT 1,
        FOREIGN KEY(ResultItemId) REFERENCES Items(Id)
    )
    ''')
    
    # Tabela de RECIPE_INGREDIENTS
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS RecipeIngredients (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        RecipeId INTEGER,
        ItemId INTEGER,
        Quantity INTEGER DEFAULT 1,
        FOREIGN KEY(RecipeId) REFERENCES Recipes(Id),
        FOREIGN KEY(ItemId) REFERENCES Items(Id)
    )
    ''')
    
    conn.commit()
    print("✓ Tabelas criadas com sucesso")
    
    return conn

def populate_items(conn):
    """Popula o banco de dados com os itens do jogo"""
    
    if not os.path.exists(ITEMS_PATH):
        print(f"⚠ Pasta de itens não encontrada: {ITEMS_PATH}")
        return 0
    
    cursor = conn.cursor()
    items_added = 0
    
    # Obtém lista de arquivos PNG na pasta de itens
    item_files = [f for f in os.listdir(ITEMS_PATH) if f.lower().endswith('.png')]
    
    print(f"\n📦 Processando {len(item_files)} itens...")
    
    for idx, filename in enumerate(sorted(item_files), 1):
        # Remove extensão e normaliza nome
        item_name = os.path.splitext(filename)[0]
        
        # Extrai informações
        category = get_item_category(filename)
        rarity = get_item_rarity(filename)
        
        # Define valor base de venda
        base_value = 0
        if rarity == "Common":
            base_value = 10
        elif rarity == "Uncommon":
            base_value = 50
        elif rarity == "Rare":
            base_value = 100
        elif rarity == "Epic":
            base_value = 500
        elif rarity == "Legendary":
            base_value = 1000
        elif rarity == "Divine":
            base_value = 2000
        elif rarity == "Mystic":
            base_value = 3000
        
        try:
            cursor.execute('''
            INSERT INTO Items (Name, Description, Category, Value, Rarity, Icon_Filename)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item_name,
                f"{item_name} ({rarity})",
                category,
                base_value,
                rarity,
                filename
            ))
            items_added += 1
            
            if idx % 100 == 0:
                print(f"  ✓ {idx}/{len(item_files)} itens processados...")
            
        except sqlite3.IntegrityError:
            # Item duplicado, ignora
            pass
        except Exception as e:
            print(f"  ⚠ Erro ao adicionar {filename}: {e}")
    
    conn.commit()
    print(f"✓ {items_added} itens adicionados ao banco de dados")
    
    return items_added

def add_sample_recipes(conn):
    """Adiciona algumas receitas de exemplo"""
    cursor = conn.cursor()
    
    recipies_added = 0
    
    try:
        # Procura por itens que parecem ser materiais crafting
        cursor.execute('''
        SELECT Id, Name FROM Items 
        WHERE Category = "Crafting Materials" 
        LIMIT 10
        ''')
        
        materials = cursor.fetchall()
        
        if len(materials) >= 2:
            # Cria receita de exemplo: 2 minérios = 1 barra
            material1_id, material1_name = materials[0]
            material2_id, material2_name = materials[1]
            
            try:
                # Procura item tipo "barra" ou "ingot"
                cursor.execute('''
                SELECT Id FROM Items 
                WHERE Name LIKE "%Ingot%" OR Name LIKE "%Barra%" 
                LIMIT 1
                ''')
                
                result = cursor.fetchone()
                if result:
                    ingot_id = result[0]
                    
                    cursor.execute('''
                    INSERT INTO Recipes (Name, ResultItemId, ResultQuantity, CraftTime)
                    VALUES (?, ?, ?, ?)
                    ''', (
                        f"Craft {materials[0][1]}",
                        ingot_id,
                        1,
                        5
                    ))
                    
                    recipies_added += 1
                    conn.commit()
            except:
                pass
    except:
        pass
    
    if recipies_added > 0:
        print(f"✓ {recipies_added} receita(s) de exemplo adicionadas")

def display_statistics(conn):
    """Exibe estatísticas do banco de dados"""
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS DO BANCO DE DADOS ".center(60, "="))
    print("="*60)
    
    # Total de itens
    cursor.execute("SELECT COUNT(*) FROM Items")
    total_items = cursor.fetchone()[0]
    print(f"\n✓ Total de itens: {total_items}")
    
    # Itens por categoria
    cursor.execute("""
    SELECT Category, COUNT(*) as count 
    FROM Items 
    GROUP BY Category 
    ORDER BY count DESC
    """)
    
    print("\n📂 Itens por categoria:")
    for category, count in cursor.fetchall():
        print(f"   • {category}: {count}")
    
    # Itens por raridade
    cursor.execute("""
    SELECT Rarity, COUNT(*) as count 
    FROM Items 
    GROUP BY Rarity 
    ORDER BY count DESC
    """)
    
    print("\n⭐ Itens por raridade:")
    for rarity, count in cursor.fetchall():
        print(f"   • {rarity}: {count}")
    
    # Valor total de todos os itens
    cursor.execute("SELECT SUM(Value) FROM Items")
    total_value = cursor.fetchone()[0] or 0
    print(f"\n💰 Valor total de todos os itens: {total_value:,}")
    
    print("\n" + "="*60)

def main():
    """Função principal"""
    print("\n" + "🎮 CRIADOR DE BANCO DE DADOS - MYTHARA ".center(70, "="))
    print("=" * 70)
    
    try:
        # Cria banco de dados
        conn = create_database()
        
        # Popula com itens
        items_count = populate_items(conn)
        
        # Adiciona receitas de exemplo
        add_sample_recipes(conn)
        
        # Exibe estatísticas
        display_statistics(conn)
        
        # Fecha conexão
        conn.close()
        
        print(f"\n✅ Banco de dados criado com sucesso em:")
        print(f"   {DB_PATH}")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n❌ Erro ao criar banco de dados: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
