# 🎯 Índice - Como Navegar o Projeto

## 📋 Arquivos Principais

### 🚀 Para Executar
- **`run.py`** ← **COMECE AQUI** - Inicia o servidor Flask
  ```bash
  python run.py
  ```

### 📖 Documentação (Leia na Ordem)
1. **`README.md`** - Visão geral do projeto
2. **`ESTRUTURA.md`** - Arquitetura e como expandir  
3. **`DEPLOY_RAPIDO.md`** - Deploy em 5 minutos
4. **`README_DEPLOY.md`** - Guia completo deployment

### ⚙️ Configuração & Setup
- **`setup_local.py`** - Script automatizado (venv + deps)
- **`requirements.txt`** - Lista de dependências Python
- **`Procfile`** - Para deploy (Render, Heroku)
- **`render.yaml`** - Config específica Render

---

## 🗂️ Estrutura de Pastas

### `src/` - Código-fonte
```
src/
├── app/                    # Interface do usuário
│   ├── templates/         # HTML (Jinja2)
│   └── static/css/        # Estilos CSS
├── core/
│   ├── analysis/          # Motor de análise
│   └── database/          # SQLite
```

### `data/` - Dados
```
data/
├── sample_tickers.csv     # Ativos de amostra
├── sample_prices.csv      # Preços históricos
└── market.sqlite          # ⚙️ Banco de dados
```

---

## 🔄 Fluxo de Desenvolvimento

### 1. **Adicionar Nova Página**
   1. Criar arquivo `src/app/templates/nova_pagina.html`
   2. Adicionar rota em `run.py`
   3. Testar em `http://127.0.0.1:5000/nova-pagina`

### 2. **Adicionar Novo Indicador**
   1. Criar função em `src/core/analysis/indicators.py`
   2. Importar e usar em `src/core/analysis/scoring.py`
   3. Testar localmente

### 3. **Conectar Nova Fonte de Dados**
   1. Adicionar função em `src/core/analysis/data_sources.py`
   2. Atualizar `ingest_latest()` se necessário
   3. Testar com dados de amostra

---

## 📚 Localização de Funcionalidades

| Funcionalidade | Arquivo | Linha |
|---|---|---|
| Iniciar app | `run.py` | 1 |
| Templates HTML | `src/app/templates/` | - |
| Estilos CSS | `src/app/static/css/styles.css` | - |
| Schema DB | `src/core/database/db.py` | ~5 |
| Cálculos de risco | `src/core/analysis/indicators.py` | ~5 |
| Coleta de dados | `src/core/analysis/data_sources.py` | ~20 |
| Scoring de ativos | `src/core/analysis/scoring.py` | ~10 |
| Relatórios | `src/core/analysis/report.py` | ~12 |

---

## 🐛 Troubleshooting Rápido

### ❌ Erro: "Módulo não encontrado"
- Instale: `pip install -r requirements.txt`

### ❌ Erro: "Porta 5000 em uso"
- Mude a porta no `run.py`: `app.run(port=5001)`

### ❌ Dados aparecem vazios
- Execute análise em `http://127.0.0.1:5000/` primeiro

### ❌ CSS não carrega
- Limpe cache: `Ctrl+Shift+Delete` → Cachés vazios

---

## 🚀 Próximos Passos

1. **Local**: `python run.py` → Teste tudo
2. **GitHub**: Envie o código para GitHub
3. **Deploy**: Use [DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)
4. **Expandir**: Veja [ESTRUTURA.md](ESTRUTURA.md) para adicionar features

---

## 📞 Dúvidas?

- Verifique `README.md` para quick start
- Consulte `ESTRUTURA.md` para arquitetura
- Leia `DEPLOY_RAPIDO.md` para deploy

**Boa sorte! 🎯**
