import os
from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "project.db")
DATABASE_URL = "sqlite:///" + DATABASE_FILE
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Plants(Base):
    __tablename__ = 'Plants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)
    capacity = Column(Integer)
    plants_products = relationship("PlantsProducts", back_populates="plants")
    plants_materials = relationship("PlantsMaterials", back_populates="plants")

class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    price = Column(DECIMAL)
    plants_products = relationship("PlantsProducts", back_populates="products")
    storage_products = relationship("StorageProducts", back_populates="products")
    products_materials = relationship("ProductsMaterials", back_populates="products")
    orders_products = relationship("OrdersProducts", back_populates="products")

class Materials(Base):
    __tablename__ = 'Materials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    cost = Column(DECIMAL)
    plants_materials = relationship("PlantsMaterials", back_populates="materials")
    storage_materials = relationship("StorageMaterials", back_populates="materials")
    products_materials = relationship("ProductsMaterials", back_populates="materials")

class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, nullable=False)
    customer_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    orders_products = relationship("OrdersProducts", back_populates="orders")

class PlantsProducts(Base):
    __tablename__ = 'PlantsProducts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('Plants.id'))
    product_id = Column(Integer, ForeignKey('Products.id'))
    quantity = Column(DECIMAL)
    plants = relationship("Plants", back_populates="plants_products")
    products = relationship("Products", back_populates="plants_products")

class ProductsMaterials(Base):
    __tablename__ = 'ProductsMaterials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Products.id'))
    material_id = Column(Integer, ForeignKey('Materials.id'))
    quantity = Column(DECIMAL)
    products = relationship("Products", back_populates="products_materials")
    materials = relationship("Materials", back_populates="products_materials")

class PlantsMaterials(Base):
    __tablename__ = 'PlantsMaterials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    plant_id = Column(Integer, ForeignKey('Plants.id'))
    material_id = Column(Integer, ForeignKey('Materials.id'))
    quantity = Column(DECIMAL)
    materials = relationship("Materials", back_populates="plants_materials")
    plants = relationship("Plants", back_populates="plants_materials")

class OrdersProducts(Base):
    __tablename__ = 'OrdersProducts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Orders.id'))
    product_id = Column(Integer, ForeignKey('Products.id'))
    quantity = Column(Integer)
    products = relationship("Products", back_populates="orders_products")
    orders = relationship("Orders", back_populates="orders_products")

class StorageProducts(Base):
    __tablename__ = 'StorageProducts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Products.id'))
    quantity = Column(Integer)
    products = relationship("Products", back_populates="storage_products")

class StorageMaterials(Base):
    __tablename__ = 'StorageMaterials'
    id = Column(Integer, primary_key=True, autoincrement=True)
    material_id = Column(Integer, ForeignKey('Materials.id'))
    quantity = Column(Integer)
    materials = relationship("Materials", back_populates="storage_materials")

try:
    Base.metadata.create_all(engine)
    print("Tabelele au fost create cu succes!")
except Exception as e:
    print(f"Eroare la crearea tabelelor: {e}")

Session = sessionmaker(bind=engine)
session = Session()

plants = [
    Plants(name='Green Valley Plant', location='Springfield, IL', capacity=1000),
    Plants(name='Herbal Remedies Factory', location='Madison, WI', capacity=1500),
    Plants(name='Natural Extracts Co.', location='Boulder, CO', capacity=2000),
    Plants(name='Pure Essence Plants', location='Austin, TX', capacity=1200),
    Plants(name='Botanical Ingredients Inc.', location='Seattle, WA', capacity=1800),
]
session.add_all(plants)

products = [
    Products(name='Herbal Tea', description='A soothing herbal tea blend.', category='Beverage', price=5.99),
    Products(name='Natural Shampoo', description='Shampoo made from natural ingredients.', category='Cosmetics', price=12.99),
    Products(name='Essential Oil', description='Pure essential oil for aromatherapy.', category='Aromatherapy', price=15.99),
    Products(name='Herbal Extract', description='Concentrated herbal extract for health benefits.', category='Supplements', price=20.99),
    Products(name='Organic Soap', description='Handmade organic soap with natural ingredients.', category='Cosmetics', price=7.49),
]
session.add_all(products)

plants_products = [
    PlantsProducts(plant_id=1, product_id=1, quantity=200),
    PlantsProducts(plant_id=1, product_id=2, quantity=150),
    PlantsProducts(plant_id=2, product_id=3, quantity=300),
    PlantsProducts(plant_id=3, product_id=4, quantity=100),
    PlantsProducts(plant_id=4, product_id=5, quantity=250),
]
session.add_all(plants_products)

materials = [
    Materials(name='Chamomile', description='Dried chamomile flowers.', unit='grams', cost=2.50),
    Materials(name='Lavender', description='Dried lavender flowers.', unit='grams', cost=3.00),
    Materials(name='Coconut Oil', description='Organic coconut oil.', unit='liters', cost=10.00),
    Materials(name='Aloe Vera', description='Fresh aloe vera gel.', unit='liters', cost=8.00),
    Materials(name='Olive Oil', description='Extra virgin olive oil.', unit='liters', cost=12.00),
]
session.add_all(materials)

products_materials = [
    ProductsMaterials(product_id=1, material_id=1, quantity=50),
    ProductsMaterials(product_id=2, material_id=3, quantity=30),
    ProductsMaterials(product_id=3, material_id=2, quantity=20),
    ProductsMaterials(product_id=4, material_id=4, quantity=25),
    ProductsMaterials(product_id=5, material_id=5, quantity=10),
]
session.add_all(products_materials)

plants_materials = [
    PlantsMaterials(plant_id=1, material_id=1, quantity=100),
    PlantsMaterials(plant_id=2, material_id=2, quantity=80),
    PlantsMaterials(plant_id=3, material_id=3, quantity=150),
    PlantsMaterials(plant_id=4, material_id=4, quantity=90),
    PlantsMaterials(plant_id=5, material_id=5, quantity=120),
]
session.add_all(plants_materials)

storage_products = [
    StorageProducts(product_id=1, quantity=500),
    StorageProducts(product_id=2, quantity=300),
    StorageProducts(product_id=3, quantity=400),
    StorageProducts(product_id=4, quantity=200),
    StorageProducts(product_id=5, quantity=600),
]
session.add_all(storage_products)

storage_materials = [
    StorageMaterials(material_id=1, quantity=150),
    StorageMaterials(material_id=2, quantity=100),
    StorageMaterials(material_id=3, quantity=200),
    StorageMaterials(material_id=4, quantity=180),
    StorageMaterials(material_id=5, quantity=220),
]
session.add_all(storage_materials)

orders = [
    Orders(order_date=datetime(2023, 1, 15), customer_name='Alice Johnson', status='Completed'),
    Orders(order_date=datetime(2023, 2, 20), customer_name='Bob Smith', status='Pending'),
    Orders(order_date=datetime(2023, 3, 5), customer_name='Charlie Brown', status='Shipped'),
    Orders(order_date=datetime(2023, 4, 10), customer_name='Diana Prince', status='Completed'),
    Orders(order_date=datetime(2023, 5, 25), customer_name='Ethan Hunt', status='Cancelled'),
]
session.add_all(orders)

orders_products = [
    OrdersProducts(order_id=1, product_id=1, quantity=2),
    OrdersProducts(order_id=1, product_id=3, quantity=1),
    OrdersProducts(order_id=2, product_id=2, quantity=3),
    OrdersProducts(order_id=3, product_id=4, quantity=2),
    OrdersProducts(order_id=4, product_id=5, quantity=5),
]
session.add_all(orders_products)

session.commit()
session.close()


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
