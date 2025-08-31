from fastapi import FastAPI, Depends, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from database import SessionLocal, engine, Base
from models import Atleta
from schemas import AtletaCreate, AtletaResponse, AtletaListResponse


Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Atletas")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/atletas", response_model=Page[AtletaListResponse])
async def get_all_atletas(
    nome: str | None = None, cpf: str | None = None, db: Session = Depends(get_db)
):
    query = db.query(Atleta).order_by(Atleta.id)

    if nome:
        query = query.filter(Atleta.nome.ilike(f"%{nome}%"))

    if cpf:
        query = query.filter(Atleta.cpf == cpf)

    return paginate(query.all())


@app.get("/atletas/{atleta_id}", response_model=AtletaResponse)
async def get_atleta(atleta_id: int, db: Session = Depends(get_db)):
    atleta = db.query(Atleta).filter(Atleta.id == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    return atleta


@app.post("/atletas", response_model=AtletaResponse)
async def create_atleta(atleta: AtletaCreate, db: Session = Depends(get_db)):
    novo_atleta = Atleta(**atleta.dict())
    db.add(novo_atleta)
    try:
        db.commit()
        db.refresh(novo_atleta)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}",
        )
    return novo_atleta


@app.put("/atletas/{atleta_id}", response_model=AtletaResponse)
async def update_atleta(
    atleta_id: int, atleta: AtletaCreate, db: Session = Depends(get_db)
):
    db_atleta = db.query(Atleta).filter(Atleta.id == atleta_id).first()
    if not db_atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")

    for key, value in atleta.dict().items():
        setattr(db_atleta, key, value)

    try:
        db.commit()
        db.refresh(db_atleta)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=303,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}",
        )

    return db_atleta


@app.delete("/atletas/{atleta_id}")
async def delete_atleta(atleta_id: int, db: Session = Depends(get_db)):
    atleta = db.query(Atleta).filter(Atleta.id == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    db.delete(atleta)
    db.commit()
    return {"message": f"Atleta {atleta_id} deletado com sucesso"}


add_pagination(app)
