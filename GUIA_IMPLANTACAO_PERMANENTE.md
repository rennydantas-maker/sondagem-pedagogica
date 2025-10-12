# 🚀 Guia de Implantação Permanente na Nuvem

Este guia mostra como colocar o **Sistema de Sondagem Pedagógica** permanentemente na internet, **sem precisar de nenhum computador ligado**.

---

## 📋 Pré-requisitos

Você vai precisar de:
1. Uma conta no **GitHub** (gratuita) - para hospedar o código
2. Uma conta no **Render.com** (gratuita) - para hospedar o site

**Tempo estimado:** 15-20 minutos

---

## 🎯 Opção 1: Render.com (RECOMENDADO - 100% Gratuito)

### Passo 1: Criar Conta no GitHub

1. Acesse: https://github.com/signup
2. Crie sua conta gratuita
3. Confirme seu e-mail

### Passo 2: Criar um Repositório no GitHub

1. Após fazer login, clique no botão **"+"** no canto superior direito
2. Selecione **"New repository"**
3. Preencha:
   - **Repository name:** `sondagem-pedagogica`
   - **Description:** "Sistema de Sondagem Pedagógica com IA"
   - Deixe como **Public**
   - **NÃO** marque "Initialize this repository with a README"
4. Clique em **"Create repository"**

### Passo 3: Fazer Upload do Projeto para o GitHub

**No seu computador:**

1. Baixe e descompacte o arquivo `sondagem-pedagogica-completo.zip`
2. Abra o Terminal/Prompt de Comando
3. Navegue até a pasta:
   ```bash
   cd caminho/para/sondagem-app
   ```

4. Execute os seguintes comandos (substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub):

   ```bash
   git init
   git add .
   git commit -m "Sistema de Sondagem Pedagógica"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/sondagem-pedagogica.git
   git push -u origin main
   ```

5. Quando pedir usuário e senha:
   - **Usuário:** seu nome de usuário do GitHub
   - **Senha:** você precisará criar um **Personal Access Token** (veja abaixo)

**Como criar um Personal Access Token:**
1. No GitHub, vá em: Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Clique em "Generate new token (classic)"
3. Dê um nome (ex: "Deploy Sondagem")
4. Marque a opção **"repo"**
5. Clique em "Generate token"
6. **COPIE O TOKEN** (você não verá ele novamente!)
7. Use esse token como senha ao fazer o `git push`

### Passo 4: Criar Conta no Render.com

1. Acesse: https://render.com
2. Clique em **"Get Started"**
3. Escolha **"Sign up with GitHub"**
4. Autorize o Render a acessar sua conta do GitHub

### Passo 5: Criar o Web Service no Render

1. No painel do Render, clique em **"New +"** → **"Web Service"**
2. Clique em **"Connect a repository"**
3. Encontre e selecione o repositório **`sondagem-pedagogica`**
4. Preencha as configurações:

   **Configurações Básicas:**
   - **Name:** `sondagem-pedagogica` (ou qualquer nome que quiser)
   - **Region:** Escolha a região mais próxima (ex: Oregon para Brasil)
   - **Branch:** `main`
   - **Root Directory:** deixe em branco
   - **Runtime:** `Python 3`

   **Comandos de Build e Start:**
   - **Build Command:** 
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     gunicorn --config gunicorn_config.py app:app
     ```

   **Configurações Avançadas:**
   - **Instance Type:** Selecione **"Free"**

5. Clique em **"Create Web Service"**

### Passo 6: Configurar Variáveis de Ambiente

1. Após criar o serviço, vá na aba **"Environment"**
2. Clique em **"Add Environment Variable"**
3. Adicione:
   - **Key:** `OPENAI_API_KEY`
   - **Value:** (a chave da OpenAI já está configurada no ambiente Manus, mas você precisará de uma própria)

**Como obter sua chave OpenAI:**
- Acesse: https://platform.openai.com/api-keys
- Crie uma conta (tem crédito gratuito para começar)
- Gere uma nova chave API
- Cole no campo "Value"

4. Clique em **"Save Changes"**

### Passo 7: Aguardar o Deploy

O Render vai automaticamente:
1. Baixar seu código do GitHub
2. Instalar as dependências
3. Iniciar o servidor
4. Gerar uma URL permanente

**Isso leva cerca de 3-5 minutos.**

Quando terminar, você verá:
- ✅ Status: **"Live"** (verde)
- 🌐 URL do seu site: **`https://sondagem-pedagogica.onrender.com`** (ou similar)

