from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import api.database as models
import api.schemas as schemas


async def create_hero(db: AsyncSession, hero: schemas.HeroCreate):
    db_hero = models.Hero(name=hero.name, power=hero.power)
    db.add(db_hero)
    await db.commit()
    await db.refresh(db_hero)
    return db_hero

async def get_heroes(db: AsyncSession):
    result = await db.execute(select(models.Hero))
    return result.scalars().all()

async def get_hero(db: AsyncSession, hero_id: int):
    result = await db.execute(select(models.Hero).filter(models.Hero.id == hero_id))
    return result.scalar_one_or_none()

async def update_hero(db: AsyncSession, hero_id: int, hero: schemas.HeroCreate):
    db_hero = await get_hero(db, hero_id)
    if db_hero:
        db_hero.name = hero.name
        db_hero.power = hero.power
        await db.commit()
        await db.refresh(db_hero)
        return db_hero
    return None

async def delete_hero(db: AsyncSession, hero_id: int):
    db_hero = await get_hero(db, hero_id)
    if db_hero:
        await db.delete(db_hero)
        await db.commit()
        return db_hero
    return None
