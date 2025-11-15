# 📈 Mercado de Investimentos

Sistema inteligente para **análise de risco** em investimentos de ações e imobiliários, com foco em mercados globais.

## ✨ Principais Funcionalidades

- 🎯 **Análise de Risco**: Volatilidade, drawdown máximo, dividend yield
- 💡 **Recomendações Inteligentes**: Score baseado em menor risco e melhor retorno  
- 📊 **Relatórios Mensais**: Lucros, dividendos e análise de perdas
- 🌍 **Dados Globais**: Suporta ações dos EUA, Brasil e outros mercados
- 💾 **Funciona Offline**: Banco de dados local SQLite com dados de amostra
- 🎨 **Interface Moderna**: UI responsiva com dark theme

---

## 🚀 Quick Start

### 1. Clone e navegue ao diretório
```bash
cd Mercado_de_investimentos
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o aplicativo
```bash
python run.py
```

### 4. Acesse no navegador
```
http://127.0.0.1:5000
```

---

## 📁 Estrutura do Projeto

```
├── src/
│   ├── app/              # Interface Flask (templates, CSS)
│   └── core/             # Lógica (análise, BD, fontes de dados)
├── data/                 # Banco SQLite + arquivos CSV
├── run.py                # 🎯 Arquivo principal
├── requirements.txt      # Dependências
└── README.md            # Este arquivo
```

**Veja `ESTRUTURA.md` para detalhes completos.**

---

## 📚 Documentação

- **[ESTRUTURA.md](ESTRUTURA.md)** - Arquitetura do projeto e como expandir
- **[DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md)** - Deploy em 5 minutos (Render)
- **[README_DEPLOY.md](README_DEPLOY.md)** - Guia completo de deployment

---

## 🎓 Como Usar

### Página Inicial
1. Informe tickers (ex: SPY, AAPL, PETR4.SA)
2. Clique em "Analisar e Recomendar"

### Recomendações
- Visualize os ativos rankados por score
- Menores riscos aparecem primeiro
- Veja volatilidade, drawdown e dividend yield

### Relatório Mensal
- Selecione um mês
- Veja lucros/perdas da carteira sugerida
- Análise de dividendos e drawdowns

---

## 🛠️ Tecnologias

| Stack | Detalhes |
|-------|----------|
| **Backend** | Python 3.10+, Flask |
| **Frontend** | HTML5, CSS3 (Dark Theme) |
| **BD** | SQLite |
| **Dados** | yfinance + CSV offline |
| **Deploy** | Render, Railway, PythonAnywhere |

---

## 💻 Exemplos de Tickers

### EUA
- SPY, QQQ, VTI, AAPL, MSFT, AMZN

### Brasil
- PETR4.SA, VALE3.SA, WEGE3.SA

### FIIs (Imobiliários)
- KNRI11.SA, XPML11.SA, RBRR11.SA

---

## 🌐 Deploy Gratuito

Hospede na internet em 5 minutos com **Render**:

1. Envie para GitHub
2. Acesse [render.com](https://render.com)
3. Conecte seu repositório
4. Deploy automático! 

**Veja [DEPLOY_RAPIDO.md](DEPLOY_RAPIDO.md) para instruções.**

---

## 🔮 Próximas Melhorias

- [ ] PostgreSQL para dados persistentes
- [ ] Autenticação de usuários
- [ ] Integração com APIs de corretoras
- [ ] Exportação de relatórios em PDF
- [ ] Gráficos interativos (Chart.js)
- [ ] Notificações por email

---

## 👤 Autor

Desenvolvido por Hiago como projeto educacional em análise financeira.

**Última atualização**: 14 de novembro de 2025