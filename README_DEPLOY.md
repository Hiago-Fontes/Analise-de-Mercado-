# Como hospedar na Internet (Gratuito)

## Opção 1: Render (RECOMENDADO) ⭐

### Pré-requisitos:
- Conta GitHub com o projeto enviado
- Conta Render (gratuita)

### Passo a passo:

1. **Envie o projeto para GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/SEU_USUARIO/mercado-investimentos.git
   git branch -M main
   git push -u origin main
   ```

2. **Crie conta no Render:**
   - Acesse https://render.com
   - Clique em "Sign up"
   - Conecte com GitHub

3. **Deploy na Render:**
   - Clique em "New +" → "Web Service"
   - Selecione seu repositório
   - Preencha assim:
     - **Name**: `mercado-investimentos`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn -w 1 -b 0.0.0.0:$PORT backend.app:app`
   - Clique em "Create Web Service"
   - Aguarde 2-3 minutos (primeira vez é mais lenta)

4. **Pronto!**
   - Seu site estará em: `https://mercado-investimentos.onrender.com` (ou similar)
   - Cada vez que você fizer push no GitHub, o site atualiza automaticamente

---

## Opção 2: Railway

1. Acesse https://railway.app
2. Clique em "Start Project"
3. Selecione "Deploy from GitHub"
4. Conecte seu repositório
5. Railway detecta automaticamente que é Python/Flask
6. Clique em "Deploy"
7. Seu site estará disponível em dias!

---

## Opção 3: PythonAnywhere

1. Acesse https://www.pythonanywhere.com
2. Sign up (gratuito)
3. Vá para "Web" → "Add a new web app"
4. Escolha "Manual configuration" + "Python 3.10"
5. Configure o `WSGI` apontando para seu `backend.app:app`
6. Suba os arquivos via Git ou upload
7. Pronto!

---

## ⚠️ Notas importantes:

### Plano Free vs Pago:

**Render (Free):**
- ✅ Hospedagem gratuita
- ✅ Suporta bancos SQLite
- ✅ Deploy automático do GitHub
- ❌ Servidor dorme após 15 min de inatividade
- ❌ Limite de 0.5 vCPU

**Solução:** Se quiser sempre ativo, upgrade para plano pago (~$7/mês)

### Dados persistentes:

Como estamos usando SQLite (arquivo local), **os dados NÃO são persistentes** no plano free após redeploy. 

**Soluções:**
1. **Upgrade para plano pago** (dados persistem no volume)
2. **Migrar para PostgreSQL** (Railway/Render oferecem planos grátis)

### Como atualizar o código:

```bash
# Localmente:
git add .
git commit -m "Minhas alterações"
git push origin main

# O site atualiza automaticamente em 2 minutos!
```

---

## Próximos passos sugeridos:

1. ✅ Usar PostgreSQL em vez de SQLite para dados persistentes
2. ✅ Adicionar autenticação de usuários
3. ✅ Conectar dados reais de dividendos (Stooq, CoinGecko)
4. ✅ Exportar relatórios em PDF
5. ✅ Melhorar análise com mais indicadores técnicos

