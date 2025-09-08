from sqlalchemy.orm import Session
from sqlalchemy import select
import api.models as models
import api.schemas as schemas

def create_hero(db: Session, hero: schemas.HeroCreate):
    db_hero = models.Hero(name=hero.name, power=hero.power)
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero

def get_heroes(db: Session):
    result = db.execute(select(models.Hero))
    return result.scalars().all()

def get_hero(db: Session, hero_id: int):
    result = db.execute(select(models.Hero).filter(models.Hero.id == hero_id))
    return result.scalar_one_or_none()

def update_hero(db: Session, hero_id: int, hero: schemas.HeroCreate):
    db_hero = get_hero(db, hero_id)
    if db_hero:
        db_hero.name = hero.name
        db_hero.power = hero.power
        db.commit()
        db.refresh(db_hero)
        return db_hero
    return None

def delete_hero(db: Session, hero_id: int):
    db_hero = get_hero(db, hero_id)
    if db_hero:
        db.delete(db_hero)
        db.commit()
        return db_hero
    return None
