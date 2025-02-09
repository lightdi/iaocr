import os
import io
import base64
import pyttsx3
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from PIL import Image

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

# Função para ler o texto
def falar_texto(texto):
    try:
        engine = pyttsx3.init()
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro ao falar texto: {str(e)}")

# Rotas Flask
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extrair_texto', methods=['POST'])
def extrair_texto():
    dados = request.get_json()
    imagem_base64 = dados.get('imagem')
    if imagem_base64:
        try:
            image_bytes = base64.b64decode(imagem_base64)
            texto = extract_text_from_image(image_bytes)
            falar_texto(texto)
            return jsonify({'texto': texto})
        except Exception as e:
            return jsonify({'erro': f"Erro ao processar imagem: {str(e)}"})
    return jsonify({'erro': 'Nenhuma imagem recebida'})

if __name__ == '__main__':
    #app.run( host="192.168.68.51",port=5000, debug=True)
    app.run( debug=True)