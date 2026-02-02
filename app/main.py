from fastapi import FastAPI
from app.database import supabase 

app = FastAPI(title="Sesh API")

@app.get("/")
def home():
    return {"message": "Sesh está online!"}

@app.post("/registrar")
def registrar_entretenimento(titulo: str, categoria: str, nota: int):
    dados = {
        "titulo": titulo,
        "categoria": categoria,
        "nota": nota
    }
    

    response = supabase.table("entretenimento").insert(dados).execute()
    return{"status": "Registrado com sucesso!", "data": response.data}