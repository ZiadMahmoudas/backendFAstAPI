from sqlalchemy.orm import Session
import crud, schemas

def create_new_hero(db: Session, hero: schemas.HeroCreate):
    if not hero.name or not hero.power:
        raise ValueError("Hero name and power must not be empty")
    return crud.create_hero(db, hero)

def list_heroes(db: Session):
    return crud.get_heroes(db)
