# Project Plan — Inventory Management System

## Task 1: Define the Problem

The company needs a small administrator system that allows employees to:

- Add inventory products
- View inventory products
- Edit prices and stock
- Delete products
- Search Open Food Facts for product information

## Task 2: Determine the Design

### Mock database

Python list:

```python
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "price": 350,
        "stock": 20,
        "barcode": "000000000001",
        "ingredients_text": "Filtered water, almonds, cane sugar"
    }
]
```

Every item has an ID.

### Route plan

| Method | Route | Purpose |
|---|---|---|
| GET | `/inventory` | Get all products |
| GET | `/inventory/<id>` | Get one product |
| POST | `/inventory` | Add product |
| PATCH | `/inventory/<id>` | Edit product |
| DELETE | `/inventory/<id>` | Delete product |
| GET | `/external-product` | Find product on Open Food Facts |

## Task 3: Develop

### Step 1 — File Setup

Install:

- Flask
- requests
- pytest

### Step 2 — API Design

Build the CRUD routes in `app.py`.

### Step 3 — Fetch Data

`external_api.py` communicates with Open Food Facts.

Keeping this in a separate file makes the application easier to understand and test.

### Step 4 — CLI Frontend

`cli.py` sends HTTP requests to the Flask server.

The CLI does not directly change the inventory list.

Instead:

```text
CLI
 ↓
HTTP request
 ↓
Flask route
 ↓
inventory list
```

## Task 4: Test and Debug

Use pytest and unittest.mock.

The external API tests mock `requests.get()` so tests do not depend on the real internet.

## Task 5: Document and Maintain

README contains:

- Setup
- API endpoints
- CLI usage
- Testing
- GitHub commands
