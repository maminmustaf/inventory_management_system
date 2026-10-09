from flask import Flask, jsonify, request

from external_api import find_product

app = Flask(__name__)

# Temporary storage: this is our "mock database".
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "price": 350.00,
        "stock": 20,
        "barcode": "01",
        "ingredients_text": "Filtered water, almonds, cane sugar"
    },
    {
        "id": 2,
        "product_name": "Corn Flakes",
        "brands": "Kellogg's",
        "price": 280.00,
        "stock": 15,
        "barcode": "02",
        "ingredients_text": "Milled corn, sugar, salt"
    }
]


def get_next_id():
    """Return an ID one larger than the current largest ID."""
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1

@app.get("/inventory")
def get_inventory():
    return jsonify({
        "inventory": inventory,
        "count": len(inventory)
    })


@app.get("/inventory/<int:item_id>")
def get_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    return jsonify(item)


@app.post("/inventory")
def add_item():
    data = request.get_json(silent=True) or {}

    required_fields = ["product_name", "price", "stock"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    try:
        price = float(data["price"])
        stock = int(data["stock"])
    except (TypeError, ValueError):
        return jsonify({"error": "Price must be a number and stock must be an integer"}), 400

    if price < 0 or stock < 0:
        return jsonify({"error": "Price and stock cannot be negative"}), 400

    item = {
        "id": get_next_id(),
        "product_name": data["product_name"],
        "brands": data.get("brands", ""),
        "price": price,
        "stock": stock,
        "barcode": data.get("barcode", ""),
        "ingredients_text": data.get("ingredients_text", "")
    }

    inventory.append(item)

    return jsonify(item), 201


@app.patch("/inventory/<int:item_id>")
def update_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    data = request.get_json(silent=True) or {}

    allowed_fields = [
        "product_name",
        "brands",
        "price",
        "stock",
        "barcode",
        "ingredients_text"
    ]

    for field in allowed_fields:
        if field in data:
            if field == "price":
                try:
                    value = float(data[field])
                except (TypeError, ValueError):
                    return jsonify({"error": "Price must be a number"}), 400
                if value < 0:
                    return jsonify({"error": "Price cannot be negative"}), 400
                item[field] = value

            elif field == "stock":
                try:
                    value = int(data[field])
                except (TypeError, ValueError):
                    return jsonify({"error": "Stock must be an integer"}), 400
                if value < 0:
                    return jsonify({"error": "Stock cannot be negative"}), 400
                item[field] = value

            else:
                item[field] = data[field]

    return jsonify(item)


@app.delete("/inventory/<int:item_id>")
def delete_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Inventory item not found"}), 404

    inventory.remove(item)

    return jsonify({
        "message": "Inventory item deleted",
        "item": item
    })


@app.get("/external-product")
def external_product():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({
            "error": "Provide either barcode or name"
        }), 400

    result = find_product(barcode=barcode, name=name)

    if result is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
