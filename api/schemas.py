from pydantic import BaseModel, constr


class HeroBase(BaseModel):
    name: constr(min_length=1, max_length=50)
    power: constr(min_length=1, max_length=100)

class HeroCreate(HeroBase):
    pass

class Hero(HeroBase):
    id: int
    class Config:
           from_attributes = True 