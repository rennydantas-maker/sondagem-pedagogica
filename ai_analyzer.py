"""
Módulo de Análise de Hipóteses de Escrita com Inteligência Artificial
Este módulo usa o Google Gemini para analisar a escrita de crianças
e classificar a hipótese de escrita segundo a psicogênese da língua escrita.
"""

import os
import google.generativeai as genai
from PIL import Image
import json

# Configura o Gemini com a chave da API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_DISPONIVEL = False

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_DISPONIVEL = True
        print("[INFO] Gemini configurado com sucesso")
    except Exception as e:
        print(f"[WARN] Erro ao configurar Gemini: {str(e)}")
        GEMINI_DISPONIVEL = False
else:
    print("[WARN] GEMINI_API_KEY não configurada. Sistema usará modo de simulação.")

# Prompt de sistema que ensina a IA sobre as hipóteses de escrita
SYSTEM_PROMPT = """Você é um especialista em alfabetização e psicogênese da língua escrita, baseado nos estudos de Emilia Ferreiro e Ana Teberosky. Sua função é analisar a escrita de crianças em processo de alfabetização e classificá-las nas seguintes hipóteses de escrita:

**1. Pré-Silábico:**
- A criança ainda não compreende que a escrita representa os sons da fala
- Usa letras aleatórias, números, pseudoletras ou desenhos
- Não há correspondência entre o que escreve e os sons da palavra
- Pode usar a mesma letra repetida ou letras sem relação com a palavra
- Exemplo: Para "CAVALO" escreve "XPTO" ou "AAAA" ou "123"

**2. Silábico sem valor sonoro:**
- A criança descobre que a escrita representa a fala
- Usa uma letra para cada sílaba da palavra
- Porém, as letras escolhidas ainda não têm relação com os sons reais
- Exemplo: Para "CAVALO" (3 sílabas: CA-VA-LO) escreve "XPT" ou "BDF"

**3. Silábico com valor sonoro:**
- A criança usa uma letra para cada sílaba
- As letras escolhidas TÊM relação com os sons da sílaba (vogais ou consoantes)
- Pode usar só vogais (AO para CAVALO) ou misturar vogais e consoantes (CAO, CVO)
- Exemplo: Para "CAVALO" escreve "AO" ou "CAO" ou "CVO"

**4. Silábico-Alfabético:**
- Fase de transição entre o silábico e o alfabético
- A criança ora escreve uma letra por sílaba, ora representa todos os sons
- Algumas sílabas estão completas, outras têm apenas uma letra
- Exemplo: Para "CAVALO" escreve "CVLO" ou "CAVLO" ou "CAVAL"

**5. Alfabético:**
- A criança compreende que cada som (fonema) é representado por uma letra (grafema)
- Escreve todas as letras necessárias, mesmo que com erros ortográficos
- A escrita é legível e foneticamente coerente
- Exemplo: Para "CAVALO" escreve "CAVALO" ou "KAVALO" ou "CAVALU"

**Sua tarefa:**
Quando receber uma palavra ditada e o que a criança escreveu, você deve:
1. Analisar a relação entre a escrita e a palavra ditada
2. Identificar padrões (letras por sílaba, correspondência sonora, etc.)
3. Classificar na hipótese mais adequada
4. Explicar brevemente o raciocínio

Responda SEMPRE no formato JSON:
{
  "hipotese": "Nome da Hipótese",
  "justificativa": "Explicação pedagógica da classificação"
}
"""


