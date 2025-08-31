from pydantic import BaseModel

class AtletaBase(BaseModel):
    nome: str
    cpf: str
    centro_treinamento: str | None = None
    categoria: str | None = None

class AtletaCreate(AtletaBase):
    pass

class AtletaListResponse(BaseModel):
    nome: str
    centro_treinamento: str | None = None
    categoria: str | None = None

    class Config:
        orm_mode = True

class AtletaResponse(AtletaBase):
    id: int

    class Config:
        orm_mode = True
