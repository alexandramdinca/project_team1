from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Optional, List
import os

# ----- DATABASE SETUP -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "project.db")
DATABASE_URL = "sqlite:///" + DATABASE_FILE

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ----- MODELS -----
class Plants(Base):
    __tablename__ = 'Plants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    capacity = Column(Integer)

# ----- SCHEMAS -----
class PlantBase(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: Optional[int] = None

class PlantCreate(PlantBase):
    pass

class PlantUpdate(PlantBase):
    pass

class Plant(PlantBase):
    id: int

    class Config:
        orm_mode = True

# ----- CRUD -----
def get_all_plants(db: Session):
    return db.query(Plants).all()

def get_plant_by_id(db: Session, plant_id: int):
    return db.query(Plants).filter(Plants.id == plant_id).first()

def create_plant(db: Session, plant: PlantCreate):
    db_plant = Plants(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def update_plant(db: Session, plant_id: int, plant_data: PlantUpdate):
    plant = get_plant_by_id(db, plant_id)
    if not plant:
        return None
    for key, value in plant_data.dict(exclude_unset=True).items():
        setattr(plant, key, value)
    db.commit()
    db.refresh(plant)
    return plant

def delete_plant(db: Session, plant_id: int):
    plant = get_plant_by_id(db, plant_id)
    if not plant:
        return None
    db.delete(plant)
    db.commit()
    return plant

# ----- FASTAPI SETUP -----
app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- API ENDPOINTS -----

@app.post("/plants/", response_model=Plant)
def create_new_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    return create_plant(db, plant)

@app.get("/plants/", response_model=List[Plant])
def read_all_plants(db: Session = Depends(get_db)):
    return get_all_plants(db)

@app.get("/plants/{plant_id}", response_model=Plant)
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = get_plant_by_id(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.put("/plants/{plant_id}", response_model=Plant)
def update_existing_plant(plant_id: int, plant_data: PlantUpdate, db: Session = Depends(get_db)):
    plant = update_plant(db, plant_id, plant_data)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.delete("/plants/{plant_id}", response_model=Plant)
def delete_existing_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = delete_plant(db, plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant
