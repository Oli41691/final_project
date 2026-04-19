import requests
from typing import Dict, Any, Optional
from requests.exceptions import HTTPError, RequestException
import logging
from config import BASE_URL, ACCESS_TOKEN, COOKIES, URL_2
import urllib.parse
from requests.exceptions import HTTPError, RequestException

logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self, 
        base_url: str = None,  
        url_2: str = None,     
        token: Optional[str] = None
    ):
        self.base_url = (base_url or "").rstrip('/') + '/' if base_url else None
        self.url_2 = (url_2 or "").rstrip('/') + '/' if url_2 else None
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
        # сюда можно добавить cookies и другие настройки
        self.timeout = 30

    def _handle_response(self, response: requests.Response) -> requests.Response:
        """Обработка ответа"""
        try:
            response.raise_for_status()
        except HTTPError as e:
            logger.error(f"HTTP error: {e}, Response: {response.text}")
        raise
        try:
            response.json()
        except ValueError:
            logger.warning("Ответ не является JSON")
        return response

    def get_cart_info(self) -> Dict[str, Any]:
        """Получение информации о корзине, использует base_url"""
        if not self.base_url:
            raise ValueError("base_url не задан")
        url = f"{self.base_url}cart/short"
        logger.info(f"Request URL: {url}")
        response = self.session.get(url, timeout=self.timeout)
        return self._handle_response(response).json()

    def search_product(self, city_id: int, phrase: str, ab_test_group: str,
        page=1,
        per_page=60,
        use_url_2: bool = True):
        """Поиск товара, выбор URL по флагу"""
        url_base = self.url_2 if use_url_2 and self.url_2 else self.base_url
        if not url_base:
            raise ValueError("URL для поиска не задан")
        response = self.session.get(
            f"{url_base}search/product",
            params={
                "customerCityId": city_id,
                "phrase": phrase,
                "abTestGroup": ab_test_group,
                "products[page]": page,
                "products[per-page]": per_page
            },
            timeout=self.timeout
        )
        return self._handle_response(response)

    def product_to_cart(self, product_id):
        if not self.base_url:
            raise ValueError("base_url не задан")
        url = f"{self.base_url}cart/product"
        payload = {"id": product_id}
        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def checkout(self, city_id: int, shipment_type: str, user_type: str, order_type: str) -> Dict[str, Any]:
        if not self.base_url:
            raise ValueError("base_url не задан")
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

    def close(self):
        self.session.close()