def analisar_escrita_com_imagem(palavras_ditadas: str, imagem_path: str) -> dict:
    """
    Analisa a escrita da criança diretamente da imagem usando Gemini Vision.
    
    Args:
        palavras_ditadas: As palavras/frase que foram ditadas para a criança
        imagem_path: Caminho para a imagem da escrita
    
    Returns:
        dict: Dicionário com 'transcricao', 'hipotese' e 'justificativa'
    """
    
    # Verifica se o Gemini está disponível
    if not GEMINI_DISPONIVEL:
        return {
            "transcricao": "",
            "hipotese": "Erro na Análise",
            "justificativa": "Gemini não está configurado. Configure a variável GEMINI_API_KEY no Render.com."
        }
    
    try:
        # Carrega a imagem
        img = Image.open(imagem_path)
        
        # Cria o modelo Gemini com visão
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Prepara o prompt completo
        prompt = f"""{SYSTEM_PROMPT}

Analise a imagem da escrita da criança e faça o seguinte:

1. **Transcreva** exatamente o que a criança escreveu na imagem
2. **Compare** com as palavras ditadas: {palavras_ditadas}
3. **Classifique** a hipótese de escrita
4. **Justifique** pedagogicamente sua classificação

Responda no formato JSON:
{{
  "transcricao": "O que você leu na imagem",
  "hipotese": "Nome da Hipótese",
  "justificativa": "Explicação pedagógica detalhada"
}}
"""
        
        # Envia para o Gemini
        response = model.generate_content([prompt, img])
        
        # Extrai o JSON da resposta
        response_text = response.text.strip()
        
        # Remove markdown code blocks se existirem e limpa o texto antes de decodificar JSON
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
            
        # Tenta encontrar o primeiro e último { } para garantir que só o JSON seja decodificado
        try:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            response_text = response_text[json_start:json_end]
        except ValueError:
            # Se não encontrar chaves, tenta decodificar o texto inteiro e lança erro se falhar
            pass
            
        resultado = json.loads(response_text)
        
        return resultado
    
    except Exception as e:
        # Em caso de erro, retorna uma resposta padrão
        error_msg = str(e)
        print(f"[ERROR] Erro no Gemini Vision: {error_msg}")
        
        # Se for erro de autenticação, retorna mensagem clara
        if "API key" in error_msg or "authentication" in error_msg.lower():
            return {
                "transcricao": "",
                "hipotese": "Erro na Análise",
                "justificativa": "Chave API do Gemini inválida ou não configurada. Configure GEMINI_API_KEY no Render.com."
            }
        
        return {
            "transcricao": "",
            "hipotese": "Erro na Análise",
            "justificativa": f"Erro ao processar com Gemini: {error_msg[:200]}"
        }


def analisar_escrita(palavra_ditada: str, escrita_crianca: str) -> dict:
    """
    Analisa a escrita da criança (quando já temos a transcrição).
    
    Args:
        palavra_ditada: A palavra que foi ditada para a criança
        escrita_crianca: O que a criança escreveu (já transcrito)
    
    Returns:
        dict: Dicionário com 'hipotese' e 'justificativa'
    """
    
    # Se não houver escrita, retorna pré-silábico por padrão
    if not escrita_crianca or escrita_crianca.strip() == "":
        return {
            "hipotese": "Pré-Silábico",
            "justificativa": "Não foi possível identificar escrita na imagem."
        }
    
    # Verifica se o Gemini está disponível
    if not GEMINI_DISPONIVEL:
        return {
            "hipotese": "Erro na Análise",
            "justificativa": "Gemini não está configurado. Configure a variável GEMINI_API_KEY."
        }
    
    try:
        # Cria o modelo Gemini
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Prepara o prompt
        prompt = f"""{SYSTEM_PROMPT}

Analise a seguinte escrita:

Palavra ditada: {palavra_ditada.upper()}
Escrita da criança: {escrita_crianca.upper()}

Classifique a hipótese de escrita e justifique.

Responda no formato JSON:
{{
  "hipotese": "Nome da Hipótese",
  "justificativa": "Explicação pedagógica"
}}
"""
        
        # Envia para o Gemini
        response = model.generate_content(prompt)
        
        # Extrai o JSON da resposta
        response_text = response.text.strip()
        
        # Remove markdown code blocks se existirem e limpa o texto antes de decodificar JSON
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
            
        # Tenta encontrar o primeiro e último { } para garantir que só o JSON seja decodificado
        try:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            response_text = response_text[json_start:json_end]
        except ValueError:
            # Se não encontrar chaves, tenta decodificar o texto inteiro e lança erro se falhar
            pass
            
        resultado = json.loads(response_text)
        
        return resultado
    
    except Exception as e:
        # Em caso de erro, retorna uma resposta padrão
        return {
            "hipotese": "Erro na Análise",
            "justificativa": f"Ocorreu um erro ao processar a análise: {str(e)}"
        }


