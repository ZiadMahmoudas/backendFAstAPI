from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, crud
from api.database import get_db

router = APIRouter(
    prefix="/heroes",
    tags=["heroes"]
)

@router.post("/", response_model=schemas.Hero)
async def create_hero(hero: schemas.HeroCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_hero(db, hero)

@router.get("/", response_model=list[schemas.Hero])
async def get_heroes( db: AsyncSession = Depends(get_db)):
    return await crud.get_heroes(db)

@router.get("/{hero_id}", response_model=schemas.Hero)
async def get_hero(hero_id: int, db: AsyncSession = Depends(get_db)):
    db_hero = await crud.get_hero(db, hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero

@router.put("/{hero_id}", response_model=schemas.Hero)
async def update_hero(hero_id: int, hero: schemas.HeroCreate, db: AsyncSession = Depends(get_db)):
    db_hero = await crud.update_hero(db, hero_id, hero)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero

@router.delete("/{hero_id}", response_model=schemas.Hero)
async def delete_hero(hero_id: int, db: AsyncSession = Depends(get_db)):
    db_hero = await crud.delete_hero(db, hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero
