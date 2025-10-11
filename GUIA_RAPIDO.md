# 🚀 Guia Rápido - Sistema de Sondagem Pedagógica

## Para Começar a Usar AGORA (Modo de Teste)

### 1️⃣ Abra o Terminal/Prompt de Comando

**Windows:** Pressione `Win + R`, digite `cmd` e pressione Enter  
**Mac/Linux:** Abra o Terminal

### 2️⃣ Navegue até a pasta do projeto

```bash
cd caminho/para/sondagem-app
```

### 3️⃣ Instale as dependências (apenas na primeira vez)

```bash
pip3 install Flask openai Pillow
```

### 4️⃣ Execute o servidor de teste

```bash
python3 app_test.py
```

### 5️⃣ Abra o navegador

Acesse: **http://localhost:5000**

---

## 📝 Como Usar o Sistema

### Passo a Passo:

1. **Preencha os dados do aluno:**
   - Nome completo
   - Série/Ano (ex: 1º Ano B)
   - Data de nascimento (opcional)
   - Seu nome (professor/a)

2. **Digite as palavras ditadas:**
   - Recomendação: Use palavras de diferentes tamanhos
   - Exemplo: `PÉ, BOLA, CAVALO, FORMIGA`
   - Separe por vírgula ou quebra de linha

3. **Envie a foto da escrita:**
   - Clique em "Enviar Foto da Escrita"
   - Selecione a imagem do celular ou computador
   - Certifique-se de que a escrita está legível

4. **Analise com IA:**
   - Clique no botão "Analisar com Inteligência Artificial"
   - Aguarde alguns segundos
   - A IA vai ler a escrita e classificar a hipótese

5. **Revise os resultados:**
   - A transcrição e a hipótese aparecerão automaticamente
   - Você pode editar se necessário
   - Adicione observações adicionais

6. **Gere o relatório:**
   - Clique em "Gerar Relatório Final"
   - O relatório aparecerá na tela
   - Use `Ctrl+P` (ou `Cmd+P` no Mac) para imprimir

---

## ⚠️ Modo de Teste vs. Modo de Produção

### 🧪 Modo de Teste (app_test.py)
- ✅ Funciona imediatamente, sem configuração
- ✅ IA de análise ATIVA
- ⚠️ OCR simulado (não lê imagens de verdade)
- 👍 Ideal para: Demonstrações, testes, aprender a usar

### 🚀 Modo de Produção (app.py)
- ✅ IA de análise ATIVA
- ✅ OCR REAL (lê caligrafia infantil)
- ⚠️ Requer configuração do Google Cloud
- 👍 Ideal para: Uso real em sala de aula

---

## 🔧 Para Ativar o OCR Real

### O que você precisa:

1. **Conta no Google Cloud** (gratuita para começar)
2. **Ativar a API Cloud Vision**
3. **Criar credenciais de serviço**
4. **Baixar o arquivo JSON de credenciais**

### Passo a passo detalhado:

#### 1. Criar conta no Google Cloud

Acesse: https://console.cloud.google.com/

#### 2. Criar um novo projeto

- Clique em "Selecionar projeto" no topo
- Clique em "Novo projeto"
- Dê um nome (ex: "Sondagem Pedagogica")
- Clique em "Criar"

#### 3. Ativar a Cloud Vision API

- No menu lateral, vá em "APIs e Serviços" → "Biblioteca"
- Pesquise por "Cloud Vision API"
- Clique nela e depois em "Ativar"

#### 4. Criar credenciais

- Vá em "APIs e Serviços" → "Credenciais"
- Clique em "Criar credenciais" → "Conta de serviço"
- Dê um nome (ex: "sondagem-ocr")
- Clique em "Criar e continuar"
- Em "Papel", selecione "Proprietário"
- Clique em "Concluir"

#### 5. Baixar o arquivo JSON

- Na lista de contas de serviço, clique na que você criou
- Vá na aba "Chaves"
- Clique em "Adicionar chave" → "Criar nova chave"
- Escolha "JSON"
- O arquivo será baixado automaticamente

#### 6. Configurar o arquivo

**No Windows:**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\caminho\para\credenciais.json
```

**No Mac/Linux:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/credenciais.json"
```

#### 7. Executar o servidor de produção

```bash
python3 app.py
```

Pronto! Agora o OCR vai ler as imagens de verdade! 🎉

---

## 💡 Dicas de Uso

### Para Melhores Resultados:

1. **Fotos de qualidade:**
   - Boa iluminação
   - Foco nítido
   - Escrita centralizada
   - Fundo claro e limpo

2. **Palavras adequadas:**
   - Use o campo semântico (frutas, animais, etc.)
   - Varie o tamanho (mono, di, tri, polissílaba)
   - Evite palavras muito complexas

3. **Análise crítica:**
   - A IA é uma ferramenta de apoio
   - Você, professor/a, tem a palavra final
   - Revise sempre os resultados
   - Adicione suas observações

### Atalhos Úteis:

- `Ctrl+P` / `Cmd+P` → Imprimir relatório
- `F5` → Recarregar página (para nova sondagem)
- `Ctrl+Shift+I` → Abrir ferramentas de desenvolvedor (para debug)

---

## ❓ Solução de Problemas

### "Erro ao conectar com o servidor"
- Verifique se o servidor está rodando
- Veja se não há erro no terminal
- Tente reiniciar o servidor

### "Erro ao processar a imagem"
- Verifique o tamanho da imagem (máx 10MB)
- Tente outro formato (JPG, PNG)
- Certifique-se de que a imagem não está corrompida

### "A IA não está classificando corretamente"
- Lembre-se: é uma sugestão, não uma verdade absoluta
- Revise e ajuste manualmente
- A IA aprende com padrões gerais, mas cada criança é única

### "O servidor não inicia"
- Verifique se instalou as dependências: `pip3 install -r requirements.txt`
- Veja se a porta 5000 não está em uso
- Tente usar outra porta: `PORT=8080 python3 app_test.py`

---

## 📚 Recursos Adicionais

### Para Entender Melhor as Hipóteses de Escrita:

- [Nova Escola - Sondagem](https://novaescola.org.br/)
- Livro: "Psicogênese da Língua Escrita" - Emilia Ferreiro
- Vídeos no YouTube: Pesquise "hipóteses de escrita"

### Para Aprender Mais Sobre as Tecnologias:

- **Python:** https://www.python.org/
- **Flask:** https://flask.palletsprojects.com/
- **Google Cloud Vision:** https://cloud.google.com/vision
- **OpenAI:** https://platform.openai.com/

---

## 🎓 Boas Práticas Pedagógicas

1. **Faça sondagens regulares:**
   - Início do ano (diagnóstica)
   - Meio do ano (formativa)
   - Final do ano (somativa)

2. **Use os resultados para:**
   - Formar grupos de trabalho
   - Planejar intervenções
   - Comunicar com as famílias
   - Documentar o progresso

3. **Lembre-se:**
   - A sondagem não é prova
   - Não há certo ou errado
   - É um diagnóstico do momento
   - Cada criança tem seu tempo

---

**Dúvidas?** Consulte o arquivo `README.md` para informações técnicas detalhadas.

**Boa sondagem! 🎉📚**

