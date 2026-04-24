#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar uma planilha HTML interativa com todos os itens do MYTHARA
"""

import sqlite3
import os
from datetime import datetime

PROJECT_ROOT = r"c:\Users\Wesley\Desktop\meu jogo 3d 3 os assets\🌍 MYTHARA Gurra de Raças 17-10-2025"
DB_PATH = os.path.join(PROJECT_ROOT, "Server", "gamedata.db")
HTML_OUTPUT = os.path.join(PROJECT_ROOT, "MYTHARA_Items_Database.html")

# Cores para raridades
RARITY_COLORS = {
    "Common": "#D3D3D3",
    "Uncommon": "#90EE90",
    "Rare": "#87CEEB",
    "Epic": "#DDA0DD",
    "Legendary": "#FFD700",
    "Divine": "#FF69B4",
    "Mystic": "#9370DB"
}

def get_html_header():
    """Retorna o header HTML com estilos"""
    return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MYTHARA - Database de Itens</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #366092 0%, #4472C4 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .controls {
            background: #f5f5f5;
            padding: 20px;
            border-bottom: 1px solid #ddd;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }

        .control-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .control-group label {
            font-weight: 600;
            color: #333;
        }

        select, input[type="text"], input[type="number"] {
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
            transition: border-color 0.3s;
        }

        select:focus, input:focus {
            outline: none;
            border-color: #366092;
            box-shadow: 0 0 5px rgba(54, 96, 146, 0.3);
        }

        button {
            padding: 8px 15px;
            background: #366092;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 600;
            transition: background 0.3s;
        }

        button:hover {
            background: #2a4a7a;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            padding: 20px;
            background: #f9f9f9;
            border-bottom: 1px solid #ddd;
        }

        .stat-box {
            background: white;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #366092;
        }

        .stat-box h3 {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }

        .stat-box .value {
            font-size: 1.8em;
            font-weight: bold;
            color: #366092;
        }

        .table-wrapper {
            overflow-x: auto;
            padding: 20px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        thead {
            background: #366092;
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
        }

        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #366092;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }

        tbody tr {
            transition: background 0.2s;
        }

        tbody tr:hover {
            background: #f5f5f5;
        }

        tbody tr:nth-child(even) {
            background: #fafafa;
        }

        .id {
            width: 60px;
            text-align: center;
            color: #999;
        }

        .name {
            font-weight: 500;
            color: #333;
        }

        .category {
            text-align: center;
            padding: 5px 10px;
            border-radius: 3px;
            background: #f0f0f0;
            font-size: 0.9em;
        }

        .rarity {
            font-weight: bold;
            text-align: center;
            padding: 5px 10px;
            border-radius: 3px;
            color: #333;
        }

        .value {
            text-align: right;
            font-weight: 600;
            color: #366092;
        }

        .stackable {
            text-align: center;
            color: #666;
        }

        .description {
            color: #666;
            font-size: 0.95em;
            max-width: 300px;
        }

        .no-results {
            padding: 40px;
            text-align: center;
            color: #999;
            font-size: 1.1em;
        }

        .footer {
            background: #f5f5f5;
            padding: 20px;
            text-align: center;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }

        .tabs {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 15px;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }

        .tab-btn {
            padding: 10px 15px;
            background: #f0f0f0;
            border: none;
            border-radius: 5px 5px 0 0;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            border-bottom: 3px solid transparent;
        }

        .tab-btn:hover {
            background: #e0e0e0;
        }

        .tab-btn.active {
            background: #366092;
            color: white;
            border-bottom-color: #366092;
        }

        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }

        @media print {
            body {
                background: white;
            }
            .controls {
                display: none;
            }
            .tabs {
                display: none;
            }
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            .control-group {
                flex-direction: column;
            }
            table {
                font-size: 0.9em;
            }
            th, td {
                padding: 8px 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 MYTHARA - Database de Itens</h1>
            <p>Catálogo Completo de Todos os Itens do Jogo</p>
        </div>
"""

