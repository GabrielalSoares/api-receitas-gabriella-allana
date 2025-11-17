from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()

mapped@_as_dataclass(table_registry)
class User:
    __tablename__ = 'users'

 id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome_usuario: Mapped[str]= mapped_clumn(unique=True)
    senha: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column
    (init=False, server_default=func.now()
    )