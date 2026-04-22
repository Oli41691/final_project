from requests.exceptions import HTTPError, RequestException
from typing import Optional, Dict, Any, Tuple
import requests
from config import BASE_URL, URL_2, ACCESS_TOKEN, COOKIES

class ApiClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        url_2: Optional[str] = None,
        token: Optional[str] = None,
        use_url_2: bool = False,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Инициализация API-клиента.
        :param base_url: Базовый URL API (строка или None).
        :param url_2: Альтернативный базовый URL (строка или None).
        :param token: Токен авторизации (строка или None).
        :param use_url_2: Использовать ли URL_2 по умолчанию.
        :param headers: Дополнительные заголовки (словарь или None).
        """
        self.base_url: str = (base_url.rstrip('/') + '/') if base_url else ''
        self.url_2: str = (url_2.rstrip('/') + '/') if url_2 else ''
        self.use_url_2: bool = use_url_2
        self.session: requests.Session = requests.Session()

        default_headers: Dict[str, str] = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        if token:
            default_headers['Authorization'] = f'Bearer {token}'

        if headers:
            default_headers.update(headers)

        self.session.headers.update(default_headers)

    def _get_base_url(self, use_url_2: Optional[bool] = None) -> str:
        """
        Возвращает базовый URL в виде строки.
        :param use_url_2: Использовать ли URL_2 (или по умолчанию, если None).
        :return: URL как строка.
        """
        if use_url_2 is None:
            use_url_2 = self.use_url_2
        return self.url_2 if use_url_2 and self.url_2 else self.base_url

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        use_url_2: Optional[bool] = None
    ) -> Tuple[int, Dict]:
        """
        Выполняет HTTP-запрос.
        :param method: метод HTTP (например, 'get', 'post').
        :param endpoint: endpoint URL (относительно базового).
        :param params: параметры строки запроса (словарь или None).
        :param json: тело запроса JSON (словарь или None).
        :param use_url_2: использовать ли URL_2.
        :return: кортеж (код ответа, JSON-ответ или сообщение об ошибке).
        """
        if use_url_2 is None:
            use_url_2 = self.use_url_2
        url: str = self._get_base_url(use_url_2) + endpoint
        resp: requests.Response = getattr(self.session, method)(url, params=params, json=json)
        try:
            response_json = resp.json()
        except Exception:
            response_json = {"error": resp.text}
        return resp.status_code, response_json

    def get_cart_info(self) -> Tuple[int, Dict]:
        """
        Получает информацию о корзине.
        :return: (код ответа, словарь данных корзины или ошибки)
        """
        return self._request('get', 'cart')

    def search_product(
        self,
        city_id: int,
        phrase: str,
        ab_test_group: str = "",
        page: int = 1,
        per_page: int = 60
    ) -> Tuple[int, Dict]:
        """
        Выполняет поиск продукта.
        :param city_id: Идентификатор города.
        :param phrase: Строка поиска.
        :param ab_test_group: Группа A/B тестирования.
        :param page: Номер страницы.
        :param per_page: Количество элементов на странице.
        :return: (код ответа, результаты поиска как словарь).
        """
        params: Dict[str, Any] = {
            "customerCityId": city_id,
            "phrase": phrase
        }
        return self._request('get', 'search/facet-search', params=params, use_url_2=True)

    def product_to_cart(self, product_id: int, quantity: int = 1) -> Tuple[int, Dict]:
        """
        Добавляет продукт в корзину.
        :param product_id: ID продукта.
        :param quantity: Количество.
        :return: (код ответа, ответ API как словарь).
        """
        payload: Dict[str, Any] = {
            "id": product_id,
            "quantity": quantity
        }
        return self._request('post', 'cart/product', json=payload)

    def checkout(self, city_id: str, shipment_type: str, user_type: str, order_type: str) -> Tuple[int, Dict]:
        """
        Оформление заказа.
        :param city_id: ID города.
        :param shipment_type: Тип доставки.
        :param user_type: Тип пользователя.
        :param order_type: Тип заказа.
        :return: (код ответа, ответ сервера как словарь).
        """
        payload: Dict[str, Any] = {
            "city_id": city_id,
            "shipment_type": shipment_type,
            "user_type": user_type,
            "order_type": order_type
        }
        return self._request('post', 'checkout', json=payload)

    def close(self) -> None:
        """
        Закрывает сессию.
        """
        self.session.close()
