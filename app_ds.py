import cv2
from PIL import Image
import requests
import pyttsx3
import os
import io
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da API do Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Chave da API carregada do ambiente
genai.configure(api_key=GEMINI_API_KEY)


def extract_text_from_image(image_path, prompt_text="Extraia o texto contido nesta imagem:"):
    """
    Extrai texto de uma imagem usando a API Gemini.

    Args:
        image_path: Caminho para o arquivo de imagem.
        prompt_text: Texto do prompt para guiar o modelo.

    Returns:
        O texto extraído da imagem, ou None se ocorrer um erro.
    """
    try:
        # Carregue a imagem
        img = Image.open(image_path)

        # Converta a imagem para bytes (formato esperado pela API Gemini)
        with io.BytesIO() as output:
            img.save(output, format="JPEG")  # Ou PNG, dependendo da imagem
            image_bytes = output.getvalue()

        # Carregue o modelo Gemini Vision (gemini-pro-vision)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Construa o prompt (incluindo a imagem)
        prompt = prompt_text
        image_data = {"mime_type": "image/jpeg", "data": image_bytes}  # Ajuste o tipo MIME se necessário

        # Envie a requisição ao modelo
        response = model.generate_content([prompt, image_data])

        # Obtenha o texto da resposta
        text = response.text

        return text

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")
        return None




def capturar_imagem():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        raise Exception("Erro ao capturar imagem")

def carregar_imagem(caminho_imagem):
    return Image.open(caminho_imagem)


def falar_texto(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def main():
    # Captura ou carrega a imagem
    caminho_imagem = ""
    opcao = input("Deseja capturar uma imagem (1) ou carregar de um arquivo (2)? ")
    if opcao == '1':
        imagem = capturar_imagem()
        imagem = Image.fromarray(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    elif opcao == '2':
        caminho_imagem = input("Digite o caminho da imagem: ")
        imagem = carregar_imagem(caminho_imagem)
    else:
        print("Opção inválida")
        return

    # Converte a imagem para o formato esperado pela API
    imagem.save('temp.jpg')
    with open('temp.jpg', 'rb') as f:
        imagem_bytes = f.read()

    # Envia a imagem para a API do Gemini
    texto = extract_text_from_image(caminho_imagem)
    print(f"Texto extraído: {texto}")

    # Fala o texto extraído
    falar_texto(texto)

if __name__ == "__main__":
    main()