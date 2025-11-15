# 🚀 Guia Rápido: Hospedar na Internet
    Caso queira hospedar na internet ou em algum Host siga os passos abaixo:
## **RESUMO EXECUTIVO**

| Plataforma | Facilidade | Preço | Tempo Setup | Melhor Para |
|-----------|-----------|-------|-----------|-----------|
| **Render** ⭐ | ⭐⭐⭐ | Grátis | 5 min | Produção |
| **Railway** | ⭐⭐⭐ | $5 crédito | 5 min | Aprendizado |
| **PythonAnywhere** | ⭐⭐ | Grátis | 10 min | Python |

---

## **PASSO 1️⃣: Enviar para GitHub (2 minutos)**

```bash
# No seu terminal/PowerShell, na pasta do projeto:

git config --global user.email "seu@email.com"
git config --global user.name "Seu Nome"

git init
git add .
git commit -m "Projeto Mercado de Investimentos"
git branch -M main

# Crie um novo repositório em github.com/new
# Copie a URL (algo como: https://github.com/SEU_USUARIO/mercado-investimentos.git)

git remote add origin https://github.com/SEU_USUARIO/mercado-investimentos.git
git push -u origin main
```

---

## **PASSO 2️⃣: Deploy no Render (3 minutos)**

1. Acesse: **https://render.com**
2. Clique em **"Sign up with GitHub"**
3. Autorize o Render acessar seu GitHub
4. Clique em **"New +" → "Web Service"**
5. Selecione seu repositório `mercado-investimentos`
6. Preencha assim:

   | Campo | Valor |
   |-------|-------|
   | **Name** | `mercado-investimentos` |
   | **Environment** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn -w 1 -b 0.0.0.0:$PORT backend.app:app` |
   | **Plan** | Free |

7. Clique em **"Create Web Service"**
8. Aguarde 2-5 minutos (primeira vez é mais lenta)
9. **Pronto!** 🎉 Seu site está em: `https://mercado-investimentos.onrender.com`

---

## **PASSO 3️⃣: Atualizar o código (automático!)**

```bash
# Sempre que quiser atualizar:
git add .
git commit -m "Melhorias adicionadas"
git push origin main

# O site atualiza automaticamente em ~2 minutos ✨
```

---

## **⚠️ IMPORTANTE**

### ❓ Por que meus dados somem?
- SQLite não persiste no plano free após redeploy
- **Solução**: Upgrade para pago (~$7/mês) ou use PostgreSQL

### ❓ Por que o site fica lento após inatividade?
- Servidor dorme no plano free após 15 min
- **Solução**: Acesse novamente e aguarde 20-30 segundos

### ❓ Preciso pagar para começar?
- **NÃO!** O plano free funciona perfeitamente para testar
- Upgrade só quando quiser mais recursos

---

## **PRÓXIMAS MELHORIAS (Depois de hospedar)**

- [ ] Integrar PostgreSQL para dados persistentes
- [ ] Adicionar autenticação por email/senha
- [ ] Conectar dados reais de dividendos
- [ ] Exportar relatórios em PDF
- [ ] Adicionar gráficos interativos (Chart.js)
- [ ] API para usar via mobile

---

## **SUPORTE**

- 📖 Docs Render: https://docs.render.com/deploy-flask
- 💬 Community: https://render.com/community
- 🐛 Issues do projeto: GitHub Discussions

**Boa sorte! 🚀**
