from fastapi import FastAPI, HTTPException
from app.database import supabase 
from app.schemas import Entretenimento
from typing import Optional
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


@app.get("/itens")
def listar_itens(categoria: Optional[str] = None):
    try: 
        consulta = supabase.table("entretenimento").select("*")

        if categoria:
            consulta = consulta.eq("categoria", categoria)

        response = consulta.order("id").execute()

        return {
            "total": len(response.data),
            "filtro_aplicado": categoria,
            "dados": response.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/itens/{item_id}")
def deletar_item(item_id: int):
    try:
        response = supabase.table("entretenimento").delete().eq("id", item_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Item não encontrado")

        return{
            "status": "Item deletado com sucesso", "id": item_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    
@app.put("/itens/{item_id}")
def atualizar_itens(item_id, item: Entretenimento):
    try: 
        #validação dados
        dados_novos = item.model_dump()
        #atualiza no banco onde id solicitado é igual
        response = supabase.table("entretenimento").update(dados_novos).eq("id", item_id).execute()

        # verifica se o id existe

        if not response.data:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        return{"status": "Atualizado com sucesso", "dados": response.data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))