from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, table_registry 

app = FastAPI(title='API de teste')

engine = create_engine("sqlite:///:memory:" , echo=False)

table_registry.metadata.create_all(engine)

with Session(engine) as session:
    allana = User(
        username="allana", password="senha123", email="allana@gmail.com"
    )
    session.add(allana)
    session.commit()
    session.refresh(allana)

print("DADOS DO USUÁRIO:", allana)
print("ID:", allana.id)
print("Criado em:", allana.created_at)