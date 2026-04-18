import requests
from typing import Dict, Any, Optional
from requests.exceptions import HTTPError, RequestException
import logging
from config import BASE_URL, ACCESS_TOKEN

logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self, base_url: str = BASE_URL, token: Optional[str] = ACCESS_TOKEN):
        self.base_url = base_url.rstrip('/') + '/'
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Python-API-Tests/10"
        })
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> requests.Response:
        """Обработка ответа"""
        try:
            response.raise_for_status()
        except HTTPError as e:
            logger.error(f"HTTP error: {e}, Response: {response.text}")
            raise
        return response

    def get_cart_info(self) -> Dict[str, Any]:
        """Получение информации о корзине"""
        try:
            response = self.session.get(
                f"{self.base_url}cart/short", 
                timeout=self.timeout
            )
            return self._handle_response(response).json()
        except RequestException as e:
            logger.error(f"Failed to get info: {e}")
            raise

    def search_product(self, city_id: int, phrase: str, ab_test_group: str) -> Dict[str, Any]:
        """Поиск товара"""
        try:
            response = self.session.get(
                f"{self.base_url}search/facet-search",
                params={
                    "customerCityId": city_id,
                    "phrase": phrase,
                    "abTestGroup": ab_test_group
                },
                timeout=self.timeout
            )
            return self._handle_response(response).json()
        except RequestException as e:
            logger.error(f"Search failed: {e}")
            raise

    def product_to_cart(self, product_id: str, quantity: int = 1) -> Dict[str, Any]:
        """Добавление товара в корзину"""
        try:
            response = self.session.post(
                f"{self.base_url}cart/product",
                json={"id": product_id, "quantity": quantity},
                timeout=self.timeout
            )
            return self._handle_response(response).json()
        except RequestException as e:
            logger.error(f"Failed to add product {product_id}: {e}")
            raise

    def checkout(self, city_id: int, shipment_type: str, user_type: str, order_type: str) -> Dict[str, Any]:
        """Оформление заказа"""
        try:
            response = self.session.get(
                f"{self.base_url}checkout",
                params={
                    "cityID": city_id,
                    "shipmentType": shipment_type,
                    "userType": user_type,
                    "orderType": order_type
                },
                timeout=self.timeout
            )
            return self._handle_response(response).json()
        except RequestException as e:
            logger.error(f"Checkout failed: {e}")
            raise

    def close(self):
        """Закрытие сессии"""
        self.session.close()
