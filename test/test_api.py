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

    @pytest.mark.api
    @allure.feature("Корзина")
    @allure.title("Получение информации о товарах в корзине")
    @allure.story("Корзина - Получение короткой информации")
    def test_api_get_cart_short(self) -> None:
        """
        Проверка получения информации о товарах в корзине (/cart/short).
        """
        with allure.step("Отправка запроса на получение информации о товарах в корзине"):
            response = self.client_2.get('cart/short')
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @pytest.mark.api
    @allure.feature("Поиск товаров")
    @allure.title("Поиск товаров по фразе")
    @allure.story("Поиск - Поиск по названию")
    def test_api_search_by_phrase(self, test_data: dict) -> None:
        """
        Поиск по названию.
        """
        phrase_encoded = requests.utils.quote(test_data['search_phrase'])
        with allure.step("Отправка запроса на поиск товаров"):
            response = self.client_1.get('search/facet-search', params={
                'customerCityId': 213,
                'phrase': phrase_encoded,
                'abTestGroup': 1
            })

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @pytest.mark.api
    @allure.feature("Корзина. Добавление товара")
    @allure.title("Добавление товара по валидному ID")
    @allure.story("Корзина - Добавление товара по валидному ID")
    def test_api_add_product_to_cart_valid(self) -> None:
        """
        Добавление товара по валидному ID.
        """
        with allure.step("Отправка запроса на добавление товара в корзину"):
            response = self.client_2.post('cart/product', json={"id": 3111363})

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    @pytest.mark.api
    @allure.feature("Корзина. Добавление товара с некорректным ID")
    @allure.title("Обработка некорректного ID товара")
    @allure.story("Корзина - Добавление товара с некорректным ID")
    def test_api_add_product_invalid_id(self, test_data: dict) -> None:
        """
        Обработка некорректного ID товара.
        """
        with allure.step("Отправка запроса на добавление товара с некорректным ID"):
            response = self.client_2.post('cart/product', json={"id": test_data['invalid_id']})

        with allure.step("Проверка статуса ответа на наличие ошибок"):
            assert response.status_code in [400, 401, 422, 500], f"Unexpected status code: {response.status_code}"

    @pytest.mark.api
    @allure.feature("Поиск книг")
    @allure.title("Поиск книг с некорректным запросом")
    @allure.story("Поиск - Некорректный запрос")
    def test_api_search_with_invalid_query(self) -> None:
        """
        Поиск без phrase — должно вернуть ошибку.
        """
        with allure.step("Отправка запроса на поиск товаров без фразы"):
            response = self.client_1.get('search/facet-search', params={'customerCityId': 213})

        with allure.step("Проверка статуса ответа на наличие ошибок"):
            assert response.status_code in [400, 401, 422, 500], f"Status code: {response.status_code}"

    @pytest.mark.api
    @allure.feature("Добавление с неправильным количеством товара")
    @allure.title("Тест: Добавление товара с некорректным количеством")
    @allure.story("Проверка обработки некорректного количества товаров в корзине")
    def test_api_add_product_with_invalid_quantity(self, test_data: dict) -> None:
        """
        Попытка добавить товар с очень большим или некорректным количеством.

        :param test_data: Данные для теста, содержащие id товара и количество.
        """
    assert 'invalid_id' in test_data, "Ключ 'invalid_id' отсутствует в test_data"
    assert 'invalid_quantity' in test_data, "Ключ 'invalid_quantity' отсутствует в test_data"

    invalid_product_id = test_data['invalid_id']
    invalid_quantity = test_data['invalid_quantity']

    with allure.step("Отправка запроса на добавление товара в корзину с некорректными данными"):
        response = self.client_2.post('cart/product', json={
            "id": invalid_product_id,
            "quantity": invalid_quantity
        })

    with allure.step("Проверка кода ответа"):
        assert response.status_code in [400, 401, 403, 404, 422, 500], (
            f"Ожидался код ответа 400, 401, 403, 404, 422, 500, "
            f"но получен: {response.status_code}"
        )
