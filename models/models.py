from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

sql_url = "sqlite:///cafe.db"
engine = create_engine(sql_url)
Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_number = Column(Integer, nullable=False, unique=True)
    orders_placed = relationship('Order',
                                 back_populates="customer")

    def __repr__(self):
        return "<Customer(name='%s', contact_number='%s')>" % (
            self.name, self.contact_number)


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
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

    def __repr__(self):
        return "<Order(order_time='%s', status='%s'>" % (
            self.order_time, self.status)


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    contact_number = Column(Integer, nullable=False, unique=True)
    email = Column(String(64), nullable=True, unique=True)
    orders_served = relationship('Order',
                                 back_populates="employee")

    def __repr__(self):
        return "<Order(name='%s', contact_number='%s', email='%s')>" % (
            self.name, self.contact_number, self.email)


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    price = Column(String(32), nullable=False)
    ingredients = Column(String(64))

    def __repr__(self):
        return "<Order(name='%s', price='%s', ingredients='%s')>" % (
            self.name, self.price, self.ingredients)


class Payment(Base):
    __tablename__ = "payment"
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    employee_id = Column(Integer, ForeignKey('employee.id'))
    price = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Order(order_id='%s', price='%s')>" % (
            self.order_id, self.price)


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    customer_notes = Column(String(64), nullable=False)
    order = relationship('Order',
                         back_populates="items_ordered")

    def __repr__(self):
        return "<Order(order_id='%s', item_id='%s', quantity='%s', customer_notes='%s')>" % (
            self.order_id, self.item_id, self.quantity, self.customer_notes)


Base.metadata.create_all(engine)
