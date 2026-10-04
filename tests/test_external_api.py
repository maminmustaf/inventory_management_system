from unittest.mock import Mock, patch
import requests

from external_api import find_product


@patch("external_api.requests.get")
def test_find_product_by_barcode(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "ingredients_text": "Water, almonds",
            "code": "000000000001",
            "image_url": "https://example.com/image.jpg"
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = find_product(barcode="000000000001")

    assert result["product_name"] == "Organic Almond Milk"
    assert result["brands"] == "Silk"
    mock_get.assert_called_once()


@patch("external_api.requests.get")
def test_find_product_by_name(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Corn Flakes",
                "brands": "Kellogg's",
                "ingredients_text": "Corn, sugar",
                "code": "000000000002"
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = find_product(name="Corn Flakes")

    assert result["product_name"] == "Corn Flakes"


@patch("external_api.requests.get")
def test_external_api_failure_returns_none(mock_get):
    mock_get.side_effect = requests.RequestException("Network problem")

    result = find_product(barcode="000000000001")

    assert result is None