def analisar_multiplas_palavras(palavras_ditadas: list, escritas: list) -> dict:
    """
    Analisa múltiplas palavras e retorna uma classificação geral.
    
    Args:
        palavras_ditadas: Lista de palavras ditadas
        escritas: Lista das escritas correspondentes
    
    Returns:
        dict: Dicionário com 'hipotese' geral, 'justificativa' e 'analises_individuais'
    """
    
    if len(palavras_ditadas) != len(escritas):
        return {
            "hipotese": "Erro",
            "justificativa": "Número de palavras ditadas e escritas não correspondem."
        }
    
    # Analisa cada palavra individualmente
    analises = []
    for palavra, escrita in zip(palavras_ditadas, escritas):
        resultado = analisar_escrita(palavra, escrita)
        analises.append({
            "palavra": palavra,
            "escrita": escrita,
            "hipotese": resultado["hipotese"],
            "justificativa": resultado["justificativa"]
        })
    
    # Prepara um prompt para síntese geral
    if not GEMINI_DISPONIVEL:
        return {
            "hipotese": "Erro na Análise",
            "justificativa": "Gemini não está configurado. Configure a variável GEMINI_API_KEY.",
            "analises_individuais": analises
        }
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        analises_texto = "\n".join([f"- {a['palavra']}: escreveu '{a['escrita']}' → {a['hipotese']}" for a in analises])
        
        sintese_prompt = f"""{SYSTEM_PROMPT}

Com base nas seguintes análises individuais, determine a hipótese de escrita GERAL da criança:

{analises_texto}

Considerando que:
- Se todas as análises apontam para a mesma hipótese, essa é a hipótese geral
- Se há variação, escolha a hipótese que melhor representa o nível de compreensão predominante
- Em caso de transição, prefira a hipótese mais avançada que aparece consistentemente

Responda no formato JSON com a hipótese geral e justificativa:
{{
  "hipotese": "Nome da Hipótese Geral",
  "justificativa": "Explicação pedagógica da classificação geral"
}}
"""
        
        response = model.generate_content(sintese_prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks se existirem e limpa o texto antes de decodificar JSON
        if response_text.startswith('```json'):
            response_text = response_text.replace('```json', '').replace('```', '').strip()
        elif response_text.startswith('```'):
            response_text = response_text.replace('```', '').strip()
            
        # Tenta encontrar o primeiro e último { } para garantir que só o JSON seja decodificado
        try:
            json_start = response_text.index('{')
            json_end = response_text.rindex('}') + 1
            response_text = response_text[json_start:json_end]
        except ValueError:
            # Se não encontrar chaves, tenta decodificar o texto inteiro e lança erro se falhar
            pass
        
        resultado_geral = json.loads(response_text)      
        return {
            "hipotese": resultado_geral["hipotese"],
            "justificativa": resultado_geral["justificativa"],
            "analises_individuais": analises
        }
    
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Erro ao processar análise geral (Gemini): {error_msg}")
        
        # Se for erro de autenticação, retorna mensagem clara
        if "API key" in error_msg or "authentication" in error_msg.lower():
            justificativa = "Chave API do Gemini inválida ou não configurada. Configure GEMINI_API_KEY no Render.com."
        elif "Invalid JSON" in error_msg:
            justificativa = "O Gemini retornou um formato inválido. Tente novamente ou simplifique o texto."
        else:
            justificativa = f"Erro ao processar análise geral: {error_msg[:200]}"
            
        return {
            "hipotese": "Erro na Análise",
            "justificativa": justificativa,
            "analises_individuais": analises
        }

