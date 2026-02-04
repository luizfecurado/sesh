from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import supabase 
from app.schemas import Entretenimento
from typing import Optional, List
import csv
import io
from fastapi.responses import StreamingResponse
app = FastAPI(title="Sesh API")

app.add_middleware(
    CORSMiddleware,       
    allow_origins=["*"],    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message": "Sesh está online!"}

#registro dos daddos com validação pydantic

@app.post("/registrar")
def registrar_entretenimento(item: Entretenimento):
    try:
        dados_para_banco = item.model_dump()

        response = supabase.table("entretenimento").insert(dados_para_banco).execute()

        return {"status": "Sucesso", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# leitura dos itens
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

#deletar itens
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



@app.get("/estatisticas")
def estatisticas():
    try:
        response = supabase.table("entretenimento").select("*").execute()
        dados = response.data

        total_itens = len(dados)

        if total_itens == 0:
            return{"mensagem": "Nenhum dado para analisar"}
        
        soma_notas = sum(item["nota"] for item in dados)
        media_geral = soma_notas/total_itens

        contagem_categorias = {}
        for item in dados:
            cat = item["categoria"]
            contagem_categorias[cat] = contagem_categorias.get(cat, 0) + 1 

        return {
            "total_consumido": total_itens,
            "nota_media_geral": round(media_geral, 2),
            "distribuicao_por_categoria": contagem_categorias 
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))