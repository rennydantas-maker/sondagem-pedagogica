"""
Servidor Flask para o Sistema de Sondagem Pedagógica
Versão de produção com OCR simulado (não requer Google Cloud)
"""

import os
from flask import Flask, request, jsonify, render_template
from ai_analyzer import analisar_escrita, analisar_multiplas_palavras
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
    
    Fluxo:
    1. Recebe a imagem, palavras ditadas (separadas por tipo silábico), frase e transcrição prévia
    2. Usa OCR para extrair o texto da imagem (ou usa a transcrição prévia)
    3. Usa IA para classificar a hipótese de escrita
    4. Retorna a transcrição, hipótese e justificativa
    """
    
    # Validação dos dados recebidos
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    
    # Recebe os campos separados de palavras ditadas
    monossilaba = request.form.get('monossilaba', '').strip()
    dissilaba = request.form.get('dissilaba', '').strip()
    trissilaba = request.form.get('trissilaba', '').strip()
    polissilaba = request.form.get('polissilaba', '').strip()
    frase_ditada = request.form.get('frase', '').strip()
    transcricao_previa = request.form.get('transcricao_previa', '').strip()
    
    # Log dos dados recebidos (para debugging)
    print(f"[DEBUG] Dados recebidos:")
    print(f"  Monossílaba: '{monossilaba}'")
    print(f"  Dissílaba: '{dissilaba}'")
    print(f"  Trissílaba: '{trissilaba}'")
    print(f"  Polissílaba: '{polissilaba}'")
    print(f"  Frase: '{frase_ditada}'")
    print(f"  Transcrição prévia: '{transcricao_previa}'")
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    try:
        # ===== PROCESSA AS PALAVRAS DITADAS =====
        # Junta todas as palavras dos 4 campos
        palavras_lista = []
        print(f"[DEBUG] Processando palavras...")
        
        if monossilaba:
            palavras_lista.extend([p.strip() for p in monossilaba.replace('\n', ',').split(',') if p.strip()])
        if dissilaba:
            palavras_lista.extend([p.strip() for p in dissilaba.replace('\n', ',').split(',') if p.strip()])
        if trissilaba:
            palavras_lista.extend([p.strip() for p in trissilaba.replace('\n', ',').split(',') if p.strip()])
        if polissilaba:
            palavras_lista.extend([p.strip() for p in polissilaba.replace('\n', ',').split(',') if p.strip()])
        
        # ===== PRIORIDADE: TRANSCRIÇÃO PRÉVIA =====
        # Se o professor forneceu uma transcrição prévia, usa ela ao invés do OCR
        if transcricao_previa:
            texto_extraido = transcricao_previa
        else:
            # ===== SIMULAÇÃO DE OCR =====
            # MODO DE DEMONSTRAÇÃO: Simula escrita para as palavras
            if len(palavras_lista) == 1:
                palavra = palavras_lista[0].upper()
                
                # Simula diferentes tipos de escrita baseado na palavra
                if palavra == "CAVALO":
                    texto_extraido = "CVLO"
                elif palavra == "BOLA":
                    texto_extraido = "BOA"
                elif palavra == "PÉ":
                    texto_extraido = "PE"
                elif palavra == "FORMIGA":
                    texto_extraido = "FRMGA"
                else:
                    # Para outras palavras, simula escrita alfabética com variação
                    texto_extraido = palavra
            
            elif len(palavras_lista) > 1:
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
            
            elif frase_ditada:
                # Se só tem frase, simula escrita da frase
                texto_extraido = frase_ditada.upper()
            else:
                texto_extraido = ""
        
        # ===== ANÁLISE COM IA =====
        # Processa as escritas extraídas (do OCR ou da transcrição prévia)
        escritas_lista = [e.strip() for e in texto_extraido.replace('\n', ',').split(',') if e.strip()]
        
        if len(palavras_lista) == 0 and not frase_ditada:
            print(f"[DEBUG] Erro: Nenhuma palavra ou frase informada")
            return jsonify({'error': 'Nenhuma palavra ou frase ditada foi informada'}), 400
        
        print(f"[DEBUG] Total de palavras: {len(palavras_lista)}")
        print(f"[DEBUG] Palavras: {palavras_lista}")
        print(f"[DEBUG] Escritas: {escritas_lista}")
        
        # Se houver apenas uma palavra
        if len(palavras_lista) == 1 and len(escritas_lista) == 1:
            resultado_ia = analisar_escrita(palavras_lista[0], escritas_lista[0])
            
            return jsonify({
                'transcricao': escritas_lista[0],
                'hipotese': resultado_ia['hipotese'],
                'justificativa': resultado_ia['justificativa'],
                'modo': 'transcricao_previa' if transcricao_previa else 'simulacao_producao'
            })
        
        # Se houver múltiplas palavras
        elif len(palavras_lista) > 1 and len(escritas_lista) > 0:
            resultado_ia = analisar_multiplas_palavras(palavras_lista, escritas_lista)
            
            return jsonify({
                'transcricao': ', '.join(escritas_lista),
                'hipotese': resultado_ia['hipotese'],
                'justificativa': resultado_ia['justificativa'],
                'analises_individuais': resultado_ia.get('analises_individuais', []),
                'modo': 'transcricao_previa' if transcricao_previa else 'simulacao_producao_multiplas'
            })
        
        # Se houver apenas frase
        elif frase_ditada and len(escritas_lista) == 1:
            resultado_ia = analisar_escrita(frase_ditada, escritas_lista[0])
            
            return jsonify({
                'transcricao': escritas_lista[0],
                'hipotese': resultado_ia['hipotese'],
                'justificativa': resultado_ia['justificativa'],
                'modo': 'transcricao_previa_frase' if transcricao_previa else 'simulacao_producao_frase'
            })
        
        else:
            return jsonify({'error': 'Não foi possível processar a análise. Verifique os dados enviados.'}), 400

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

