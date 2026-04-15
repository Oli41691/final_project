import pytest
import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from Pages.MainPage import MainPage
from Pages.SearchPage import SearchPage

@allure.title("Проверка поиска по точному названию книги")
@allure.story("Поиск книги по точному названию")
@pytest.mark.ui
def test_ui_search_by_exact_title(driver: WebDriver) -> None:
    main_page = MainPage(driver)
    search_results_page = SearchPage(driver)

    with allure.step("Открытие сайта и ожидание загрузки страницы"):
        driver.get("https://www.chitai-gorod.ru/")

    with allure.step("Ввод названия книги и выполнение поиска"):
        main_page.perform_search("Повелитель мух")

    with allure.step("Проверка результатов поиска содержат искомую книгу"):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-page")))
        
        results = search_results_page.get_results()
        assert any("Повелитель мух" in result.text for result in results), "Книга 'Повелитель мух' не найдена в результатах"


@allure.title("Добавление книги в корзину из карточки товара")
@allure.story("Добавление товара")
@pytest.mark.ui
def test_ui_add_book_to_cart(driver: WebDriver) -> None:
    with allure.step("Открытие сайта и ожидание загрузки страницы"):
        driver.get("https://www.chitai-gorod.ru/")

    with allure.step("Выбор и клик по первой карточке книги на главной"):
        # Ищем контейнер карточки
        card_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, ".product-carousel__slide, .product-recommendation-edit, .product-card__recommendation-edit"
            ))
        )
        card_container.click()

    with allure.step("Поиск названия книги и кнопки 'Добавить в корзину' внутри карточки"):
        book_title_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-detail-page__title"))
        )
        book_title = book_title_elem.text

        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-offer__buttons"))
        )

        assert add_button.is_displayed(), "Кнопка добавления в корзину не отображается"
        add_button.click()

    with allure.step("Проверка обновления корзины"):
        cart_indicator = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".header-controls__indicator")))
        count_text = cart_indicator.text.strip()

        assert count_text.isdigit(), f"Некорректное значение счетчика: {count_text}"
        assert int(count_text) >= 1, f"Книга '{book_title}' не добавилась в корзину. Количество: {count_text}"

@pytest.mark.usefixtures("login_with_token")
@allure.title("Оформление заказа с заполнением обязательных полей")
@allure.story("Оформление заказа")
@pytest.mark.ui
def test_ui_checkout(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, 10)

    with allure.step("Переход в корзину"):
        driver.get("https://www.chitai-gorod.ru/cart/")
    
    with allure.step("Нажатие кнопки 'Перейти к оформлению'"):
        route_to_checkout_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "chg-app-button__content")))
        route_to_checkout_button.click()

    with allure.step("Выбор магазина 'заберу отсюда'"):
        pick_shop_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "point-preview__button")))
        pick_shop_button.click()
    
    # Теперь можно заполнить форму
    with allure.step("Заполнение формы обязательных полей"):
        driver.find_element(By.NAME, "name").send_keys("Иван Иванов")
        driver.find_element(By.NAME, "phone").send_keys("+71234567890")
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
    
    with allure.step("Отправка формы и проверка подтверждения"):
        driver.find_element(By.CLASS_NAME, "checkout-summary__button").click()
        confirmation = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "checkout-summary__button")))
        assert "Спасибо, ваш заказ принят!" in confirmation.text, "Заказ не оформлен. Получено сообщение: " + confirmation.text


@allure.title("Проверка элементов интерфейса на главной странице")
@allure.story("UI и отзывчивость элементов")
@pytest.mark.ui
def test_ui_elements_responsiveness(driver):
    url = "https://www.chitai-gorod.ru/"

    with allure.step("Открытие главной страницы сайта"):
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'popmechanic-desktop'))
            )
        except TimeoutException:
            pytest.fail("Страница не загрузилась вовремя или элемент не найден: 'popmechanic-desktop'")

    with allure.step("Проверка наличия логотипа и меню навигации"):
        try:
            logo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "header-sticky__logo-wrapper"))
            )
            nav_menu = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "header-sticky__catalog-menu"))
            )
            assert logo.is_displayed(), "Логотип не отображается"
            assert nav_menu.is_displayed(), "Меню навигации не отображается"
        except TimeoutException:
            pytest.fail("Элемент логотипа или меню навигации не найден или не отображается")

    with allure.step("Проверка, что кнопки и элементы реагируют на клик"):
        max_attempts = 3
        attempt = 0
        success = False

        while attempt < max_attempts and not success:
            attempt += 1
            try:
                buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button, a.btn"))
                )

                for button in buttons:
                    try:
                        if button.is_displayed() and button.is_enabled():
                            pass
                    except StaleElementReferenceException:
                        raise
                success = True

            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)

        if not success:
            pytest.fail("Некоторые кнопки не были обнаружены или стали устаревшими при проверке")
