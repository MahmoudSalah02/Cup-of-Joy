from models.models import session, Customer, Order, OrderItem, Payment, Employee, Item
from seeds.data import MENU, CUSTOMERS
from datetime import datetime

items = []
for item in MENU:
    print(item)
    i = Item(name=item.get("name"),
             price=item.get("price"),
             ingredients=item.get("ingredients"))
    items += [i]
    session.add(i)

# synchronize session data with the database
session.flush()

# iterate over the MENU and CUSTOMERS structure and populate the database
price = 10
for customer in CUSTOMERS:
    print(customer)
    c = Customer(id=customer.get("customer_id"),
                 name=customer.get("name"),
                 contact_number=customer.get("contact_number"))
    session.add(c)
    for order in customer.get("orders"):
        price += 1.5
        employee_info = order.get("employee")
        print(employee_info)
        e = Employee(id=employee_info.get("employee_id"),
                     name=employee_info.get("name"),
                     contact_number=employee_info.get("contact_number"))
        o = Order(id=order.get("id"),
                  customer_id=c.id,
                  employee_id=e.id,
                  order_time=datetime.now(),
                  status=order.get("status"))
        session.add(e)
        c.orders_placed.append(o)
        for item in items:
            orderItem = OrderItem(order_id=o.id,
                                  item_id=item.id,
                                  quantity=1,
                                  customer_notes="no salt")
            o.items_ordered.append(orderItem)
        p = Payment(order_id=o.id,
                    customer_id=c.id,
                    employee_id=e.id,
                    price=price)

session.commit()
