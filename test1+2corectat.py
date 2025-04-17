from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

DATABASE_URL = "sqlite:///project.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    products = relationship("Product", back_populates="plant")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    plant = relationship("Plant", back_populates="products")
    materials = relationship("Material", back_populates="product")
    orders = relationship("Order", back_populates="product")

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="materials")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="orders")

class Storage(Base):
    __tablename__ = "storage"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    capacity = Column(Integer)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/plants/")
def create_plant(name: str, location: str, db: Session = Depends(get_db)):
    plant = Plant(name=name, location=location)
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant

@app.get("/plants/")
def read_plants(db: Session = Depends(get_db)):
    return db.query(Plant).all()

@app.get("/plants/{plant_id}")
def read_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@app.put("/plants/{plant_id}")
def update_plant(plant_id: int, name: str, location: str, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    plant.name = name
    plant.location = location
    db.commit()
    return plant

@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    db.delete(plant)
    db.commit()
    return {"message": "Plant deleted successfully"}

@app.post("/products/")
def create_product(name: str, price: float, plant_id: int, db: Session = Depends(get_db)):
    product = Product(name=name, price=price, plant_id=plant_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, name: str, price: float, plant_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product.name = name
    product.price = price
    product.plant_id = plant_id
    db.commit()
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.post("/materials/")
def create_material(name: str, quantity: int, product_id: int, db: Session = Depends(get_db)):
    material = Material(name=name, quantity=quantity, product_id=product_id)
    db.add(material)
    db.commit()
    db.refresh(material)
    return material

@app.get("/materials/")
def read_materials(db: Session = Depends(get_db)):
    return db.query(Material).all()

@app.get("/materials/{material_id}")
def read_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@app.put("/materials/{material_id}")
def update_material(material_id: int, name: str, quantity: int, product_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    material.name = name
    material.quantity = quantity
    material.product_id = product_id
    db.commit()
    return material

@app.delete("/materials/{material_id}")
def delete_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()
    return {"message": "Material deleted successfully"}

@app.post("/orders/")
def create_order(quantity: int, product_id: int, db: Session = Depends(get_db)):
    order = Order(quantity=quantity, product_id=product_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@app.get("/orders/")
def read_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.get("/orders/{order_id}")
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}")
def update_order(order_id: int, quantity: int, product_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order.quantity = quantity
    order.product_id = product_id
    db.commit()
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}

@app.post("/storage/")
def create_storage(location: str, capacity: int, db: Session = Depends(get_db)):
    storage = Storage(location=location, capacity=capacity)
    db.add(storage)
    db.commit()
    db.refresh(storage)
    return storage

@app.get("/storage/")
def read_storage(db: Session = Depends(get_db)):
    return db.query(Storage).all()

@app.get("/storage/{storage_id}")
def read_single_storage(storage_id: int, db: Session = Depends(get_db)):
    storage = db.query(Storage).filter(Storage.id == storage_id).first()
    if storage is None:
        raise HTTPException(status_code=404, detail="Storage not found")
    return storage

@app.put("/storage/{storage_id}")
def update_storage(storage_id: int, location: str, capacity: int, db: Session = Depends(get_db)):
    storage = db.query(Storage).filter(Storage.id == storage_id).first()
    if storage is None:
        raise HTTPException(status_code=404, detail="Storage not found")
    storage.location = location
    storage.capacity = capacity
    db.commit()
    return storage

@app.delete("/storage/{storage_id}")
def delete_storage(storage_id: int, db: Session = Depends(get_db)):
    storage = db.query(Storage).filter(Storage.id == storage_id).first()
    if storage is None:
        raise HTTPException(status_code=404, detail="Storage not found")
    db.delete(storage)
    db.commit()
    return {"message": "Storage deleted successfully"}
