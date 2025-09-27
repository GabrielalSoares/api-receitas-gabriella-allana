from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title='API da Allana e Gabriela')


class Receita(BaseModel) :
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class CreateReceita(BaseModel) :
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

receitas: List[Receita] = []
proximo_id = 0

    
@app.get("/")
def hello():
    return{"title":"Livro de receitas"}

@app.get("/receitas")
def get_todas_receitas():
    return receitas

@app.get("/receitas/{receita}")
def get_receita(receita:str):
    for r in receitas:
        if r["nome"].lower() == receita.lower():
            return r
    return {"error": "Receita não encontrada"}

@app.get("/receitas/id/{id}")
def get_receitas(id: int):
    for r in receitas:
        if r.id == id:
            return r
        return {"mensagem": "Receita não encontrada"}

@app.post("/receitas")
def create_receita(dados: CreateReceita):
    global proximo_id

    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
            return {"mensagem":"Já existe uma receita com esse nome"}

         if not (1 <= len(dados.ingredientes) <= 20):
            return {"mensagem": "A receita deve ter de 1 a 20 ingredientes"}

         if not (2 <= len(dados.nome) <= 50):
            return {"mensagem": "O nome da receita deve ter de 2 a 50 caracteres"}

    proximo_id+= 1
    nova_receita=Receita(id = proximo_id , nome = dados.nome, ingredientes= dados.ingredientes, modo_de_preparo= dados.modo_de_preparo)
    
    receitas.append(nova_receita)
    return nova_receita


@app.put("/receitas/{id}")
def update_receita(id: int, dados: CreateReceita):

    for i in range(len(receitas)):
        if receitas[i].id == id:
           for r in receitas:
             if r.nome.lower() == dados.nome.lower():
                    return {"mensagem": "Já existe uma receita com esse nome"}
                
             if r.nome == "":
                    return {"mensagem": "O nome não pode estar vazio"}

             if not (1 <= len(dados.ingredientes) <= 20):
                return {"mensagem": "A receita deve ter entre 1 e 20 ingredientes"}
            
             if not (2 <= len(dados.nome) <= 50):
                return {"mensagem": "O nome da receita deve ter entre 2 e 50 caracteres"}

            receitas_atualizada = Receita( id=id, nome=dados.nome, ingredientes=dados.ingredientes, modo_de_preparo=dados.modo_de_preparo)
            receitas[i]= receitas_atualizada
            return receitas_atualizada
          
      return {"mensagem":"Receita não encontrada"}
            

@app.delete("/receitas/{id}")
def deletar_receita(id: int):

    for i in range(len(receitas)):
        if receitas == "":
            return{"não existe receita para apagar"}
           
        if receitas[i].id == id:
            rct=receitas[i].nome
            receitas.pop(i)
            return {"mensagem": "Receita "+rct+" deletada"}
    
    return {"mensagem": "Receita não encontrada"}

      