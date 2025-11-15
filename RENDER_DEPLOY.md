# Instruções para Deploy e Redeploy no Render

## Problema Resolvido
O CSS não estava sendo servido e as rotas não funcionavam porque:
1. Flask não estava configurado com os caminhos corretos de `static` e `templates`
2. `run.py` não estava sincronizado com `backend/app.py`
3. Gunicorn não estava configurado para servir arquivos estáticos

## Correções Implementadas

### 1. Configuração Flask
- Criado `backend/app.py` com Flask corretamente configurado:
  ```python
  BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
  TEMPLATE_DIR = os.path.join(BACKEND_DIR, 'templates')
  STATIC_DIR = os.path.join(BACKEND_DIR, 'static')
  
  app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR, static_url_path='/static')
  ```

### 2. Sincronização do run.py
- `run.py` agora importa o app do `backend/app.py`
- Isso garante que o Render possa usar `gunicorn ... run:app`

### 3. Configuração Gunicorn
- Criado `gunicorn_config.py` com configurações otimizadas
- Atualizado `Procfile` para usar a configuração

### 4. Arquivos de Configuração
- `Procfile`: Define como executar no Heroku/Render
- `render.yaml`: Configuração específica do Render
- `.env.example`: Exemplo de variáveis de ambiente necessárias

## Como Fazer Redeploy no Render

### Opção 1: Auto-deploy (Recomendado)
1. Faça push para GitHub: `git push origin main`
2. O Render detectará a mudança e fará rebuild automaticamente
3. Aguarde 2-5 minutos para a implantação completar

### Opção 2: Manual via Dashboard Render
1. Acesse https://dashboard.render.com
2. Encontre o serviço "mercado-investimentos"
3. Clique em "Manual Deploy" → "Deploy Latest Commit"

### Opção 3: Trigger via Webhook
1. No Render dashboard, copie o Deploy Hook URL
2. Execute: 
   ```bash
   curl -X POST <DEPLOY_HOOK_URL>
   ```

## Verificar Deploy

Após o deploy:
1. Acesse https://analise-mercado.onrender.com
2. Verifique se o CSS está carregando (azul/escuro)
3. Teste selecionando ativos:
   - Clique em categoria
   - Selecione ativos
   - Clique "Analisar e Recomendar"
4. Verifique se aparecem os gráficos de análise

## Possíveis Problemas

### CSS Still Not Loading
- Limpe cache: Ctrl+Shift+Del (ou Cmd+Shift+Delete no Mac)
- Acesse em modo anônimo/privado
- Verifique no DevTools (F12) se há erro 404 em `/static/css/styles.css`

### Rotas Não Funcionam
- Verifique logs no Render dashboard
- Procure por erros Python na seção "Logs"
- Se houver erro de módulo, verifique `requirements.txt`

### Database Vazio
- No Render (free tier), o SQLite pode ser resetado
- Isso faz parte do comportamento do free tier
- Dados serão recuperados ao analisar ativos (via yfinance)

## Logs do Render

Para ver logs em tempo real:
1. Dashboard Render → Seu serviço → "Logs"
2. Filtrar por erros: procure por "ERROR" ou "Traceback"

## Próximas Melhorias

- [ ] Migrar para PostgreSQL para dados persistentes
- [ ] CDN para servir CSS (CloudFlare)
- [ ] Plano pago Render para melhor performance
- [ ] Cache de dados entre requests

## Contato/Suporte

Se o problema persistir:
1. Verifique se todos os arquivos estão em GitHub
2. Execute `git status` para ver mudanças não commitadas
3. Verifique `requirements.txt` tem todas as dependências
