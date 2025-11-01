from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from schema import CreateReceita, Receita, Usuario, BaseUsuario, UsuarioPublic


app = FastAPI(title='API da Allana e Gabriela')


receitas: List[Receita] = []
usuarios: List[Usuario] = []


proximo_id = 0
proximo_id_usuario = 0


@app.get("/")
def hello():
    return {"title": "Livro de receitas"}


# Rotas de Receitas (Mantidas)
@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas

@app.get("/receitas/{receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita(receita: str):
    for r in receitas:
        if r.nome.lower() == receita.lower():
            return r
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.get("/receitas/id/{id}" , response_model=Receita, status_code=HTTPStatus.OK)
def get_receitas(id: int):
    for r in receitas:
        if r.id == id:
            return r
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.OK)
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


@app.put("/receitas/{id}" , response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            for r in receitas:
                if r.nome.lower() == dados.nome.lower() and r.id != id: # Corrigido: verifica se o nome é o mesmo, mas o ID é diferente
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




def get_usuario_by_email(email: str) -> Usuario | None:
    for u in usuarios:
        if u.email.lower() == email.lower():
            return u
    return None

def get_usuario_by_id(id: int) -> Usuario | None:
    for u in usuarios:
        if u.id == id:
            return u
    return None

def get_usuario_by_nome(nome_usuario: str) -> Usuario | None:
    for u in usuarios:
        if u.nome_usuario.lower() == nome_usuario.lower():
            return u
    return None


@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario):
    global proximo_id_usuario

    
    if get_usuario_email(dados.email):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe um usuário com este email.")

    
    if not any(char.isalpha() for char in dados.senha) or not any(char.isdigit() for char in dados.senha):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A senha deve conter letras e números.")

    proximo_id_usuario += 1
    novo_usuario = Usuario(
        id=proximo_id_usuario,
        nome_usuario=dados.nome_usuario,
        email=dados.email,
        senha=dados.senha 
    )

    usuarios.append(novo_usuario)
    return novo_usuario


@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios():
    return usuarios


@app.get("/usuarios/{nome_usuario}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuario_por_nome(nome_usuario: str):
    usuario = get_usuario_nome(nome_usuario)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
    return usuario


@app.get("/usuarios/id/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuario_por_id(id: int):
    usuario = get_usuario_id(id)
    if not usuario:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")
    return usuario


@app.put("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def update_usuario(id: int, dados: BaseUsuario):
    usuario_exist = get_usuario_id(id)
    if not usuario_exist:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")

    
    usuario_mesmo_email = get_usuario_email(dados.email)
    if usuario_mesmo_email and usuario_mesmo_email.id != id:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Já existe outro usuário com este email.")

    
    if not any(char.isalpha() for char in dados.senha) or not any(char.isdigit() for char in dados.senha):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A senha deve conter letras e números.")

    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            usuario_atualizado = Usuario(
                id=id,
                nome_usuario=dados.nome_usuario,
                email=dados.email,
                senha=dados.senha
            )
            usuarios[i] = usuario_atualizado
            return usuario_atualizado
    
    
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Erro ao atualizar usuário.")


@app.delete("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def delete_usuario(id: int):
    usuario_a_deletar = get_usuario_by_id(id)
    if not usuario_a_deletar:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")

    for i in range(len(usuarios)):
        if usuarios[i].id == id:
            return usuarios.pop(i)
    
    
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Erro ao deletar usuário.")
