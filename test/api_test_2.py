import pytest
import requests
import allure
from Pages.api_client import ApiClient


class TestAPI:

    @pytest.fixture(scope='class', autouse=True)
    def set_up_class(self, api_urls):
        self.api_urls = api_urls
        self.client_1 = ApiClient(self.api_urls['URL_1'])
        self.client_2 = ApiClient(self.api_urls['URL_2'])

    @allure.feature("Корзина")
    @allure.title("Получение информации о товарах в корзине")
    @allure.story("Корзина - Получение короткой информации")
    @pytest.mark.api
    def test_api_get_cart_short(self) -> None:
        response = self.client_2.get('cart/short')
        assert response.status_code == 200

    @allure.feature("Поиск товаров")
    @allure.title("Поиск товаров по фразе")
    @allure.story("Поиск - Поиск по названию")
    @pytest.mark.api
    def test_api_search_by_phrase(self, test_data: dict) -> None:
        phrase_encoded = requests.utils.quote(test_data['search_phrase'])
        response = self.client_1.get('search/facet-search', params={
            'customerCityId': 213,
            'phrase': phrase_encoded,
            'abTestGroup': 1
        })
        assert response.status_code == 200

    @allure.feature("Корзина. Добавление товара")
    @allure.title("Добавление товара по валидному ID")
    @allure.story("Корзина - Добавление товара по валидному ID")
    @pytest.mark.api
    def test_api_add_product_to_cart_valid(self) -> None:
        response = self.client_2.post('cart/product', json={"id": 3111363})
        assert response.status_code == 200

    @allure.feature("Корзина. Добавление товара с некорректным ID")
    @allure.title("Обработка некорректного ID товара")
    @allure.story("Корзина - Добавление товара с некорректным ID")
    @pytest.mark.api
    def test_api_add_product_invalid_id(self, test_data: dict) -> None:
        response = self.client_2.post('cart/product', json={"id": test_data['invalid_id']})
        assert response.status_code in [400, 401, 422, 500]

    @allure.feature("Поиск книг")
    @allure.title("Поиск книг с некорректным запросом")
    @allure.story("Поиск - Некорректный запрос")
    @pytest.mark.api
    def test_api_search_with_invalid_query(self, client: ApiClient, test_data: dict) -> None:
        response = client.get('search/facet-search', params={'customerCityId': 213})
        assert response.status_code in [400, 401, 422, 500]

    @allure.feature("Добавление с неправильным количеством товара")
    @allure.title("Тест: Добавление товара с некорректным количеством")
    @allure.story("Проверка обработки некорректного количества товаров в корзине")
    @pytest.mark.api
    def test_api_add_product_with_invalid_quantity(self, test_data: dict) -> None:
        response = self.client_2.post('cart/product', json={
            "id": test_data['invalid_id'],
            "quantity": test_data['invalid_quantity']
        })
        assert response.status_code in [400, 401, 403, 404, 422, 500]