import requests
from typing import Dict, Any
from config import TOKEN, URL1, URL2

class APIClient:
    def __init__(self) -> None:
        self.headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        }

    def get_cart_info(self) -> Dict[str, Any]:
        response = requests.get(f"{URL2}cart/short", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search_product(
        self,
        city_id: int,
        phrase: str,
        ab_test_group: str
    ) -> requests.Response:
        response = requests.get(
            f"{URL1}search/facet-search",
            params={
                "customerCityId": city_id,
                "phrase": phrase,
                "abTestGroup": ab_test_group
            },
            headers=self.headers
        )
        response.raise_for_status()
        return response

    def add_product_to_cart(self, product_id: int) -> requests.Response:
        response = requests.post(
            f"{URL2}cart/product",
            json={"id": product_id},
            headers=self.headers
        )
        response.raise_for_status()
        return response

    def checkout(
        self,
        city_id: int,
        shipment_type: str,
        user_type: str,
        order_type: str
    ) -> requests.Response:
        response = requests.get(
            f"{URL2}orders/checkout",
            params={
                "cityID": city_id,
                "shipmentType": shipment_type,
                "userType": user_type,
                "orderType": order_type
            },
            headers=self.headers
        )
        response.raise_for_status()
        return response
