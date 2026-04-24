# Guia rápido para agentes de código (Copilot / AI)

Objetivo: fornecer o contexto essencial para que agentes assistentes sejam produtivos rapidamente neste repositório.

---

## Visão geral (big picture)
- Projeto distribuído do motor Intersect: contém artefatos binários (Client/ e Server/) + recursos (JSON, sprites, tiles, etc.) e documentação XML (Intersect.*.xml). Não há arquivos de projeto fonte (.sln/.csproj) neste diretório.
- Componentes principais:
  - Server/: ASP.NET Core server (binários, EF Core *migrations* presentes nos metadados XML). Configurações e dados do jogo ficam em `Server/resources/`.
  - Client/: Aplicativo desktop (MonoGame / .NET), Editor e recursos do jogo em `Client/resources/`.
  - Web: `Server/wwwroot/` contém UI e assets estáticos para administração/identidade.
- Rede: cliente e servidor se comunicam via porta configurável (padrão 5400 — ver `Server/resources/config.json` e `Client/resources/config.json`) usando LiteNetLib (biblioteca incluída).

## Onde olhar primeiro (trabalho prático)
- Configuração do servidor: `Server/resources/config.json` — contém portas, DB type (SQLite/MySQL), limite de jogadores, timers, opções de combate etc. Ex.: `"ServerPort": 5400`.
- Fórmulas / balanceamento: `Server/resources/formulas.json` — equações de dano/exp.
- Conteúdo do jogo (descritores): `Server/resources/spells/`, `Server/resources/items/`, `Server/resources/tilesets/`, `Server/resources/entities/` etc. Alterações aqui mudam comportamento no runtime.
- Cliente: `Client/resources/config.json` (host/port, fontes, UI skin), assets em `Client/resources/images/`, `tilesets/`, `paperdolls/`.
- Logs: `Server/logs/` e `Client/logs/` (ponto inicial para reproduzir e diagnosticar problemas).

## Fluxos de desenvolvimento e execução
- Execução local (básico): abrir e executar os binários em `Server/` e `Client/`: `Server\Intersect Server.exe` e `Client\Intersect Client.exe` (Windows). O Editor é `Client\Intersect Editor.exe`.
- Migrações/DB: metadados XML provam que o servidor usa EF Core com migrações para SQLite/MySQL; mensagens de `Server/resources/server_strings.json` indicam uma workflow de migração (ex.: "Starting migration").
- Depuração: PDBs estão incluídos para várias DLLs (ex.: `LiteNetLib.pdb`) — útil para attach/debug se você tiver o código fonte correspondente.

## Padrões e convenções do projeto
- Arquivos de configuração e descritores do jogo são JSON com chaves em PascalCase (ex.: `Server/resources/config.json`).
- Assets organizados por tipo/função: `images/`, `spells/`, `items/`, `tilesets/`, `paperdolls/` — nome e estrutura esperada são usados em runtime.
- Mapas e tiles assumem 32×32 por padrão (`Server/resources/config.json`: `TileWidth` / `TileHeight`).

## Integrações e dependências externas relevantes
- Rede: LiteNetLib (bibliotecas presentes em `Client/` e `Server/`).
- Cliente: MonoGame (presença de `MonoGame.Framework.Client.dll`).
- DB: suporta SQLite por padrão (e arquivos binários de sqlite embalados); também há suporte a MySQL/MariaDB (MySql migrations aparecem nos docs).
- Web/Identity: `Server/wwwroot/Identity/` contém assets do fluxo de autenticação.

## O que NÃO está aqui (ou é importante verificar antes de editar)
- Não encontrei projetos C# (.sln/.csproj) ou código fonte editável neste snapshot — alterações profundas na lógica do servidor/cliente geralmente exigirão o repositório fonte original ou um fork.

## Boas tarefas para um agente
- Quando solicitado a alterar comportamento do jogo, preferir mudanças em `Server/resources/*` (spells, items, formulas, config) quando possível, pois são mudanças detectáveis em runtime.
- Ao investigar bugs, coletar logs de `Server/logs` e `Client/logs` e checar `config.json` (timeouts, ports, DB type).
- Para mudanças de UI/assets, verificar `Client/resources/` e, se necessário, `Server/wwwroot/` para partes web.

## Exemplos práticos (quick snippets)
- Para alterar host/porta que o cliente conecta: editar `Client/resources/config.json` — ex.:
  - "Host": "26.109.183.50"
  - "Port": 5400
- Para ajustar tempo de respawn de itens no mapa: `Server/resources/config.json` → `Map.ItemAttributeRespawnTime`.

---

Se quiser, eu posso:
- 1) Adicionar links para o repositório upstream (se você fornecer) e comandos de build para o código fonte real.
- 2) Inserir um pequeno checklist de validação (como: "iniciar server, iniciar client, verificar logs, validar rota X") para mudanças típicas.

Por favor, informe se quer que eu inclua exemplos de comandos exatos para execução/depuração na sua máquina (PowerShell/Windows) ou se deseja que eu procure um repositório fonte relacionado para completar o guia. Obrigado!