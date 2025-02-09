import requests
import json

# URL da API do Gemini
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDZkEeLjT8q1TMc-jS7wLREFt9TL9cngFE"

# Cabeçalhos da requisição
headers = {
    'Content-Type': 'application/json'
}

# Corpo da requisição
data = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Explain how AI works"
                }
            ]
        }
    ]
}

# Fazendo a requisição POST
response = requests.post(url, headers=headers, data=json.dumps(data))

# Verificando a resposta
if response.status_code == 200:
    print("Resposta da API:")
    print(response.json())
else:
    print(f"Erro na requisição: {response.status_code}")
    print(response.text)