def get_html_footer():
    """Retorna o footer HTML"""
    return """
        <div class="footer">
            <p>MYTHARA Items Database | Gerado em 24 de Abril de 2026</p>
            <p>Total de itens: <strong>2.311</strong> | Todas as categorias incluídas</p>
        </div>
    </div>
    
    <script>
        function filterTable() {
            const categoryFilter = document.getElementById('categoryFilter').value;
            const rarityFilter = document.getElementById('rarityFilter').value;
            const nameFilter = document.getElementById('nameFilter').value.toLowerCase();
            const minValue = parseInt(document.getElementById('minValue').value) || 0;
            const maxValue = parseInt(document.getElementById('maxValue').value) || Infinity;
            
            const table = document.querySelector('table tbody');
            const rows = table.querySelectorAll('tr');
            let visibleCount = 0;
            
            rows.forEach(row => {
                const category = row.getAttribute('data-category');
                const rarity = row.getAttribute('data-rarity');
                const name = row.getAttribute('data-name').toLowerCase();
                const value = parseInt(row.getAttribute('data-value'));
                
                const categoryMatch = categoryFilter === '' || category === categoryFilter;
                const rarityMatch = rarityFilter === '' || rarity === rarityFilter;
                const nameMatch = name.includes(nameFilter);
                const valueMatch = value >= minValue && value <= maxValue;
                
                if (categoryMatch && rarityMatch && nameMatch && valueMatch) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            const noResults = document.querySelector('.no-results');
            if (visibleCount === 0) {
                if (!noResults) {
                    const div = document.createElement('div');
                    div.className = 'no-results';
                    div.textContent = 'Nenhum item encontrado com os filtros selecionados.';
                    table.parentElement.appendChild(div);
                }
            } else {
                if (noResults) {
                    noResults.remove();
                }
            }
            
            updateStats();
        }
        
        function updateStats() {
            const rows = document.querySelectorAll('table tbody tr:not([style*="display: none"])');
            document.getElementById('visibleCount').textContent = rows.length;
        }
        
        function resetFilters() {
            document.getElementById('categoryFilter').value = '';
            document.getElementById('rarityFilter').value = '';
            document.getElementById('nameFilter').value = '';
            document.getElementById('minValue').value = '';
            document.getElementById('maxValue').value = '';
            filterTable();
        }
        
        function exportToCSV() {
            const rows = document.querySelectorAll('table tbody tr:not([style*="display: none"])');
            let csv = 'ID,Nome,Categoria,Raridade,Valor,Empilhável,Máx Stack\\n';
            
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                csv += `${cells[0].textContent},${cells[1].textContent},${cells[2].textContent},${cells[3].textContent},${cells[4].textContent},${cells[5].textContent},${cells[6].textContent}\\n`;
            });
            
            const link = document.createElement('a');
            link.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
            link.download = 'MYTHARA_Items.csv';
            link.click();
        }
        
        // Inicializar filtros ao carregar
        document.addEventListener('DOMContentLoaded', filterTable);
    </script>
</body>
</html>
"""

