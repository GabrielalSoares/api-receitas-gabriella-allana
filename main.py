from datetime import datetime
from http import HTTPStatus
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from schema import CreateReceita, Receita, BaseUsuario, UsuarioPublic
from config import settings
from models import User
from database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError 


app = FastAPI(title='API de receitas')


receitas: List[Receita] = []
proximo_id = 0

@app.get("/", status_code=HTTPStatus.OK)
def hello():
    return {"title": "Livro de receitas"}

@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas

@app.get("/receitas/{receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita(receita: str):
    for r in receitas:
        if r.nome.lower() == receita.lower():
            return r
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.get("/receitas/id/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receitas_por_id(id: int):
    for r in receitas:
        if r.id == id:
            return r
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
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

@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            
            for r in receitas:
                if r.nome.lower() == dados.nome.lower() and r.id != id:
                    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe uma receita com esse nome")
                    
            if dados.nome == "":
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome não pode estar vazio")

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

@app.delete("/receitas/{id}", status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    if not receitas:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Não existe receita para apagar")

    for i in range(len(receitas)):
        if receitas[i].id == id:
            rct_nome = receitas[i].nome
            receitas.pop(i)
            return {"mensagem": f"Receita {rct_nome} deletada"}
            
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")



@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.nome_usuario == dados.nome_usuario) | (User.email == dados.email)
        )
    ) 

    if db_user:
        if db_user.nome_usuario == dados.nome_usuario:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuário já existe',
            ) # [cite: 92-95]
        elif db_user.email == dados.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email já existe',
            ) 
        
    
    db_user = User(
        nome_usuario=dados.nome_usuario, 
        senha=dados.senha, 
        email=dados.email
    ) 

    session.add(db_user)
    session.commit()
    session.refresh(db_user) 

    return db_user

@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users 

@app.get("/usuarios/{nome_usuario}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuario_por_nome(nome_usuario: str, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.nome_usuario == nome_usuario)
    )
    if db_user:
        return db_user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado") 

@app.get("/usuarios/id/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuario_por_id(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == id)
    )
    if db_user:
        return db_user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado") 

@app.put("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def update_usuario(id: int, dados: BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))
    
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado"
        )
    
    try:
        db_user.nome_usuario = dados.nome_usuario
        db_user.senha = dados.senha
        db_user.email = dados.email
        session.commit()
        session.refresh(db_user)
        return db_user
        
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nome de usuário ou Email já existe'
        ) 

@app.delete("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def delete_usuario(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="Usuário não encontrado"
        )

    session.delete(db_user)
    session.commit()

    return db_user 