### Passo 8: Acessar Seu Site!

Clique na URL gerada e pronto! Seu sistema está **permanentemente** na internet! 🎉

---

## 🔄 Como Atualizar o Site Depois

Se você fizer alterações no código:

1. Faça as mudanças nos arquivos locais
2. No terminal:
   ```bash
   git add .
   git commit -m "Descrição da mudança"
   git push
   ```
3. O Render detectará automaticamente e fará o deploy da nova versão!

---

## ⚠️ Limitações do Plano Gratuito do Render

- ✅ **Hospedagem permanente** (24/7)
- ✅ **Sem limite de tempo**
- ⚠️ O site "dorme" após **15 minutos de inatividade**
- ⚠️ Ao acessar um site "dormindo", leva ~30 segundos para acordar
- ⚠️ Limite de **750 horas/mês** (suficiente para uso escolar)

**Solução:** Se quiser que nunca durma, você pode:
- Fazer upgrade para o plano pago ($7/mês)
- Usar um serviço de "ping" gratuito como o UptimeRobot para manter o site acordado

---

## 🎯 Opção 2: Railway.app (Alternativa Gratuita)

Se preferir usar o Railway:

1. Acesse: https://railway.app
2. Faça login com GitHub
3. Clique em **"New Project"** → **"Deploy from GitHub repo"**
4. Selecione o repositório `sondagem-pedagogica`
5. O Railway detectará automaticamente que é um projeto Python
6. Adicione a variável de ambiente `OPENAI_API_KEY`
7. Pronto! Você terá uma URL tipo: `https://sondagem-pedagogica.up.railway.app`

**Vantagem:** Não "dorme"  
**Limitação:** $5 de crédito gratuito por mês (suficiente para uso moderado)

---

## 🎯 Opção 3: PythonAnywhere (Específico para Python)

1. Acesse: https://www.pythonanywhere.com
2. Crie uma conta gratuita
3. Vá em **"Web"** → **"Add a new web app"**
4. Escolha **"Manual configuration"** → **"Python 3.10"**
5. No **"Code"** → **"Source code"**, faça upload dos arquivos
6. Configure o **WSGI configuration file** para apontar para `app.py`
7. Recarregue o web app

**URL:** `https://seuusuario.pythonanywhere.com`

---

## 📊 Comparação das Opções

| Plataforma | Gratuito? | Dorme? | Limite | Facilidade |
|------------|-----------|--------|--------|------------|
| **Render.com** | ✅ Sim | ⚠️ Após 15min | 750h/mês | ⭐⭐⭐⭐⭐ |
| **Railway.app** | ⚠️ $5/mês | ❌ Não | Crédito mensal | ⭐⭐⭐⭐ |
| **PythonAnywhere** | ✅ Sim | ❌ Não | Tráfego limitado | ⭐⭐⭐ |
| **Heroku** | ❌ Não | - | Pago ($7/mês) | ⭐⭐⭐⭐⭐ |

---

## 🆘 Solução de Problemas

### "Build failed" no Render

**Causa:** Erro ao instalar dependências  
**Solução:** Verifique se o arquivo `requirements.txt` está correto

### "Application Error" ao acessar o site

**Causa:** Erro no código ou variável de ambiente faltando  
**Solução:** 
1. Vá em "Logs" no painel do Render
2. Veja qual é o erro específico
3. Adicione a variável `OPENAI_API_KEY` se ainda não adicionou

### Site muito lento

**Causa:** Servidor gratuito "dormiu"  
**Solução:** Normal no plano gratuito. Aguarde 30s que ele acorda.

---

## 🎓 Dicas Finais

1. **Salve a URL do seu site** em algum lugar seguro
2. **Compartilhe com cuidado:** Lembre-se que é um site público
3. **Monitore o uso:** Verifique os logs no painel do Render
4. **Faça backup:** Mantenha uma cópia local dos arquivos

---

## 📞 Precisa de Ajuda?

Se tiver dificuldades:
1. Consulte a documentação do Render: https://render.com/docs
2. Veja tutoriais no YouTube: "Deploy Flask Render"
3. Entre em contato com o suporte do Render (muito responsivo!)

---

**Parabéns! Seu sistema está pronto para uso profissional! 🎉**

