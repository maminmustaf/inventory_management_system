import requests

OPEN_FOOD_FACTS_BASE = "https://world.openfoodfacts.org"
USER_AGENT = "MoringaInventoryApp/1.0 (student-project@example.com)"


def _clean_product(product):
    """Return only the fields our inventory system needs."""
    return {
        "product_name": product.get("product_name", ""),
        "brands": product.get("brands", ""),
        "ingredients_text": product.get("ingredients_text", ""),
        "barcode": product.get("code", ""),
        "image_url": product.get("image_url", "")
    }


def find_product(barcode=None, name=None):
    """
    Find a product from Open Food Facts.

    Barcode lookup uses API v3.
    Name lookup uses the Open Food Facts search endpoint.
    Returns a simple dictionary, or None when no product is found.
    """
    headers = {"User-Agent": USER_AGENT}

    try:
        if barcode:
            url = f"{OPEN_FOOD_FACTS_BASE}/api/v3.6/product/{barcode}.json"
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != 1 or "product" not in data:
                return None

            product = data["product"]
            product["code"] = barcode
            return _clean_product(product)

        if name:
            params = {
                "search_terms": name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 1
            }

            url = f"{OPEN_FOOD_FACTS_BASE}/cgi/search.pl"
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            products = data.get("products", [])
            if not products:
                return None

            return _clean_product(products[0])

    except requests.RequestException:
        return None

    return None
