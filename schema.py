from pydantic import BaseModel
from typing import List


class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Usuario(BaseModel):
    id: int
    nome_usuario: str
    email: str
    senha: str

class BaseUsuario(BaseModel):
    nome_usuario: str
    email: str
    senha: str

class UsuarioPublic(BseModel):
    id: int
    nome_usuario: str
    email: str

    