def generate_html():
    """Gera o arquivo HTML"""
    print("\n" + "=" * 70)
    print("🌐 CRIADOR DE PLANILHA HTML - MYTHARA".center(70, "="))
    print("=" * 70)
    
    try:
        if not os.path.exists(DB_PATH):
            print(f"\n❌ Banco de dados não encontrado: {DB_PATH}")
            return 1
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print(f"\n✓ Conectado ao banco de dados")
        
        # Inicia HTML
        html = get_html_header()
        
        # Obtém estatísticas
        cursor.execute("SELECT COUNT(*) FROM Items")
        total_items = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(Value) FROM Items")
        total_value = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(DISTINCT Category) FROM Items")
        total_categories = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(Value) FROM Items")
        avg_value = cursor.fetchone()[0] or 0
        
        # Seção de Estatísticas
        html += f"""
        <div class="stats">
            <div class="stat-box">
                <h3>Total de Itens</h3>
                <div class="value">{total_items}</div>
            </div>
            <div class="stat-box">
                <h3>Categorias</h3>
                <div class="value">{total_categories}</div>
            </div>
            <div class="stat-box">
                <h3>Valor Total</h3>
                <div class="value">{total_value:,}</div>
            </div>
            <div class="stat-box">
                <h3>Valor Médio</h3>
                <div class="value">{avg_value:.0f}</div>
            </div>
            <div class="stat-box">
                <h3>Itens Visíveis</h3>
                <div class="value" id="visibleCount">0</div>
            </div>
        </div>
"""
        
        # Controles de filtro
        cursor.execute("SELECT DISTINCT Category FROM Items ORDER BY Category")
        categories = [row[0] for row in cursor.fetchall()]
        
        html += """
        <div class="controls">
            <div class="control-group">
                <label for="categoryFilter">📂 Categoria:</label>
                <select id="categoryFilter" onchange="filterTable()">
                    <option value="">Todas as Categorias</option>
"""
        
        for category in categories:
            html += f'                    <option value="{category}">{category}</option>\n'
        
        html += """
                </select>
            </div>
            
            <div class="control-group">
                <label for="rarityFilter">⭐ Raridade:</label>
                <select id="rarityFilter" onchange="filterTable()">
                    <option value="">Todas as Raridades</option>
                    <option value="Legendary">Legendary</option>
                    <option value="Divine">Divine</option>
                    <option value="Mystic">Mystic</option>
                    <option value="Epic">Epic</option>
                    <option value="Rare">Rare</option>
                    <option value="Uncommon">Uncommon</option>
                    <option value="Common">Common</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="nameFilter">🔍 Procurar:</label>
                <input type="text" id="nameFilter" placeholder="Nome do item..." onkeyup="filterTable()">
            </div>
            
            <div class="control-group">
                <label for="minValue">💰 Valor Min:</label>
                <input type="number" id="minValue" placeholder="0" onchange="filterTable()">
            </div>
            
            <div class="control-group">
                <label for="maxValue">até Max:</label>
                <input type="number" id="maxValue" placeholder="99999" onchange="filterTable()">
            </div>
            
            <button onclick="resetFilters()">🔄 Limpar Filtros</button>
            <button onclick="exportToCSV()">📥 Exportar CSV</button>
            <button onclick="window.print()">🖨️ Imprimir</button>
        </div>
"""
        
        # Tabela de itens
        html += """
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th class="id">ID</th>
                        <th>Nome</th>
                        <th>Categoria</th>
                        <th>Raridade</th>
                        <th class="value">Valor</th>
                        <th>Empilhável</th>
                        <th>Máx Stack</th>
                        <th>Descrição</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Obtém itens
        cursor.execute("""
            SELECT Id, Name, Category, Rarity, Value, IsStackable, MaxStack, Description
            FROM Items
            ORDER BY Category, Rarity DESC, Value DESC, Name
        """)
        
        items_count = 0
        for item_id, name, category, rarity, value, stackable, max_stack, description in cursor.fetchall():
            stackable_text = "Sim" if stackable else "Não"
            rarity_color = RARITY_COLORS.get(rarity, "#CCCCCC")
            
            html += f"""                    <tr data-id="{item_id}" data-name="{name}" data-category="{category}" data-rarity="{rarity}" data-value="{value}">
                        <td class="id">{item_id}</td>
                        <td class="name">{name}</td>
                        <td><span class="category">{category}</span></td>
                        <td><span class="rarity badge" style="background-color: {rarity_color}; color: {'#000' if rarity in ['Common', 'Uncommon', 'Rare', 'Legendary'] else '#fff'};">{rarity}</span></td>
                        <td class="value">{value:,}</td>
                        <td class="stackable">{stackable_text}</td>
                        <td class="stackable">{max_stack}</td>
                        <td class="description">{description or ''}</td>
                    </tr>
"""
            items_count += 1
            
            if items_count % 500 == 0:
                print(f"  ✓ {items_count}/{total_items} itens processados...")
        
        html += """
                </tbody>
            </table>
        </div>
"""
        
        # Footer
        html += get_html_footer()
        
        # Salva arquivo
        print(f"\n✓ Salvando arquivo HTML...", end="", flush=True)
        with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
            f.write(html)
        print(" ✓")
        
        file_size = os.path.getsize(HTML_OUTPUT) / (1024 * 1024)
        
        print("\n" + "=" * 70)
        print("✅ SUCESSO! PLANILHA HTML CRIADA COM SUCESSO".center(70, "="))
        print("=" * 70)
        
        print(f"\n📊 Resumo:")
        print(f"   • Total de itens: {items_count}")
        print(f"   • Tamanho do arquivo: {file_size:.2f} MB")
        
        print(f"\n📁 Localização:")
        print(f"   {HTML_OUTPUT}")
        
        print(f"\n✨ Recursos:")
        print(f"   ✓ Filtrar por categoria, raridade, valor")
        print(f"   ✓ Procurar por nome")
        print(f"   ✓ Exportar para CSV")
        print(f"   ✓ Imprimir")
        print(f"   ✓ Interface responsiva")
        print(f"   ✓ Tabela interativa e rápida")
        
        print("\n" + "=" * 70)
        
        conn.close()
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(generate_html())
