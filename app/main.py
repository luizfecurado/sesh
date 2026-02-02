from fastapi import FastAPI, HTTPException
from app.database import supabase 
from app.schemas import Entretenimento

app = FastAPI(title="Sesh API")

@app.get("/")
def home():
    return {"message": "Sesh está online!"}

@app.post("/registrar")
def registrar_entretenimento(item: Entretenimento):
    try:
        dados_para_banco = item.model_dump()

        response = supabase.table("entretenimento").insert(dados_para_banco).execute()

        return {"status": "Sucesso", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


