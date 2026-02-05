import requests

API_URL = "http://127.0.0.1:8000/registrar"

dados_iniciais = [
    {
        "titulo": "The Last of Us",
        "categoria": "jogo",
        "status": "Concluido",
        "nota": 10.0,
        "comentario": "Melhor narrativa dos games.",
        "imagem_url": "https://image.api.playstation.com/vulcan/ap/rnd/202206/0720/eEHQBmHpmnzSB2JaZR1SsPvH.png"
    },
    {
        "titulo": "Breaking Bad",
        "categoria": "serie",
        "status": "Concluido",
        "nota": 9.9,
        "comentario": "Química pura.",
        "imagem_url": "https://m.media-amazon.com/images/M/MV5BYmQ4YWMxYjktNzcxZi00OTJkLWE2ODItNWRmNHZmNzQwYjZkXkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg"
    },
    {
        "titulo": "Duna",
        "categoria": "livro",
        "status": "Lendo",
        "nota": 8.5,
        "comentario": "O início é lento, mas o mundo é incrível.",
        "imagem_url": "https://m.media-amazon.com/images/I/81zN7udGRUL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "titulo": "Interestelar",
        "categoria": "filme",
        "status": "Planejando",
        "nota": None,
        "comentario": "",
        "imagem_url": "https://upload.wikimedia.org/wikipedia/pt/3/3a/Interstellar_Filme.jpg"
    }
]

print("Iniciando o povoamento do banco...")

for item in dados_iniciais:
    try:
        response = requests.post(API_URL, json=item)
        if response.status_code == 200:
            print(f"✅ {item['titulo']} inserido com sucesso!")
        else:
            print(f"Erro ao inserir {item['titulo']}: {response.text}")
    except Exception as e:
        print(f"Erro crítico: {e}")

print("Finalizado!")