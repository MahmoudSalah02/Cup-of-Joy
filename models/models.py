from datetime import datetime
from datetime import timedelta

from bcrypt import hashpw, checkpw, gensalt
from jwt import encode, decode
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# TODO: error when you this file is imported from inside /seeds/
PRIVATE_KEY = open('jwt-key').read()
PUBLIC_KEY = open('jwt-key.pub').read()
ALGORITHM = "RS256"

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
    username = Column(String(64), unique=True)
    role = Column(String(64))
    password = Column(LargeBinary)

    def __repr__(self):
        """

        :return:
        """
        return "<Order(name='%s', contact_number='%s', email='%s')>" % (
            self.name, self.contact_number, self.email)

    def set_username(self, username):
        """
        This function sets the username of an employee
        :return:
        """
        self.username = username

    def set_hash_password(self, new_password):
        """
        This function takes a string representing the new password and
        stores it in the db hashed
        :param new_password: string representing the new password
        :return: true if the operation is successful
        """
        new_password_as_bytes = str.encode(new_password)
        hashed_password = hashpw(new_password_as_bytes, gensalt())
        self.password = hashed_password

    def check_password(self, unchecked_password):
        """
        This function returns true if the input password is equal to the password
        stores in the db, false otherwise
        :param unchecked_password: string representing the password to be checked
        :return: True if the unchecked password matches the password in the db, False otherwise
        """
        unchecked_password_as_bytes = str.encode(unchecked_password)
        return checkpw(unchecked_password_as_bytes, self.password)

    def encode_access_token(self):
        """
        This function creates and returns an encoded access token
        :return: string representing an encoded access token
        """
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "sub": self.id,
            "username": self.username,
            "role": self.role,
        }
        return encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(access_token):
        """

        :param access_token:
        :return:
        """
        return decode(access_token, PUBLIC_KEY, algorithms=ALGORITHM)


class Item(Base):
    __tablename__ = "item"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    price = Column(String(32), nullable=False)
    ingredients = Column(String(64))
    item_ordered = relationship('OrderItem',
                                back_populates="item_details")

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
    item_details = relationship('Item',
                                back_populates="item_ordered")

    def __repr__(self):
        return "<Order(order_id='%s', item_id='%s', quantity='%s', customer_notes='%s')>" % (
            self.order_id, self.item_id, self.quantity, self.customer_notes)
