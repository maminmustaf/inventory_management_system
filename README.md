# Inventory Management System

A beginner-friendly Flask REST API for managing retail inventory.

The project includes:

- Flask REST API
- CRUD operations
- Temporary array-based storage
- Open Food Facts integration
- CLI interface
- Simple browser admin interface
- Pytest unit tests
- Mocked external API tests

## 1. Project Structure

```text
inventory_management_system/
│
├── app.py
├── cli.py
├── external_api.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── app.js
│   └── style.css
│
└── tests/
    ├── test_app.py
    └── test_external_api.py
```

## 2. Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Run the Flask API

```bash
python3 app.py
```

The server runs at:

```text
http://127.0.0.1:5000
```

Open that address in a browser to use the simple admin portal.

## 4. REST API Endpoints

### GET /inventory

Returns all inventory items.

```bash
curl http://127.0.0.1:5000/inventory
```

### GET /inventory/<id>

Returns one item.

```bash
curl http://127.0.0.1:5000/inventory/1
```

### POST /inventory

Adds a new item.

```bash
curl -X POST http://127.0.0.1:5000/inventory \
-H "Content-Type: application/json" \
-d '{"product_name":"Milk","price":200,"stock":10}'
```

### PATCH /inventory/<id>

Updates part of an item.

```bash
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
-H "Content-Type: application/json" \
-d '{"price":400,"stock":30}'
```

### DELETE /inventory/<id>

Deletes an item.

```bash
curl -X DELETE http://127.0.0.1:5000/inventory/1
```

### GET /external-product

Find a product from Open Food Facts.

By barcode:

```bash
curl "http://127.0.0.1:5000/external-product?barcode=3017620422003"
```

By name:

```bash
curl "http://127.0.0.1:5000/external-product?name=Nutella"
```

## 5. CLI

Start Flask first:

```bash
python3 app.py
```

Then open another terminal and run:

```bash
python3 cli.py
```

The CLI allows you to:

1. Add inventory item
2. View inventory
3. Update item
4. Delete item
5. Find product on Open Food Facts
6. Exit

## 6. Testing

Run:

```bash
pytest -v
```

The tests cover:

- GET all inventory
- GET one item
- Missing item errors
- POST
- Invalid POST
- PATCH
- DELETE
- External API mocking

## 7. Important Design Decision

This project intentionally uses a Python list as temporary storage instead of a database.

That matches the assignment requirement to simulate a database with an array.

If the Flask server is restarted, changes made to the array are lost.

A future version could replace the list with SQLite, PostgreSQL, or another database.

## 8. External API

Open Food Facts provides product information such as product names, brands, ingredients, images, and nutritional information.

This project uses the external API only to supplement product information. It does not store Open Food Facts data permanently.

## 9. GitHub

Example commands:

```bash
git init
git add .
git commit -m "Build inventory management system"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
