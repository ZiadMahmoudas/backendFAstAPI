from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database import get_db
import api.schemas as schemas
import api.crud as crud

router = APIRouter(
    prefix="/heroes",
    tags=["heroes"]
)

@router.post("/", response_model=schemas.Hero)
def create_hero(hero: schemas.HeroCreate, db: Session = Depends(get_db)):
    return crud.create_hero(db, hero)

@router.get("/", response_model=list[schemas.Hero])
def get_heroes(db: Session = Depends(get_db)):
    return crud.get_heroes(db)

@router.get("/{hero_id}", response_model=schemas.Hero)
def get_hero(hero_id: int, db: Session = Depends(get_db)):
    db_hero = crud.get_hero(db, hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero

@router.put("/{hero_id}", response_model=schemas.Hero)
def update_hero(hero_id: int, hero: schemas.HeroCreate, db: Session = Depends(get_db)):
    db_hero = crud.update_hero(db, hero_id, hero)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero

@router.delete("/{hero_id}", response_model=schemas.Hero)
def delete_hero(hero_id: int, db: Session = Depends(get_db)):
    db_hero = crud.delete_hero(db, hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero
