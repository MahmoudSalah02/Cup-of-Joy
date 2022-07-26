
# Cafe REST API

Backend code for a coffee shop that allows employees to take customer orders


## API Reference

### Get all employees

```http
  GET /operations/employees
```

`Response`:
```yaml
[
  {
    "contact_number": 555,
    "email": "five@gmail.com",
    "id": 1,
    "name": "five"
  },
  {
    "contact_number": 444,
    "email": "four@gmail.com",
    "id": 2,
    "name": "four"
  }
]
```

### Create employee

```http
  POST /operations/employees
```

`Request Body`:
```yaml
{
  "contact_number": 555,
  "email": "five@gmail.com",
  "name": "five"
}
```

`Response`:
```yaml
{
  "contact_number": 555,
  "email": five@gmail.com,
  "id": 1,
  "name": "five"
}

```
### Delete employee

```http
  DELETE /operations/employees/${employee_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `employee_id`| `integer` | **Required**. Id of employee to delete |


`Response`:

```yaml
{
"contact_number": 555,
"email": "five@gmail.com",
"id": 1,
"name": "five"
}
```

### Get employee

```http
  GET /operations/employees/${employee_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `employee_id`| `integer` | **Required**. Id of employee to fetch |


`Response`:
```yaml
{
  "contact_number": 555,
  "email": five@gmail.com,
  "id": 1,
  "name": "five"
}
```
### Update employee

```http
  PUT /operations/employees/${employee_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `employee_id`| `integer` | **Required**. Id of employee to update |


`Request Body`:
```yaml
{
  "contact_number": 555,
  "email": "five@gmail.com",
  "name": "five"
}

```

`Response`:
```yaml
{
  "contact_number": 555,
  "email": five@gmail.com,
  "id": 1,
  "name": "five"
}
```


### Get all items

```http
  GET /operations/items
```

`Response`:
```yaml
[
  {
    "id": 1,
    "ingredients": "",
    "name": "Curry Chicken with Onion",
    "price": "$7.00"
  },
  {
    "id": 2,
    "ingredients": "",
    "name": "Chicken with Black Beans",
    "price": "$7.00"
  }
]
```

### Create item

```http
  POST /operations/items
```

`Request Body`:
```yaml
{
  "ingredients": "chicken, onions, rice",
  "name": "Curry Chicken with Onion",
  "price": "$7.00"
}
```

`Response`:
```yaml
{
  "id": 1,
  "ingredients": "",
  "name": "Curry Chicken with Onion",
  "price": "$7.00"
}
```

### Delete item

```http
  DELETE /operations/items/${item_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `item_id`| `integer` | **Required**. Id of item to delete |


`Response`:
```yaml
{
  "id": 1,
  "ingredients": "",
  "name": "Curry Chicken with Onion",
  "price": "$7.00"
}
```
### Get item

```http
  GET /operations/items/${item_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `item_id`| `integer` | **Required**. Id of item to fetch |


`Response`:
```yaml
{
  "id": 1,
  "ingredients": "",
  "name": "Curry Chicken with Onion",
  "price": "$7.00"
}
```

### Update item

```http
  PUT /operations/employees/${item_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `item_id`| `integer` | **Required**. Id of item to update |


`Request Body`:
```yaml
{
  "ingredients": "chicken, onions, rice",
  "name": "Curry Chicken with Onion",
  "price": "$10.00"
}
```

`Response`:
```yaml
{
  "id": 1,
  "ingredients": "",
  "name": "Curry Chicken with Onion",
  "price": "$10.00"
}
```

### Get all customers

```http
  GET /shop/customers
```

`Response`:
```yaml
[
  {
    "contact_number": 1,
    "id": 1,
    "name": "one"
  },
  {
    "contact_number": 2,
    "id": 2,
    "name": "two"
  }
]
```

### Create customer

```http
  POST /shop/customers
```

`Request Body`:
```yaml
{
  "contact_number": 3,
  "name": "three"
}
```


`Response`:
```yaml
{
  "id": 3,
  "contact_number": 3,
  "name": "three"
}
```

### Delete customer

```http
  DELETE /shop/customers/${customer_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `customer_id`| `integer` | **Required**. Id of customer to delete |


`Response`:
```yaml
{
  "id": 3,
  "contact_number": 3,
  "name": "three"
}
```
### Get customer

```http
  GET /shop/customers/${employee_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `customer_id`| `integer` | **Required**. Id of customer to fetch |


`Response`:
```yaml
{
  "id": 3,
  "contact_number": 3,
  "name": "three"
}
```

### Update customer

```http
  PUT /shop/customers/${customer_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `customer_id`| `integer` | **Required**. Id of customer to update |


`Request Body`:
```yaml
{
  "contact_number": 4,
  "name": "four"
}
```

`Response`:
```yaml
{
  "id": 4,
  "contact_number": 4,
  "name": "four"
}
```

### Get all orders

```http
  GET /shop/orders
```

`Response`:
```yaml
[
 {
  "customer_id": 2,
  "employee_id": 5,
  "id": 7,
  "items_ordered": [
    {
      "customer_notes": "no salt",
      "item_id": 1,
      "quantity": 1
    }
  ],
  "order_time": "2022-07-25T07:20:08.023003",
  "status": "preparing"
},
{
  "customer_id": 1,
  "employee_id": 2,
  "id": 12,
  "items_ordered": [
    {
      "customer_notes": "A LOT OF SALT",
      "item_id": 5,
      "quantity": 2
    },
    {
      "customer_notes": "NO SUGAR",
      "item_id": 4,
      "quantity": 2
    }
  ],
  "order_time": "2022-07-25T07:20:08.023003",
  "status": "preparing"
]
```

### Create order

```http
  POST /shop/orders
```

`Request Body`:
```yaml
{
  "customer_id": 2,
  "employee_id": 3,
  "items_ordered": [
    {
      "customer_notes": "extra salt",
      "item_id": 3,
      "quantity": 2
    }
  ],
  "status": "preparing"
}
```


`Response`:
```yaml
{
  "customer_id": 2,
  "employee_id": 1,
  "id": 19,
  "items_ordered": [
    {
      "customer_notes": "extra salt",
      "item_id": 3,
      "quantity": 2
    }
  ],
  "order_time": "2022-07-25T10:12:40.397597",
  "status": "preparing"
}
```

### Delete order

```http
  DELETE /shop/orders/${order_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `order_id`| `integer` | **Required**. Id of order to delete |


`Response`:

```yaml
{
  "customer_id": 2,
  "employee_id": 1,
  "id": 19,
  "items_ordered": [
    {
      "customer_notes": "extra salt",
      "item_id": 3,
      "quantity": 2
    }
  ],
  "order_time": "2022-07-25T10:12:40.397597",
  "status": "preparing"
}
```
### Get order

```http
  GET /shop/orders/${order_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `order_id`| `integer` | **Required**. Id of order to fetch |


`Response`:
```yaml
{
  "customer_id": 1,
  "employee_id": 2,
  "id": 12,
  "items_ordered": [
    {
      "customer_notes": "A LOT OF SALT",
      "item_id": 5,
      "quantity": 2
    },
    {
      "customer_notes": "NO SUGAR",
      "item_id": 4,
      "quantity": 2
    }
  ],
  "order_time": "2022-07-25T07:44:11.668169",
  "status": "preparing"
}
```
### Update order

```http
  PUT /shop/orders/${order_id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `order_id`| `integer` | **Required**. Id of order to update |


`Request Body`:
```yaml
{
  "customer_id": 1,
  "employee_id": 2,
  "items_ordered": [
    {
      "customer_notes": "chicken tika masala",
      "item_id": 1,
      "quantity": 2
    }
  ],
  "status": "preparing"
}
```


`Response`:
```yaml
{
  "customer_id": 1,
  "employee_id": 2,
  "id": 12,
  "items_ordered": [
    {
      "customer_notes": "chicken tika masala",
      "item_id": 1,
      "quantity": 2
    }
  ],
  "order_time": "2022-07-25T07:44:11.668169",
  "status": "preparing"
}
```
## Authors

- [@Mahmoud Salah](https://www.github.com/MahmoudSalah02)

