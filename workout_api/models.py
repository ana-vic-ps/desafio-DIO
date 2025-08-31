from sqlalchemy import Column, Integer, String
from database import Base

class Atleta(Base):
    __tablename__ = "atletas"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    centro_treinamento = Column(String(255), nullable=True)
    categoria = Column(String(255), nullable=True)
