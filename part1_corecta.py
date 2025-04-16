import os
from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

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

# 🔧 Crearea bazei de date
try:
    Base.metadata.create_all(engine)
    print("Tabelele au fost create cu succes!")
except Exception as e:
    print(f"Eroare la crearea tabelelor: {e}")

# ✅ Popularea bazei de date
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
