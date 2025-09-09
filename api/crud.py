from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import api.database as models
import api.schemas as schemas
import logging
from fastapi import HTTPException

# إعداد السجلات (logs)
logging.basicConfig(level=logging.DEBUG)

# دالة CRUD لإنشاء بطل (hero)
async def create_hero(db: AsyncSession, hero: schemas.HeroCreate):
    try:
        db_hero = models.Hero(name=hero.name, power=hero.power)
        db.add(db_hero)
        await db.commit()
        await db.refresh(db_hero)
        return db_hero
    except Exception as e:
        logging.error(f"Error creating hero: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# دالة CRUD للحصول على كل الأبطال
async def get_heroes(db: AsyncSession):
    try:
        result = await db.execute(select(models.Hero))
        return result.scalars().all()
    except Exception as e:
        logging.error(f"Error getting heroes: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# دالة CRUD للحصول على بطل بناءً على ID
async def get_hero(db: AsyncSession, hero_id: int):
    try:
        result = await db.execute(select(models.Hero).filter(models.Hero.id == hero_id))
        return result.scalar_one_or_none()
    except Exception as e:
        logging.error(f"Error getting hero with id {hero_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# دالة CRUD لتحديث بطل بناءً على ID
async def update_hero(db: AsyncSession, hero_id: int, hero: schemas.HeroCreate):
    try:
        db_hero = await get_hero(db, hero_id)
        if db_hero:
            db_hero.name = hero.name
            db_hero.power = hero.power
            await db.commit()
            await db.refresh(db_hero)
            return db_hero
        raise HTTPException(status_code=404, detail="Hero not found")
    except Exception as e:
        logging.error(f"Error updating hero with id {hero_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# دالة CRUD لحذف بطل بناءً على ID
async def delete_hero(db: AsyncSession, hero_id: int):
    try:
        db_hero = await get_hero(db, hero_id)
        if db_hero:
            await db.delete(db_hero)
            await db.commit()
            return db_hero
        raise HTTPException(status_code=404, detail="Hero not found")
    except Exception as e:
        logging.error(f"Error deleting hero with id {hero_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
