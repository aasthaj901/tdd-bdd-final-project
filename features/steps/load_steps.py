######################################################################
# Load steps for BDD testing
######################################################################
import requests
from behave import given
from service.common import status

BASE_URL = "http://localhost:5000/api/products"

@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones from context.table """
    # Delete all existing products
    response = requests.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK
    for product in response.json():
        del_resp = requests.delete(f"{BASE_URL}/{product['id']}")
        assert del_resp.status_code == status.HTTP_204_NO_CONTENT

    # Load the database with new products
    for row in context.table:
        payload = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"] in ["True", "true", "1"],
            "category": row["category"]
        }
        context.resp = requests.post(BASE_URL, json=payload)
        assert context.resp.status_code == status.HTTP_201_CREATED
