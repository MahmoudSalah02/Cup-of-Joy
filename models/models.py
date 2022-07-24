from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from datetime import datetime

engine = create_engine(r"sqlite:///C:\Users\mahmo\PycharmProjects\coffeeShop\cafe.db")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_number = Column(Integer, nullable=False, unique=True)
    orders_placed = relationship('Order',
                                 back_populates="customer",
                                 cascade="all, delete, delete-orphan",
                                 single_parent=True)


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    order_time = Column(DateTime,
                        default=datetime.utcnow,
                        onupdate=datetime.utcnow,
                        nullable=False)
    status = Column(String(32), nullable=False)
    customer = relationship('Customer',
                            back_populates="orders_placed",
                            foreign_keys=[customer_id])
    employee = relationship('Employee',
                            back_populates="orders_served",
                            foreign_keys=[employee_id])
    items_ordered = relationship('OrderItem',
                                 back_populates="order",
                                 cascade="all, delete, delete-orphan",
                                 single_parent=True)


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    contact_number = Column(Integer, nullable=False, unique=True)
    email = Column(String(64), nullable=True, unique=True)
    orders_served = relationship('Order',
                                 back_populates="employee",
                                 cascade="all, delete, delete-orphan",
                                 single_parent=True)


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    price = Column(String(32), nullable=False)
    ingredients = Column(String(64), nullable=False)


class Payment(Base):
    __tablename__ = "payment"
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    price = Column(Integer, nullable=False)


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    customer_notes = Column(String(64), nullable=False)
    order = relationship('Order',
                         back_populates="items_ordered")

# Base.metadata.create_all(engine)
