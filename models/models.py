from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from bcrypt import hashpw, checkpw, gensalt
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from config.config import *

PUBLIC_KEY = "secret"
ALGORITHM = "HS256"
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
    password = Column(String(64))

    def __repr__(self):
        """

        :return:
        """
        return "<Order(name='%s', contact_number='%s', email='%s')>" % (
            self.name, self.contact_number, self.email)

    # TODO: do I need a whole method for this??
    def set_username(self, username):
        """
        This function sets the username of an employee
        :return:
        """
        self.username = username

    # TODO: is there a @setter thingy?
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

        # TODO: should I return true or None?
        return True

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
            "username": self.username,
            "iat": datetime.now(),
            "role": self.role
        }
        return encode(payload, PUBLIC_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(access_token):
        """

        :param access_token:
        :return:
        """

        payload = decode(access_token, PUBLIC_KEY, algorithms=ALGORITHM)
        return {
            "username": payload.get("username"),
            "iat": datetime.now(),
            "role": payload.get("role"),
            "access_token": access_token
        }

        # TODO: should I create exceptions like this:
        # try:
        # except ExpiredSignatureError:
        #     error = "Access token expired. Please log in again."
        #     return {"error": error}
        # except InvalidTokenError:
        #     error = "Invalid token. Please log in again."
        #     return {"error": error}

    @staticmethod
    def find_by_username(username):
        """
        This function finds the user with a matching username
        :param username: username of the user to find
        :return: user with matching username
        """
        return session.query(Employee).filter(Employee.username == username).one_or_none()


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


Base.metadata.create_all(engine)
