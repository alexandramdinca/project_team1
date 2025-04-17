from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PlantBase(BaseModel):
    name: str
    location: Optional[str] = None
    capacity: Optional[int] = None

class PlantCreate(PlantBase):
    pass

class PlantRead(PlantBase):
    id: int

    class Config:
        orm_mode = True

class PlantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None

app = FastAPI()

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

from fastapi import FastAPI, Depends, HTTPException

@app.post("/plants/", response_model=PlantRead)
def create_plant(plant: PlantCreate, db: Session = Depends(get_db)):
    new_plant = Plants(**plant.dict())
    db.add(new_plant)
    db.commit()
    db.refresh(new_plant)
    return new_plant

@app.get("/plants/", response_model=List[PlantRead])
def get_plants(db: Session = Depends(get_db)):
    return db.query(Plants).all()

@app.get("/plants/{plant_id}", response_model=PlantRead)
def get_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plants).get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.put("/plants/{plant_id}", response_model=PlantRead)
def update_plant(plant_id: int, plant_update: PlantUpdate, db: Session = Depends(get_db)):
    plant = db.query(Plants).get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    for key, value in plant_update.dict(exclude_unset=True).items():
        setattr(plant, key, value)
    db.commit()
    db.refresh(plant)
    return plant

@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plants).get(plant_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"detail": "Plant deleted successfully"}

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None

@app.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Products(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/", response_model=List[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return db.query(Products).all()

@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Products).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_update.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

class MaterialBase(BaseModel):
    name: str
    description: Optional[str] = None
    unit: Optional[str] = None
    cost: float

class MaterialCreate(MaterialBase):
    pass

class MaterialRead(MaterialBase):
    id: int

    class Config:
        orm_mode = True

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    cost: Optional[float] = None

@app.post("/materials/", response_model=MaterialRead)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    new_material = Materials(**material.dict())
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    return new_material

@app.get("/materials/", response_model=List[MaterialRead])
def get_materials(db: Session = Depends(get_db)):
    return db.query(Materials).all()

@app.get("/materials/{material_id}", response_model=MaterialRead)
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Materials).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@app.put("/materials/{material_id}", response_model=MaterialRead)
def update_material(material_id: int, material_update: MaterialUpdate, db: Session = Depends(get_db)):
    material = db.query(Materials).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    for key, value in material_update.dict(exclude_unset=True).items():
        setattr(material, key, value)
    db.commit()
    db.refresh(material)
    return material

@app.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Materials).get(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()
    return {"detail": "Material deleted successfully"}

class OrderBase(BaseModel):
    order_date: datetime
    customer_name: str
    status: str

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int

    class Config:
        orm_mode = True

class OrderUpdate(BaseModel):
    order_date: Optional[datetime] = None
    customer_name: Optional[str] = None
    status: Optional[str] = None

@app.post("/orders/", response_model=OrderRead)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Orders(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/orders/", response_model=List[OrderRead])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Orders).all()

@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Orders).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=OrderRead)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Orders).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Orders).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}
