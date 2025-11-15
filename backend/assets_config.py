"""
Configuração de ativos disponíveis para análise e recomendação.
Inclui ações, FIIs (imóveis) e ETFs de principais bancos e corretoras brasileiras.
"""

# Ações brasileiras - Blue Chips e diversos setores
ACOES_BRASIL = {
    "PETR4.SA": {"nome": "Petrobras PN", "setor": "Energia", "tipo": "ação"},
    "VALE3.SA": {"nome": "Vale ON", "setor": "Mineração", "tipo": "ação"},
    "ITUB4.SA": {"nome": "Itaú Unibanco PN", "setor": "Financeiro", "tipo": "ação"},
    "BBDC4.SA": {"nome": "Bradesco PN", "setor": "Financeiro", "tipo": "ação"},
    "BBAS3.SA": {"nome": "Banco do Brasil ON", "setor": "Financeiro", "tipo": "ação"},
    "SANB11.SA": {"nome": "Santander Brasil UNT", "setor": "Financeiro", "tipo": "ação"},
    "CIEL3.SA": {"nome": "Cielo ON", "setor": "Tecnologia", "tipo": "ação"},
    "MGLU3.SA": {"nome": "Magazine Luiza ON", "setor": "Varejo", "tipo": "ação"},
    "B3SA3.SA": {"nome": "B3 ON", "setor": "Financeiro", "tipo": "ação"},
    "RENT3.SA": {"nome": "Localiza ON", "setor": "Serviços", "tipo": "ação"},
    "EMBR3.SA": {"nome": "Embraer ON", "setor": "Aeronáutica", "tipo": "ação"},
    "WEGE3.SA": {"nome": "WEG ON", "setor": "Industrial", "tipo": "ação"},
    "JBSS3.SA": {"nome": "JBS ON", "setor": "Alimentação", "tipo": "ação"},
    "SUZB3.SA": {"nome": "Suzano ON", "setor": "Celulose", "tipo": "ação"},
    "GOLL4.SA": {"nome": "Gol PN", "setor": "Aviação", "tipo": "ação"},
    "USIM5.SA": {"nome": "Usiminas PNA", "setor": "Siderurgia", "tipo": "ação"},
    "CSNA3.SA": {"nome": "CSN ON", "setor": "Siderurgia", "tipo": "ação"},
    "ECOR3.SA": {"nome": "Ecorodovias ON", "setor": "Infraestrutura", "tipo": "ação"},
    "GGBR4.SA": {"nome": "Gerdau PN", "setor": "Siderurgia", "tipo": "ação"},
    "KLBN11.SA": {"nome": "Klabin UNT", "setor": "Celulose", "tipo": "ação"},
}

# FIIs (Fundos de Investimento Imobiliário) - Imóveis
FIIS_BRASIL = {
    "KNRI11.SA": {"nome": "Kinea Rendimentos Imobiliários", "setor": "Varejo", "tipo": "fii"},
    "MALL11.SA": {"nome": "Malezas", "setor": "Shopping", "tipo": "fii"},
    "BRML11.SA": {"nome": "BR Malls", "setor": "Shopping", "tipo": "fii"},
    "CXSE11.SA": {"nome": "Complexo Executivo", "setor": "Comercial", "tipo": "fii"},
    "HGLG11.SA": {"nome": "Hedge Imóveis", "setor": "Comercial", "tipo": "fii"},
    "XPML11.SA": {"nome": "XP Log", "setor": "Logística", "tipo": "fii"},
    "MXRF11.SA": {"nome": "Maxi Renda Fixa", "setor": "Comercial", "tipo": "fii"},
    "RBRR11.SA": {"nome": "RBR Realty", "setor": "Residencial", "tipo": "fii"},
    "VILG11.SA": {"nome": "Village Offices", "setor": "Comercial", "tipo": "fii"},
    "PATB11.SA": {"nome": "Pátria Logística", "setor": "Logística", "tipo": "fii"},
    "SAGG11.SA": {"nome": "Sagen Desenvolvimento", "setor": "Logística", "tipo": "fii"},
    "BBPO11.SA": {"nome": "BB Progressivo", "setor": "Logística", "tipo": "fii"},
    "IRDM11.SA": {"nome": "Iridium Logística", "setor": "Logística", "tipo": "fii"},
    "CPFF11.SA": {"nome": "C&P Logística", "setor": "Logística", "tipo": "fii"},
    "HAGG11.SA": {"nome": "Hagg Logística", "setor": "Logística", "tipo": "fii"},
}

# Ações internacionais (EUA) - Blue chips globais
ACOES_USA = {
    "AAPL": {"nome": "Apple Inc", "setor": "Tecnologia", "tipo": "ação"},
    "MSFT": {"nome": "Microsoft Corporation", "setor": "Tecnologia", "tipo": "ação"},
    "GOOGL": {"nome": "Alphabet Inc (Google)", "setor": "Tecnologia", "tipo": "ação"},
    "AMZN": {"nome": "Amazon.com Inc", "setor": "Varejo/Tech", "tipo": "ação"},
    "TSLA": {"nome": "Tesla Inc", "setor": "Automotivo", "tipo": "ação"},
    "META": {"nome": "Meta Platforms", "setor": "Tecnologia", "tipo": "ação"},
    "NVDA": {"nome": "NVIDIA Corporation", "setor": "Tecnologia", "tipo": "ação"},
    "JPM": {"nome": "JPMorgan Chase", "setor": "Financeiro", "tipo": "ação"},
    "V": {"nome": "Visa Inc", "setor": "Financeiro", "tipo": "ação"},
    "MA": {"nome": "Mastercard Inc", "setor": "Financeiro", "tipo": "ação"},
    "PG": {"nome": "Procter & Gamble", "setor": "Consumo", "tipo": "ação"},
    "KO": {"nome": "The Coca-Cola Company", "setor": "Consumo", "tipo": "ação"},
    "JNJ": {"nome": "Johnson & Johnson", "setor": "Saúde", "tipo": "ação"},
    "MCD": {"nome": "McDonald's", "setor": "Varejo/Alimentação", "tipo": "ação"},
    "WMT": {"nome": "Walmart Inc", "setor": "Varejo", "tipo": "ação"},
    "XOM": {"nome": "Exxon Mobil", "setor": "Energia", "tipo": "ação"},
    "CVX": {"nome": "Chevron Corporation", "setor": "Energia", "tipo": "ação"},
    "BA": {"nome": "Boeing Company", "setor": "Aeronáutica", "tipo": "ação"},
    "CAT": {"nome": "Caterpillar Inc", "setor": "Industrial", "tipo": "ação"},
    "IBM": {"nome": "IBM", "setor": "Tecnologia", "tipo": "ação"},
}

# ETFs e REITs internacionais (EUA) - Imóveis e Diversificação
ETFS_USA = {
    "VTI": {"nome": "Vanguard Total Market ETF", "setor": "Diversificado", "tipo": "etf"},
    "VOO": {"nome": "Vanguard S&P 500 ETF", "setor": "Diversificado", "tipo": "etf"},
    "VEA": {"nome": "Vanguard FTSE Developed Markets", "setor": "Diversificado", "tipo": "etf"},
    "VWO": {"nome": "Vanguard FTSE Emerging Markets", "setor": "Emergente", "tipo": "etf"},
    "BND": {"nome": "Vanguard Total Bond Market", "setor": "Renda Fixa", "tipo": "etf"},
    "VGLT": {"nome": "Vanguard Long-Term Treasury", "setor": "Renda Fixa", "tipo": "etf"},
    "VNQ": {"nome": "Vanguard Real Estate ETF", "setor": "Imóvel", "tipo": "etf"},
    "SCHH": {"nome": "Schwab US REIT ETF", "setor": "Imóvel", "tipo": "etf"},
    "XLRE": {"nome": "Real Estate Select Sector SPDR", "setor": "Imóvel", "tipo": "etf"},
    "IYR": {"nome": "iShares US Real Estate ETF", "setor": "Imóvel", "tipo": "etf"},
    "QQQ": {"nome": "Invesco QQQ Trust (Nasdaq-100)", "setor": "Tecnologia", "tipo": "etf"},
    "XLK": {"nome": "Technology Select Sector SPDR", "setor": "Tecnologia", "tipo": "etf"},
    "XLF": {"nome": "Financial Select Sector SPDR", "setor": "Financeiro", "tipo": "etf"},
    "XLE": {"nome": "Energy Select Sector SPDR", "setor": "Energia", "tipo": "etf"},
    "XLV": {"nome": "Health Care Select Sector SPDR", "setor": "Saúde", "tipo": "etf"},
}

# Ações brasileiras - Bancos digitais e fintechs
FINTECHS_BRASIL = {
    "NUBANK": {"nome": "Nubank (quando IPO)", "setor": "Fintech", "tipo": "ação"},
    "INTER3.SA": {"nome": "Banco Inter ON", "setor": "Fintech", "tipo": "ação"},
}

# Todos os ativos disponíveis
TODOS_ATIVOS = {
    **ACOES_BRASIL,
    **FIIS_BRASIL,
    **ACOES_USA,
    **ETFS_USA,
    **FINTECHS_BRASIL,
}

# Agrupamentos por categoria
CATEGORIAS = {
    "Ações Brasil": ACOES_BRASIL,
    "Imóveis (FIIs)": FIIS_BRASIL,
    "Ações EUA": ACOES_USA,
    "ETFs e REITs EUA": ETFS_USA,
    "Fintechs": FINTECHS_BRASIL,
}

# Mapeamento de tickers para nomes amigáveis
NOMES_ATIVOS = {k: v["nome"] for k, v in TODOS_ATIVOS.items()}

# Função auxiliar para validar tickers
def validar_ticker(ticker: str) -> bool:
    """Verifica se o ticker está na lista de ativos disponíveis."""
    return ticker.upper() in TODOS_ATIVOS

def obter_nome_ativo(ticker: str) -> str:
    """Obtém o nome amigável do ativo."""
    ticker = ticker.upper()
    return NOMES_ATIVOS.get(ticker, ticker)

def obter_categoria_ativo(ticker: str) -> str:
    """Obtém a categoria do ativo."""
    ticker = ticker.upper()
    for categoria, ativos in CATEGORIAS.items():
        if ticker in ativos:
            return categoria
    return "Desconhecido"

def listar_ativos_por_categoria(categoria: str) -> dict:
    """Lista todos os ativos de uma categoria."""
    return CATEGORIAS.get(categoria, {})

def listar_todas_categorias() -> list:
    """Lista todas as categorias disponíveis."""
    return list(CATEGORIAS.keys())
