import allure
import pytest
from Pages.api_client import ApiClient
from config import BASE_URL, URL_2

client = ApiClient(base_url=BASE_URL)

@allure.story("Добавление товара с неверным ID")
@allure.title("Проверка ошибки при добавлении товара с неправильным ID")
@pytest.mark.api
def test_add_product_with_invalid_id():
    with allure.step("Отправляем POST-запрос с неверным ID товара"):
        try:
            response = client.product_to_cart(product_id="1ks12nmd")
            assert response.get("status_code", 200) >= 400, \
                f"Expected error status, got: {response}"
        except Exception as e:
            assert "40" in str(e) or "50" in str(e), f"Unexpected error: {e}"

@allure.story("Получение информации о товарах в корзине")
@allure.title("Проверка успешного получения корзины")
@pytest.mark.api
def test_get_cart_info():
    with allure.step("Запрашиваем список товаров в корзине"):
        response = client.get_cart_info()
    with allure.step("Проверяем что ответ содержит ожидаемую структуру"):
        assert isinstance(response, dict), f"Expected dict, got {type(response)}"
        assert "data" in response, "Response should contain 'data' key"
        data = response["data"]
        assert "items" in data, "Data should contain 'items' key"
        assert isinstance(data["items"], list), "'items' should be a list"

@allure.story("Поиск по названию")
@allure.title("Поиск товара по фразе с правильными параметрами")
@pytest.mark.api
def test_search_product():
    client = ApiClient(URL_2)
    city_id = 213
    phrase = "в плену синих роз"
    ab_test_group = "1"
    page = 1
    per_page = 60

    with allure.step("Отправляем GET запрос к поиску"):
        response = client.search_product(
            city_id=city_id,
            phrase=phrase,
            ab_test_group=ab_test_group,
            page=page,
            per_page=per_page
        )

    with allure.step("Проверяем структуру ответа поиска"):
        assert isinstance(response, dict), f"Expected dict, got {type(response)}"
        assert "data" in response, "Response should contain 'data' key"
        if "data" in response and response["data"]:
            assert isinstance(response["data"], list), "Data key should be a list"
            for item in response["data"]:
                assert isinstance(item, dict), "Each item should be a dict"

@allure.story("Добавление товара в корзину")
@allure.title("Добавление товара по ID")
@pytest.mark.api
def test_add_product_valid():
    product_id = "3111363"
    
    with allure.step("Отправляем POST-запрос для добавления товара в корзину"):
        try:
            response = client.product_to_cart(product_id=product_id)
        except Exception as e:
            pytest.fail(f"Unexpected error when adding valid product: {e}")

    with allure.step("Проверяем успешный ответ"):
        assert isinstance(response, dict), f"Expected dict, got {type(response)}"
        assert response.get("success", False) or "id" in response, \
            "Add product response should indicate success or contain product id"

@allure.story("Поиск книги с невалидным запросом")
@allure.title("Поиск книги без фразы, ожидаем ошибку")
@pytest.mark.api
def test_search_without_phrase():
    with allure.step("Отправляем GET без параметра phrase"):
        try:
            response = client.search_product(
                city_id=213, 
                phrase="", 
                ab_test_group=""
            )
            assert response.get("error") is not None or response.get("status_code", 200) >= 400, \
                f"Expected error indication, got: {response}"
                
        except Exception as e:
            assert "40" in str(e) or "50" in str(e) or "empty" in str(e).lower(), \
                f"Unexpected error type: {e}"

@allure.story("Оформление заказа с невалидным ID города")
@allure.title("Проверка ошибки при неправильном cityID")
@pytest.mark.api
def test_checkout_with_invalid_city_id():
    invalid_city_id = "1ола61"
    
    with allure.step("Отправляем GET запрос на оформление заказа с неправильным cityID"):
        try:
            response = client.checkout(
                city_id=invalid_city_id,
                shipment_type="pickup",
                user_type="individual",
                order_type="order"
            )
            assert response.get("error") is not None or response.get("status_code", 200) >= 400, \
                f"Expected error for invalid city ID, got: {response}"
                
        except Exception as e:
            assert "40" in str(e) or "50" in str(e) or "invalid" in str(e).lower(), \
                f"Unexpected error type: {e}"

@allure.story("Добавление товара с невалидным количеством")
@allure.title("Проверка ошибки при запросе с большим количеством")
@pytest.mark.api
def test_add_product_with_invalid_quantity():
    product_id = "3111363"
    quantity = 1000000
    
    with allure.step("Отправляем POST-запрос с очень большим количеством товара"):
        try:
            response = client.product_to_cart(
                product_id=product_id, 
                quantity=quantity
            )
            assert response.get("error") is not None or response.get("status_code", 200) >= 400, \
                f"Expected error for invalid quantity, got: {response}"
                
        except Exception as e:
            assert "40" in str(e) or "50" in str(e) or "quantity" in str(e).lower(), \
                f"Unexpected error type: {e}"

@allure.story("Проверка работы API без авторизации")
@allure.title("Запрос без токена авторизации")
@pytest.mark.api
def test_api_without_authentication():
    with allure.step("Создаем клиент без токена авторизации"):
        unauth_client = ApiClient(base_url=BASE_URL, token=None)
    
    with allure.step("Пытаемся получить информацию о корзине"):
        try:
            response = unauth_client.get_cart_info()
            assert isinstance(response, dict), f"Expected dict, got {type(response)}"
            
        except Exception as e:
            assert "401" in str(e) or "403" in str(e) or "auth" in str(e).lower(), \
                f"Unexpected error for unauthenticated request: {e}"
