from pydantic import BaseModel, Field
from typing import Optional

#validacao dos dados 
#ge = greater ou equal | le = less or equal
# Field(...) campo é obrigatório
# Pattern expressao para determinar um intervalo entre palavras 
class Entretenimento(BaseModel):

    titulo: str = Field(..., min_length=1, description="Nome do Jogo, Livro, Filme ou Desenho")

    categoria: str = Field(..., pattern="^(jogo|livro|filme|filme|desenho)$", description="Categorias aceitas")

    status: str = Field("Planejando", pattern="^(Planejando[Em Andamento|Concluido|Abandonei])")
    nota: float = Field(..., ge=0, le=10, description="Nota de 0.0 a 10.0")

    comentario: Optional[str] = Field(None, max_length=250)
    imagem_url: Optional[str] = Field(None, description="URL da capa do item")
    class Config:
        from_atributes = True