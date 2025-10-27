from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from schema import CreateReceita, Receita

app = FastAPI(title='API da Allana e Gabriela')


receitas: List[Receita] = []

proximo_id = 0


@app.get("/")
def hello():
    return {"title": "Livro de receitas"}


@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas
    
@app.get("/receitas/{receita}", response_model=Receita, status_code=HTTPStatus.Ok)
def get_receita(receita: str):
    for r in receitas:
        if r.nome.lower() == receita.lower():
            return r
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.get("/receitas/id/{id}" , response_model=Receita, status_code=HTTPStatus.Ok)
def get_receitas(id: int):
    for r in receitas:
        if r.id == id:
            return r
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.Ok)
def create_receita(dados: CreateReceita):
    global proximo_id

    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
             raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome")


    if not (1 <= len(dados.ingredientes) <= 20):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter de 1 a 20 ingredientes")

    if not (2 <= len(dados.nome) <= 50):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter de 2 a 50 caracteres")

    proximo_id += 1
    nova_receita = Receita(
        id=proximo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )

    receitas.append(nova_receita)
    return nova_receita


@app.put("/receitas/{id}" , response_model=Receita, status_code=HTTPStatus.Ok)
def update_receita(id: int, dados: CreateReceita):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            for r in receitas:
                if r.nome.lower() == dados.nome.lower():
                    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome")
                    
            if dados.nome == "":
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="O nome não pode estar vazio")

            if not (1 <= len(dados.ingredientes) <= 20):
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter de 1 a 20 ingredientes")

            if not (2 <= len(dados.nome) <= 50):
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter de 2 a 50 caracteres")


            receita_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo
            )
            receitas[i] = receita_atualizada
            return receita_atualizada

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.delete("/receitas/{id}" , response_model=Receita, status_code=HTTPStatus.Ok)
def deletar_receita(id: int):
    if not receitas:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Não existe receita para apagar")

    for i in range(len(receitas)):
        if receitas[i].id == id:
            rct = receitas[i].nome
            receitas.pop(i)
            return {"mensagem":f"Receita {rct} deletada"}

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")
