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


    
@app.get("/")
def hello():
    return{"title":"Livro de receitas"}

@app.get("/receitas/{receita}")
def get_receita(receita:str):
    for r in receitas:
        if r["nome"].lower() == receita.lower():
            return r
    return {"error": "Receita não encontrada"}



@app.get("/receitas")
def get_todas_receitas():
    return receitas

@app.post("/receitas", response_model=Receita, status_code=201)
def create_receita(dados: CreateReceita):
    global proximo_id

    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=400,detail="Já existe uma receita com esse nome")

    nova_receita=Receita(id = proximo_id , nome = dados.nome, ingredientes= dados.ingredientes, modo_de_preparo= dados.modo_de_preparo)
    
    receitas.append(nova_receita)
    proximo_id+= 1

    return nova_receita
    
@app.get("/receitas/id/{id}")
def get_receitas(id: int):
    for r in receitas:
        if r.id == id:
            return r
        raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.put("/receitas/{id}",response_model=Receita)
def update_receita(id: int, dados: CreateReceita):

    for i in range(len(receitas)):

        if receitas[i].id == id:
            receitas_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo,
            )
            for j in range(len(receitas)):
                if receitas[j].nome==receitas_atualizada.nome:
                    return {"mensagem":"receita já existe"}
            if receitas_atualizada.nome=="":
                return{"digite algo"}
                
            receitas[i] = (receitas_atualizada)
            return receitas_atualizada
            raise HTTPException(status_code=404, detail= "Receita não encontrada")

@app.delete("/receitas/{ìd}")
def deletar_receita(id: int):

    for i in range(len(receitas)):
        if receitas == "":
            return{"não existe receita para apagar"}
           
        if receitas[i].id == id:
            rct=receitas[i].nome
            receitas.pop(i)
            return {"mensagem": "Receita "+rct+" deletada"}
    
    return {"mensagem": "Receita não encontrada"}

      