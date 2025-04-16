import os
from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, Numeric, String, create_engine
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
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String, unique = True, nullable = False)
    location = Column(String)
    capacity = Column(Integer)
    plant_products = relationship("PlantProducts", back_populates="plants")
    plant_materials = relationship("PlantMaterials", back_populates="plants")

class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String, unique = True, nullable = False)
    description = Column(String, nullable = True)
    category = Column(String, nullable = False)
    price = Column(DECIMAL)
    plant_products = relationship("PlantProduct", back_populates="products")
    storage_products = relationship("StorageProducts", back_populates="products")
    product_materials = relationship("ProductMaterials", back_populates="products")
    order_products = relationship("OrderProducts", back_populates="products")

class Materials(Base):
    __tablename__ = 'Materials'
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String, unique = True, nullable = False)
    description = Column(String, nullable = True)
    unit = Column(String, nullable = True)
    cost = Column(DECIMAL)
    plant_materials = relationship("PlantMaterials", back_populates="materials")
    storage_materials = relationship("StorageMaterials", back_populates="materials")
    product_materials = relationship("ProductMaterials", back_populates="materials")

class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key = True, autoincrement = True)
    order_date = Column(DateTime, nullable = False)
    customer_name = Column(String, nullable = False)
    status = Column(String, nullable = False)
    order_products = relationship("OrderProducts", back_populates="orders")

class PlantsProducts(Base):
    __tablename__ = 'PlantsProducts'
    id = Column(Integer, primary_key = True, autoincrement = True)
    plant_id = Column(Integer, ForeignKey('Plants.id'))
    product_id = Column(Integer, ForeignKey('Products.id'))
    quantity = Column(DECIMAL)
    plants = relationship("Plants", back_populates="plants")
    products = relationship("Products", back_populates="products")

class ProductsMaterials(Base):
    __tablename__ = 'ProductsMaterials'
    id = Column(Integer, primary_key = True, autoincrement = True)
    product_id = Column(Integer,  ForeignKey('Products.id'))
    material_id = Column(Integer,  ForeignKey('Materials.id'))
    quantity = Column(DECIMAL)
    products = relationship("Products", back_populates="products")
    materials = relationship("Materials", back_populates="materials")


class PlantsMaterials(Base):
    __tablename__ = 'PlantsMaterias'
    id = Column(Integer, primary_key = True, autoincrement = True)
    plant_id = Column(Integer,  ForeignKey('Plants.id'))
    material_id = Column(Integer,  ForeignKey('Materials.id'))
    quantity = Column(DECIMAL)
    materials = relationship("Materials", back_populates="materials")
    plants = relationship("Plants", back_populates="plants")

class OrdersProducts(Base):
    __tablename__ = 'OrdersProducts'
    id = Column(Integer, primary_key = True, autoincrement = True)
    order_id = Column(Integer,  ForeignKey('Orders.id'))
    product_id = Column(Integer,  ForeignKey('Products.id'))
    quantity = Column(Integer)
    products = relationship("Products", back_populates="products")
    orders = relationship("Orders", back_populates="orders")

class StorageProducts(Base):
    __tablename__ = 'StorageProducts'
    id = Column(Integer, primary_key = True, autoincrement = True)
    product_id = Column(Integer,  ForeignKey('Products.id'))
    quantity = Column(Integer)
    products = relationship("Products", back_populates="products")
    storage = relationship("Storage", back_populates="storage")

class StorageMaterials(Base):
    __tablename__ = 'StorageMaterials'
    id = Column(Integer, primary_key = True, autoincrement = True)
    material_id = Column(Integer,  ForeignKey('Materials.id'))
    quantity = Column(Integer)
    storage = relationship("Storage", back_populates="storage")
    materials =  relationship("Materials", back_populates="materials")