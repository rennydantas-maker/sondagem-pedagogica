"""
Servidor Flask para o Sistema de Sondagem Pedagógica
Versão de produção com OCR simulado (não requer Google Cloud)
"""

import os
from flask import Flask, request, jsonify, render_template
from ai_analyzer import analisar_escrita, analisar_multiplas_palavras, analisar_escrita_com_imagem
import io

# Configuração do Flask
app = Flask(__name__, template_folder='templates')

# Modo de produção sem Google Vision (OCR simulado)
OCR_DISPONIVEL = False


@app.route('/')
def index():
    """Rota principal que carrega a página de sondagem."""
    return render_template('sondagem.html')


@app.route('/analyze', methods=['POST'])
def analyze_image():
    """
    Rota que recebe a imagem, processa com OCR e analisa com IA.
    
    Fluxo SIMPLIFICADO:
    1. Recebe a imagem, palavras ditadas (em um único campo) e transcrição prévia
    2. Usa OCR para extrair o texto da imagem (ou usa a transcrição prévia)
    3. Usa IA para classificar a hipótese de escrita
    4. Retorna a transcrição, hipótese e justificativa
    """
    
    # Validação dos dados recebidos
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    
    # Recebe os campos simplificados
    palavras_ditadas = request.form.get('palavras_ditadas', '').strip()
    transcricao_previa = request.form.get('transcricao_previa', '').strip()
    
    # Log dos dados recebidos (para debugging)
    print(f"[DEBUG] Dados recebidos:")
    print(f"  Palavras ditadas: '{palavras_ditadas}'")
    print(f"  Transcrição prévia: '{transcricao_previa}'")
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    try:
        # ===== PROCESSA AS PALAVRAS DITADAS =====
        # Separa as palavras por vírgula ou quebra de linha
        palavras_lista = []
        if palavras_ditadas:
            # Substitui quebras de linha por vírgulas e depois separa
            palavras_texto = palavras_ditadas.replace('\n', ',')
            palavras_lista = [p.strip() for p in palavras_texto.split(',') if p.strip()]
        
        print(f"[DEBUG] Total de palavras ditadas: {len(palavras_lista)}")
        print(f"[DEBUG] Palavras: {palavras_lista}")
        
        if len(palavras_lista) == 0:
            return jsonify({'error': 'Nenhuma palavra ou frase ditada foi informada'}), 400
        
        # ===== SALVA A IMAGEM TEMPORARIAMENTE =====
        # Salva a imagem para o Gemini processar
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
            file.save(tmp_file.name)
            temp_image_path = tmp_file.name
        
        print(f"[DEBUG] Imagem salva em: {temp_image_path}")
        
        # ===== PRIORIDADE: TRANSCRIÇÃO PRÉVIA =====
        # Se o professor forneceu uma transcrição prévia, usa ela ao invés do Gemini Vision
        if transcricao_previa:
            texto_extraido = transcricao_previa
            print(f"[DEBUG] Usando transcrição prévia: '{texto_extraido}'")
        else:
            # ===== ANÁLISE COM GEMINI VISION =====
            # Usa o Gemini para ler a imagem diretamente
            print(f"[DEBUG] Usando Gemini Vision para analisar a imagem...")
            
            try:
                resultado_gemini = analisar_escrita_com_imagem(palavras_ditadas, temp_image_path)
                texto_extraido = resultado_gemini.get('transcricao', '')
                print(f"[DEBUG] Gemini extraiu: '{texto_extraido}'")
                
                # Se o Gemini retornou uma análise completa, usa ela diretamente
                if resultado_gemini.get('hipotese') and resultado_gemini.get('hipotese') != 'Erro na Análise':
                    # Limpa o arquivo temporário
                    import os as os_module
                    try:
                        os_module.unlink(temp_image_path)
                    except:
                        pass
                    
                    return jsonify({
                        'transcricao': resultado_gemini.get('transcricao', ''),
                        'hipotese': resultado_gemini.get('hipotese', ''),
                        'justificativa': resultado_gemini.get('justificativa', ''),
                        'modo': 'gemini_vision'
                    })
            
            except Exception as e:
                print(f"[DEBUG] Erro ao usar Gemini Vision: {str(e)}")
                print(f"[DEBUG] Voltando para simulação de OCR...")
            
            # Se o Gemini falhou, usa simulação de OCR como fallback
            if len(palavras_lista) == 1:
                palavra = palavras_lista[0].upper()
                
                # Simula diferentes tipos de escrita baseado na palavra
                if palavra == "CAVALO":
                    texto_extraido = "CVLO"
                elif palavra == "BOLA":
                    texto_extraido = "BOA"
                elif palavra == "PÉ" or palavra == "PE":
                    texto_extraido = "PE"
                elif palavra == "FORMIGA":
                    texto_extraido = "FRMGA"
                else:
                    # Para outras palavras, simula escrita alfabética com variação
                    texto_extraido = palavra
            
            else:
                # Para múltiplas palavras, simula escritas variadas
                escritas_simuladas = []
                for palavra in palavras_lista:
                    palavra_upper = palavra.upper()
                    # Remove vogais aleatoriamente para simular escrita silábico-alfabética
                    if len(palavra_upper) > 3:
                        escrita_sim = ''.join([c for i, c in enumerate(palavra_upper) if i % 2 == 0 or c in 'AEIOU'])
                    else:
                        escrita_sim = palavra_upper
                    escritas_simuladas.append(escrita_sim)
                
                texto_extraido = ', '.join(escritas_simuladas)
            
            print(f"[DEBUG] Texto simulado (fallback): '{texto_extraido}'")
        
        # Limpa o arquivo temporário
        import os as os_module
        try:
            os_module.unlink(temp_image_path)
        except:
            pass
        
        # ===== ANÁLISE COM IA =====
        # Processa as escritas extraídas (do OCR ou da transcrição prévia)
        escritas_lista = []
        if texto_extraido:
            # Substitui quebras de linha por vírgulas e depois separa
            escritas_texto = texto_extraido.replace('\n', ',')
            escritas_lista = [e.strip() for e in escritas_texto.split(',') if e.strip()]
        
        print(f"[DEBUG] Total de escritas: {len(escritas_lista)}")
        print(f"[DEBUG] Escritas: {escritas_lista}")
        
        if len(escritas_lista) == 0:
            return jsonify({'error': 'Não foi possível extrair texto da imagem ou da transcrição'}), 400
        
        # ===== ANÁLISE INTELIGENTE =====
        # Se houver apenas uma palavra/escrita
        if len(palavras_lista) == 1 and len(escritas_lista) == 1:
            print(f"[DEBUG] Analisando palavra única: '{palavras_lista[0]}' → '{escritas_lista[0]}'")
            resultado_ia = analisar_escrita(palavras_lista[0], escritas_lista[0])
            
            return jsonify({
                'transcricao': escritas_lista[0],
                'hipotese': resultado_ia['hipotese'],
                'justificativa': resultado_ia['justificativa'],
                'modo': 'transcricao_previa' if transcricao_previa else 'simulacao_ocr'
            })
        
        # Se houver múltiplas palavras/escritas
        else:
            print(f"[DEBUG] Analisando múltiplas palavras...")
            resultado_ia = analisar_multiplas_palavras(palavras_lista, escritas_lista)
            
            return jsonify({
                'transcricao': ', '.join(escritas_lista),
                'hipotese': resultado_ia['hipotese'],
                'justificativa': resultado_ia['justificativa'],
                'analises_individuais': resultado_ia.get('analises_individuais', []),
                'modo': 'transcricao_previa' if transcricao_previa else 'simulacao_ocr_multiplas'
            })

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[ERROR] Erro ao processar análise:")
        print(error_details)
        return jsonify({
            'error': f'Ocorreu um erro ao processar: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Rota de verificação de saúde do servidor."""
    return jsonify({
        'status': 'online',
        'modo': 'producao_simulado',
        'ocr_disponivel': False,
        'ia_disponivel': True
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

