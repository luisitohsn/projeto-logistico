# Sistema de Monitoração Logística

## Sobre o projeto

Este projeto é um sistema de monitoramento logístico simples em Python, desenvolvido como uma aplicação de terminal que controla usuários, pedidos, rastreamento, veículos e custos.

A arquitetura do projeto é leve e baseada em SQLite. A aplicação oferece:
- autenticação de usuários (`cliente` e `admin`)
- visualização de pedidos do cliente
- rastreamento de pedidos com histórico
- visão de frota e custos para administradores

## Objetivo

O objetivo do sistema é demonstrar uma solução prática para gerenciar operações logísticas básicas em modo texto, incluindo:
- cadastro de usuários e perfis
- gerenciamento de pedidos por cliente
- registro de rastreamento de entregas
- controle de veículos e custos de frete

## Instalação e como configurar o ambiente

### 1. Crie ou ative o ambiente virtual

No PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No CMD:

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

No bash/WSL:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Inicialize o banco de dados e dados de teste

```bash
python seed.py
```

Isso criará as tabelas necessárias no arquivo `logistica.db` e incluirá usuários, veículos, pedido e rastreamento de exemplo.

### 4. Execute a aplicação

```bash
python main.py
```

### 5. Credenciais de exemplo

- `ana` / `1234` → cliente
- `carlos` / `1234` → cliente
- `admin` / `admin` → administrador

## Stacks e Ferramentas usadas

- Python 3.14
- SQLite para persistência local
- `rich` para exibir tabelas formatadas no terminal

## Análise do projeto

### Estrutura principal

- `main.py` — ponto de entrada. Cria tabelas, faz login e direciona para a interface correta de acordo com o perfil.
- `auth.py` — lógica de autenticação, consulta por login e senha no banco.
- `database.py` — gerencia a conexão e criação de tabelas SQLite.
- `seed.py` — popular o banco com dados de teste e corrigir duplicatas existentes.

### Diretórios e módulos

- `models/`
  - `pedidos.py` — consultas de pedidos por cliente, por ID e listagem geral.
  - `rastreamento.py` — histórico de rastreamento e último evento de rastreio.
  - `veiculos.py` — listagem de veículos.
  - `custos.py` — listagem de custos por pedido.
  - `clientes.py` — (não é modelo, mas pode conter lógica futura específica de clientes?)

- `views/`
  - `clientes.py` — menu do cliente para exibir pedidos e rastreamento.
  - `admin.py` — menu de administrador para visualizar todos os pedidos, veículos e custos.

- `utils/display.py` — funções para imprimir tabelas com `rich`.

### Principais melhorias já aplicadas

- `seed.py` agora evita inserção repetida de dados de teste e corrige dados duplicados existentes.
- `views/clientes.py` valida se o pedido pertence ao cliente antes de mostrar o rastreamento.
- `models/rastreamento.py` agora suporta recuperar o histórico completo e apenas o último registro de rastreamento.

## Como usar

1. Execute o programa com `python main.py`.
2. Faça login com um usuário válido.
3. Se for cliente:
   - escolha `1` para ver seus pedidos.
   - escolha `2` para consultar rastreio e, por padrão, mostrar o último registro.
4. Se for administrador:
   - escolha `1` para ver todos os pedidos.
   - escolha `2` para ver a frota de veículos.
   - escolha `3` para ver custos de frete.

## Observações

- O banco de dados está em `logistica.db`.
- O projeto é ideal para estudos e protótipos. Em produção, recomenda-se usar senha criptografada, validação de entrada mais robusta e migrações de banco de dados.
- Caso o terminal exiba problemas com caracteres acentuados no Windows, utilize `chcp 65001` antes de rodar o script ou configure o console para UTF-8.

---

Se quiser, posso também adicionar um item de `Contribuição` e `Roadmap` para a evolução do sistema.