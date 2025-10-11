"""
Servidor Flask para o Sistema de Sondagem Pedagógica - VERSÃO DE TESTE
Esta versão simula o OCR para permitir testes sem configuração do Google Cloud
"""

import os
from flask import Flask, request, jsonify, render_template
from ai_analyzer import analisar_escrita, analisar_multiplas_palavras
import io

# Configuração do Flask
app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    """Rota principal que carrega a página de sondagem."""
    return render_template('sondagem.html')


@app.route('/analyze', methods=['POST'])
def analyze_image():
    """
    Rota que recebe a imagem e analisa com IA.
    VERSÃO DE TESTE: Simula o OCR pedindo para o usuário digitar manualmente.
    """
    
    # Validação dos dados recebidos
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    if 'palavras_ditadas' not in request.form:
        return jsonify({'error': 'Palavras ditadas não foram informadas'}), 400

    file = request.files['file']
    palavras_ditadas_texto = request.form['palavras_ditadas']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400

    try:
        # ===== SIMULAÇÃO DE OCR =====
        # Em um ambiente de produção, aqui seria usado o Google Vision
        # Para teste, vamos retornar uma mensagem pedindo entrada manual
        
        # Processa as palavras ditadas
        palavras_lista = [p.strip() for p in palavras_ditadas_texto.replace('\n', ',').split(',') if p.strip()]
        
        if len(palavras_lista) == 0:
            return jsonify({'error': 'Nenhuma palavra ditada foi informada'}), 400
        
        # MODO DE DEMONSTRAÇÃO: Vamos simular uma escrita para a primeira palavra
        # Em produção real, isso viria do OCR
        if len(palavras_lista) == 1:
            palavra = palavras_lista[0].upper()
            
            # Simula diferentes tipos de escrita baseado na palavra
            if palavra == "CAVALO":
                texto_simulado = "CVLO"  # Silábico-Alfabético
            elif palavra == "BOLA":
                texto_simulado = "BOA"   # Silábico com valor sonoro
            elif palavra == "PÉ":
                texto_simulado = "PE"    # Alfabético
            elif palavra == "FORMIGA":
                texto_simulado = "FRMGA" # Silábico-Alfabético
            else:
                # Para outras palavras, simula escrita alfabética com pequena variação
                texto_simulado = palavra
            
            resultado_ia = analisar_escrita(palavra, texto_simulado)
            
            return jsonify({
                'transcricao': texto_simulado,
                'hipotese': resultado_ia['hipotese'],
                'justificativa': resultado_ia['justificativa'],
                'modo': 'simulacao_teste',
                'aviso': 'MODO DE TESTE: A transcrição foi simulada. Em produção, o OCR lerá a imagem real.'
            })
        
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
            
            resultado_ia = analisar_multiplas_palavras(palavras_lista, escritas_simuladas)
            
            return jsonify({
                'transcricao': ' '.join(escritas_simuladas),
                'hipotese': resultado_ia['hipotese'],
                'justificativa': resultado_ia['justificativa'],
                'analises_individuais': resultado_ia.get('analises_individuais', []),
                'modo': 'simulacao_teste_multiplas',
                'aviso': 'MODO DE TESTE: As transcrições foram simuladas. Em produção, o OCR lerá a imagem real.'
            })

    except Exception as e:
        return jsonify({
            'error': f'Ocorreu um erro ao processar: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Rota de verificação de saúde do servidor."""
    return jsonify({
        'status': 'online',
        'modo': 'teste',
        'ocr_disponivel': False,
        'ia_disponivel': True
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("🎓 SISTEMA DE SONDAGEM PEDAGÓGICA - MODO DE TESTE")
    print("="*60)
    print(f"🌐 Servidor rodando em: http://localhost:{port}")
    print("⚠️  MODO DE TESTE: OCR simulado (não requer Google Cloud)")
    print("✅ IA de análise: ATIVA")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=port, debug=True)

