import cv2
import pyttsx3
import requests
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import base64
import io
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Chave da API carregada do ambiente
GEMINI_URL = "https://api.gemini.com/v1/ocr"

def capturar_imagem():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret:
        filename = "captura.jpg"
        cv2.imwrite(filename, frame)
        processar_imagem(filename)

def carregar_imagem():
    filename = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg;*.png;*.jpeg")])
    if filename:
        processar_imagem(filename)

def processar_imagem(filename):
    with open(filename, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    
    response = requests.post(
        GEMINI_URL,
        headers={"Authorization": f"Bearer {GEMINI_API_KEY}"},
        json={"image": img_base64}
    )
    
    if response.status_code == 200:
        texto_extraido = response.json().get("text", "Não foi possível reconhecer o texto.")
        exibir_texto(texto_extraido)
        falar_texto(texto_extraido)
    else:
        exibir_texto("Erro ao processar imagem")

def falar_texto(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def exibir_texto(texto):
    texto_saida.config(state=tk.NORMAL)
    texto_saida.delete("1.0", tk.END)
    texto_saida.insert(tk.END, texto)
    texto_saida.config(state=tk.DISABLED)

def criar_interface():
    global texto_saida
    
    root = tk.Tk()
    root.title("Leitor de Texto")
    
    btn_capturar = tk.Button(root, text="Capturar Imagem", command=capturar_imagem)
    btn_capturar.pack(pady=10)
    
    btn_carregar = tk.Button(root, text="Carregar Imagem", command=carregar_imagem)
    btn_carregar.pack(pady=10)
    
    texto_saida = tk.Text(root, height=5, width=50, state=tk.DISABLED)
    texto_saida.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    criar_interface()
