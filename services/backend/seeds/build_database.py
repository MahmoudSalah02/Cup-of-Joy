from services.backend.models.models import Customer, Order, OrderItem, Payment, Employee, Item
from services.backend import init_db
from services.backend.seeds.data import MENU, CUSTOMERS
from datetime import datetime


def populate():
    session = init_db.get_session()
    try:
        items = []
        for item in MENU:
            new_item = Item(name=item.get("name"),
                            price=item.get("price"),
                            ingredients=item.get("ingredients"))
            items += [new_item]
            session.add(new_item)

        # synchronize session data with the database
        session.flush()

        # iterate over the MENU and CUSTOMERS structure and populate the database
        price = 10
        for customer in CUSTOMERS:
            new_customer = Customer(id=customer.get("customer_id"),
                                    name=customer.get("name"),
                                    contact_number=customer.get("contact_number"))
            session.add(new_customer)
            for order in customer.get("orders"):
                price += 1.5
                employee_info = order.get("employee")
                new_employee = Employee(id=employee_info.get("employee_id"),
                                        name=employee_info.get("name"),
                                        contact_number=employee_info.get("contact_number"),
                                        role="cashier")
                new_order = Order(id=order.get("id"),
                                  customer_id=new_customer.id,
                                  employee_id=new_employee.id,
                                  order_time=datetime.now(),
                                  status=order.get("status"))
                session.add(new_employee)
                new_customer.orders_placed.append(new_order)
                for item in items:
                    order_item = OrderItem(order_id=new_order.id,
                                           item_id=item.id,
                                           quantity=1,
                                           customer_notes="no salt")
                    new_order.items_ordered.append(order_item)

                session.flush()

                new_payment = Payment(order_id=new_order.id,
                                      customer_id=new_customer.id,
                                      employee_id=new_employee.id,
                                      price=price)
                session.add(new_payment)
        session.commit()
    except Exception as e:
        print(type(e))
