from pydantic import BaseModel, Field
from typing import Optional

class Entretenimento(BaseModel):

    titulo: str = Field(..., min_length=1, description="Nome do Jogo, Livro, Filme ou Desenho")
    categoria: str = Field(..., pattern="^(jogo|livro|filme|filme|desenho)$", description="Categorias aceitas")
    nota: float = Field(..., ge=0, le=10, description="Nota de 0.0 a 10.0")
    comentario: Optional[str] = Field(None, max_length=250)

    class Config:
        from_atributtes = True