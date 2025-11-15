# 📁 Estrutura do Projeto - Mercado de Investimentos

```
Mercado_de_investimentos/
│
├── 📄 README.md                    # Documentação principal
├── 📄 README_DEPLOY.md             # Guia de deployment
├── 📄 DEPLOY_RAPIDO.md             # Guia rápido de deployment
├── 📄 requirements.txt             # Dependências Python
├── 📄 Procfile                     # Configuração Render/Heroku
├── 📄 render.yaml                  # Config específica Render
├── 📄 .gitignore                   # Arquivos ignorados Git
├── 📄 run.py                       # 🚀 ARQUIVO PRINCIPAL - EXECUTAR ISTO
│
├── 📂 src/                         # Código-fonte da aplicação
│   ├── __init__.py
│   ├── 📂 app/                     # Interface Flask
│   │   ├── __init__.py
│   │   ├── 📂 routes/              # Rotas da API
│   │   │   └── __init__.py
│   │   ├── 📂 templates/           # Templates HTML
│   │   │   ├── base.html           # Layout base
│   │   │   ├── index.html          # Página inicial
│   │   │   ├── recommendations.html # Recomendações
│   │   │   └── report.html         # Relatório mensal
│   │   └── 📂 static/              # Arquivos estáticos
│   │       ├── 📂 css/
│   │       │   └── styles.css      # Estilos da UI
│   │       └── 📂 js/
│   │
│   └── 📂 core/                    # Lógica de negócio
│       ├── __init__.py
│       ├── 📂 database/            # Camada de BD
│       │   ├── __init__.py
│       │   └── db.py               # SQLite conexão e schema
│       └── 📂 analysis/            # Motor de análise
│           ├── __init__.py
│           ├── indicators.py       # Cálculos de risco
│           ├── data_sources.py     # Coleta de dados
│           ├── scoring.py          # Engine de pontuação
│           └── report.py           # Geração de relatórios
│
├── 📂 data/                        # Dados da aplicação
│   ├── sample_tickers.csv          # Tickers de amostra
│   ├── sample_prices.csv           # Preços históricos
│   └── market.sqlite               # ⚙️ BD SQLite (gerado)
│
├── 📂 docs/                        # Documentação técnica
│   └── (Adicionar docs futuras)
│
├── 📂 scripts/                     # Scripts auxiliares
│   └── (Scripts de setup/maintenance)
│
├── 📂 config/                      # Configurações
│   └── (Variáveis de ambiente)
│
└── 📂 tests/                       # Testes unitários
    └── (Testes futuros)
```

## 🎯 Arquivo Principal

**Para rodar o projeto localmente:**
```bash
python run.py
```
Então acesse: `http://127.0.0.1:5000`

## 📦 Estrutura Lógica

### `src/app/` - Interface do Usuário
- **Templates Jinja2** + **HTML/CSS responsivo**
- Formulários para análise
- Visualização de recomendações
- Geração de relatórios

### `src/core/database/` - Persistência
- **SQLite** com schema otimizado
- Tabelas: `assets`, `prices`, `econ_indicators`, `recommendations`, `reports`
- Gerenciamento de conexões

### `src/core/analysis/` - Motor de Análise
- **indicators.py**: Cálculos de volatilidade, drawdown, dividend yield
- **data_sources.py**: Integração yfinance + fallback CSV offline
- **scoring.py**: Algoritmo de pontuação por risco
- **report.py**: Geração HTML de relatórios mensais

## 🔄 Fluxo de Dados

```
Entrada de Tickers
        ↓
[data_sources.py] → Busca preços (online ou CSV)
        ↓
[database/db.py] → Armazena em SQLite
        ↓
[indicators.py] → Calcula vol, drawdown, dividend
        ↓
[scoring.py] → Cria ranking por score
        ↓
[Flask Routes] → Exibe em templates
        ↓
[report.py] → Gera relatório mensal HTML
```

## 🚀 Como Expandir

### Adicionar nova página:
1. Criar template em `src/app/templates/`
2. Adicionar rota em `src/app/routes/`
3. Importar em `run.py`

### Adicionar novo indicador:
1. Criar função em `src/core/analysis/indicators.py`
2. Importar em `scoring.py`
3. Usar no cálculo de score

### Conectar nova fonte de dados:
1. Adicionar função em `data_sources.py`
2. Atualizar `ensure_seed_data()` 
3. Testar com dados de amostra

---

**Data**: 14 de novembro de 2025  
**Versão**: 1.0  
**Status**: ✅ Pronto para produção
