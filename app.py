import os
import base64
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não está definido no arquivo .env")

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

# Função para extrair texto
def extract_text_from_image(image_bytes):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        image_data = {"mime_type": "image/jpeg", "data": image_bytes}
        response = model.generate_content(["Extraia o texto contido nesta imagem:", image_data])
        return response.text
    except Exception as e:
        return f"Erro ao extrair texto: {str(e)}"

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para extrair texto da imagem
@app.route('/extrair_texto', methods=['POST'])
def extrair_texto():
    dados = request.get_json()
    imagem_base64 = dados.get('imagem')
    
    if imagem_base64:
        try:
            image_bytes = base64.b64decode(imagem_base64)
            texto = extract_text_from_image(image_bytes)
            return jsonify({'texto': texto})
        except Exception as e:
            return jsonify({'erro': f"Erro ao processar imagem: {str(e)}"})
    
    return jsonify({'erro': 'Nenhuma imagem recebida'})

if __name__ == '__main__':
    app.run(debug=True)
