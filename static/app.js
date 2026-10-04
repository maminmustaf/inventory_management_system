const message = document.getElementById("message");
const inventoryList = document.getElementById("inventory-list");


async function loadInventory() {
    const response = await fetch("/inventory");
    const data = await response.json();

    inventoryList.innerHTML = "";

    data.inventory.forEach(item => {
        const div = document.createElement("div");
        div.className = "item";

        div.innerHTML = `
            <strong>${item.product_name}</strong><br>
            Brand: ${item.brands || "N/A"}<br>
            Price: KSh ${item.price}<br>
            Stock: ${item.stock}<br>
            Barcode: ${item.barcode || "N/A"}
            <div class="item-actions">
                <button onclick="editItem(${item.id})">Edit</button>
                <button onclick="deleteItem(${item.id})">Delete</button>
            </div>
        `;

        inventoryList.appendChild(div);
    });
}


document.getElementById("add-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
        product_name: document.getElementById("product_name").value,
        brands: document.getElementById("brands").value,
        price: Number(document.getElementById("price").value),
        stock: Number(document.getElementById("stock").value),
        barcode: document.getElementById("barcode").value,
        ingredients_text: document.getElementById("ingredients_text").value
    };

    const response = await fetch("/inventory", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
        message.textContent = "Item added successfully.";
        message.className = "success";
        event.target.reset();
        loadInventory();
    } else {
        message.textContent = result.error;
        message.className = "error";
    }
});


async function editItem(id) {
    const price = prompt("Enter new price:");
    const stock = prompt("Enter new stock:");

    if (price === null && stock === null) {
        return;
    }

    const data = {};

    if (price !== null && price !== "") {
        data.price = Number(price);
    }

    if (stock !== null && stock !== "") {
        data.stock = Number(stock);
    }

    const response = await fetch(`/inventory/${id}`, {
        method: "PATCH",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
        loadInventory();
    } else {
        alert(result.error);
    }
}


async function deleteItem(id) {
    if (!confirm("Delete this item?")) {
        return;
    }

    const response = await fetch(`/inventory/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    if (response.ok) {
        loadInventory();
    } else {
        alert(result.error);
    }
}


async function findByBarcode() {
    const barcode = document.getElementById("external-barcode").value;

    const response = await fetch(
        `/external-product?barcode=${encodeURIComponent(barcode)}`
    );

    const result = await response.json();

    document.getElementById("external-result").textContent =
        JSON.stringify(result, null, 2);
}


async function findByName() {
    const name = document.getElementById("external-name").value;

    const response = await fetch(
        `/external-product?name=${encodeURIComponent(name)}`
    );

    const result = await response.json();

    document.getElementById("external-result").textContent =
        JSON.stringify(result, null, 2);
}


loadInventory();
