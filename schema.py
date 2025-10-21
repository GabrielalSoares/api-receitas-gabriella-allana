from pydantic import BaseModel
from typing import list


class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

    class Receita(BaseModel):
        id: int
        nome: str
        ingredientes: List[str]
        modo_de_preparo: str
