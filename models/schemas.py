from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema, auto_field, fields
from models.models import *


class OrderItemSchema(SQLAlchemySchema):
    class Meta:
        model = OrderItem
        include_fk = True
        load_instance = True
        include_relationships = True

    id = auto_field()
    order_id = auto_field()
    item_id = auto_field()
    quantity = auto_field()
    customer_notes = auto_field()
    order = auto_field()


class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        include_fk = True
        load_instance = True
        include_relationships = True

    id = auto_field()
    customer_id = auto_field()
    employee_id = auto_field()
    order_time = auto_field()
    status = auto_field()
    items_ordered = fields.Nested(OrderItemSchema(only=("item_id", "quantity", "customer_notes"), many=True), many=True)


class CustomerSchema(SQLAlchemySchema):
    class Meta:
        model = Customer
        include_fk = True
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    contact_number = auto_field()


class EmployeeSchema(SQLAlchemySchema):
    class Meta:
        model = Employee
        include_fk = True
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    contact_number = auto_field()
    email = auto_field()
    role = auto_field()


class ItemSchema(SQLAlchemySchema):
    class Meta:
        model = Item
        include_fk = True
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    price = auto_field()
    ingredients = auto_field()


class PaymentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        include_fk = True
        load_instance = True
        include_relationships = True

    order_id = auto_field()
    employee_id = auto_field()
    customer_id = auto_field()
    price = auto_field()
