import requests

BASE_URL = "http://127.0.0.1:5000"


def print_item(item):
    print("\n--- Inventory Item ---")
    print(f"ID: {item.get('id')}")
    print(f"Product: {item.get('product_name')}")
    print(f"Brand: {item.get('brands', '')}")
    print(f"Price: KSh {item.get('price', 0)}")
    print(f"Stock: {item.get('stock', 0)}")
    print(f"Barcode: {item.get('barcode', '')}")
    print(f"Ingredients: {item.get('ingredients_text', '')}")


def add_item():
    data = {
        "product_name": input("Product name: "),
        "brands": input("Brand: "),
        "price": float(input("Price (KSh): ")),
        "stock": int(input("Stock: ")),
        "barcode": input("Barcode (optional): "),
        "ingredients_text": input("Ingredients (optional): ")
    }

    response = requests.post(f"{BASE_URL}/inventory", json=data)
    print(response.json())


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.ok:
        data = response.json()
        print(f"\nInventory contains {data['count']} item(s).")
        for item in data["inventory"]:
            print_item(item)
    else:
        print(response.json())


def update_item():
    item_id = int(input("Item ID to update: "))
    print("Leave a field blank if you do not want to change it.")

    data = {}

    price = input("New price: ")
    stock = input("New stock: ")
    name = input("New product name: ")

    if price:
        data["price"] = float(price)
    if stock:
        data["stock"] = int(stock)
    if name:
        data["product_name"] = name

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )
    print(response.json())


def delete_item():
    item_id = int(input("Item ID to delete: "))

    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    print(response.json())


def find_external_product():
    choice = input("Search by (1) barcode or (2) name: ")

    if choice == "1":
        barcode = input("Barcode: ")
        response = requests.get(
            f"{BASE_URL}/external-product",
            params={"barcode": barcode}
        )
    elif choice == "2":
        name = input("Product name: ")
        response = requests.get(
            f"{BASE_URL}/external-product",
            params={"name": name}
        )
    else:
        print("Invalid choice.")
        return

    print(response.json())


def main():
    while True:
        print("""
= INVENTORY CLI =
1. Add inventory item
2. View inventory
3. Update item
4. Delete item
5. Find External Product
6. Exit
""")

        choice = input("Choose an option: ")

        try:
            if choice == "1":
                add_item()
            elif choice == "2":
                view_inventory()
            elif choice == "3":
                update_item()
            elif choice == "4":
                delete_item()
            elif choice == "5":
                find_external_product()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Choose 1-6.")
        except ValueError:
            print("Invalid input. Please enter the correct type of value.")


if __name__ == "__main__":
    main()
