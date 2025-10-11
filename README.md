# 🎓 Sistema de Sondagem Pedagógica com Inteligência Artificial

## Descrição

Sistema web completo para auxiliar professores na realização e análise de sondagens de escrita para crianças do 1º ano do Ensino Fundamental. Utiliza **Reconhecimento Óptico de Caracteres (OCR)** e **Inteligência Artificial** para automatizar a classificação das hipóteses de escrita segundo a psicogênese da língua escrita (Emilia Ferreiro e Ana Teberosky).

## 🌟 Funcionalidades

### Para o Professor:
- ✅ Interface intuitiva para registro de dados do aluno
- ✅ Upload de fotos da escrita da criança
- ✅ Análise automática com IA
- ✅ Classificação nas 5 hipóteses de escrita:
  - Pré-Silábico
  - Silábico sem valor sonoro
  - Silábico com valor sonoro
  - Silábico-Alfabético
  - Alfabético
- ✅ Justificativas pedagógicas automáticas
- ✅ Campos editáveis (o professor sempre tem a palavra final)
- ✅ Geração de relatórios profissionais prontos para impressão
- ✅ Registro de observações adicionais

### Tecnologias Utilizadas:
- **Back-end:** Python 3.11 + Flask
- **Front-end:** HTML5, CSS3, JavaScript (Vanilla)
- **OCR:** Google Cloud Vision API
- **IA:** OpenAI GPT-4.1-mini (instruído com conhecimento pedagógico)
- **Design:** Gradientes modernos, animações suaves, responsivo

## 📁 Estrutura do Projeto

```
/sondagem-app
├── app.py                  # Servidor principal (requer Google Cloud)
├── app_test.py             # Servidor de teste (OCR simulado)
├── ai_analyzer.py          # Módulo de análise com IA
├── requirements.txt        # Dependências Python
├── README.md               # Esta documentação
├── /templates
│   └── sondagem.html       # Interface do usuário
└── server.log              # Log do servidor (gerado em execução)
```

## 🚀 Como Executar Localmente

### Pré-requisitos:
- Python 3.11+
- pip3

### Passo 1: Instalar Dependências

```bash
cd sondagem-app
pip3 install -r requirements.txt
```

### Passo 2: Executar em Modo de Teste (Sem Google Cloud)

```bash
python3 app_test.py
```

Acesse: `http://localhost:5000`

**Modo de Teste:**
- OCR simulado (gera escritas de exemplo)
- IA de análise ATIVA e funcional
- Ideal para demonstrações e testes

### Passo 3: Executar em Modo de Produção (Com Google Cloud)

#### 3.1. Configurar Google Cloud Vision API

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a API "Cloud Vision API"
4. Crie uma conta de serviço e baixe o arquivo JSON de credenciais
5. Configure a variável de ambiente:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/credenciais.json"
```

#### 3.2. Configurar OpenAI API (Já configurado no ambiente Manus)

Se estiver executando fora do ambiente Manus:

```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

#### 3.3. Executar o Servidor

```bash
python3 app.py
```

Acesse: `http://localhost:5000`

**Modo de Produção:**
- OCR REAL (lê imagens de caligrafia infantil)
- IA de análise ATIVA
- Sistema completo e funcional

## 🌐 Como Implantar na Internet

### Opção 1: Heroku (Recomendado para Iniciantes)

1. Crie uma conta em [Heroku](https://heroku.com)
2. Instale o Heroku CLI
3. Execute:

```bash
cd sondagem-app
heroku login
heroku create nome-do-seu-app
git init
git add .
git commit -m "Deploy inicial"
git push heroku main
```

4. Configure as variáveis de ambiente no Heroku:
   - `GOOGLE_APPLICATION_CREDENTIALS` (conteúdo do JSON)
   - `OPENAI_API_KEY`

### Opção 2: PythonAnywhere

1. Crie uma conta em [PythonAnywhere](https://www.pythonanywhere.com)
2. Faça upload dos arquivos
3. Configure um Web App Flask
4. Configure as variáveis de ambiente
5. Recarregue o Web App

### Opção 3: Google Cloud Run

1. Crie um `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
```

2. Execute:

```bash
gcloud run deploy sondagem-app --source .
```

## 📊 Como Funciona a IA

### Módulo `ai_analyzer.py`

O módulo de IA foi instruído com conhecimento pedagógico profundo sobre as hipóteses de escrita. Ele:

1. **Recebe:** Palavra ditada + Escrita da criança
2. **Analisa:** Padrões de correspondência entre sons e letras
3. **Classifica:** Em uma das 5 hipóteses
4. **Justifica:** Explica o raciocínio pedagógico

### Exemplo de Análise:

**Entrada:**
- Palavra ditada: CAVALO
- Escrita da criança: CVLO

**Saída da IA:**
```json
{
  "hipotese": "Silábico-Alfabético",
  "justificativa": "A criança está em transição. Representou algumas sílabas completas (CA → C, LO → LO) e outras com apenas uma letra (VA → V), caracterizando a fase silábico-alfabética."
}
```

## 🔐 Segurança e Privacidade

- ✅ Nenhum dado é armazenado permanentemente
- ✅ Imagens são processadas em memória e descartadas
- ✅ Não há banco de dados (sistema stateless)
- ✅ Ideal para conformidade com LGPD

## 🎯 Casos de Uso

1. **Sondagem Inicial:** Diagnóstico no início do ano letivo
2. **Sondagem Intermediária:** Acompanhamento do progresso
3. **Sondagem Final:** Avaliação do desenvolvimento
4. **Relatórios para Pais:** Documentação clara e profissional
5. **Planejamento Pedagógico:** Dados para formar grupos de trabalho

## 🤝 Contribuindo

Este é um projeto educacional. Sugestões de melhorias:

- [ ] Suporte a múltiplas línguas
- [ ] Histórico de sondagens (requer banco de dados)
- [ ] Gráficos de evolução da turma
- [ ] Exportação para PDF automática
- [ ] Análise de frases (além de palavras)
- [ ] Sugestões de atividades personalizadas

## 📄 Licença

Projeto educacional desenvolvido para auxiliar professores alfabetizadores.

## 👨‍💻 Autor

Desenvolvido com ❤️ para educadores brasileiros.

---

## 📞 Suporte

Para dúvidas sobre configuração ou uso, consulte a documentação das APIs:
- [Google Cloud Vision](https://cloud.google.com/vision/docs)
- [OpenAI API](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Versão:** 1.0.0  
**Data:** Outubro de 2025  
**Status:** ✅ Funcional e Testado

