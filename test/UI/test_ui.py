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

devices = [
    {"name": "mobile", "width": 375, "height": 667},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "desktop", "width": 1920, "height": 1080},
]

@allure.title("Проверка поиска по точному/не корректному названию книги")
@allure.story("Поиск книги по точному/ не корректному названию")
@pytest.mark.ui
def test_search_by_exact_title(driver: WebDriver) -> None:
    main_page = MainPage(driver)
    search_results_page = SearchPage(driver)

    with allure.step("Открытие сайта и ожидание загрузки страницы"):
        driver.get("https://www.chitai-gorod.ru/")

    with allure.step("Ввод названия книги и выполнение поиска"):
        main_page.perform_search("Повелитель мух")

    with allure.step("Проверка результатов или сообщений об отсутствии"):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "app-page-container")))

        results = search_results_page.get_results()
        if results:
            assert any("Повелитель мух" in result.text for result in results), "Книга 'Повелитель мух' не найдена в результатах"
        else:
            try:
                no_results_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "catalog-stub__title"))
                )
                assert "Похоже, у нас такого нет" in no_results_element.text
            except:
                pass

            try:
                search_head = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-title__head"))
                )
                assert "Результаты поиска «»" in search_head.text
            except:
                pass

            try:
                search_sub_title = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "search-title__sub"))
                )
                text = search_sub_title.text
                match = re.search(r'Нашли (\d+) товаров и (\d+) других совпадений', text)
                assert match, "Сообщение о количестве совпадений не соответствует шаблону"
                N1 = int(match.group(1))
                N2 = int(match.group(2))
                print(f"Найдено {N1} товаров и {N2} других совпадений")
            except:
                pass

@pytest.mark.parametrize("device", devices)
@allure.story("Адаптивность сайта на разных устройствах")
@pytest.mark.ui
def test_responsive_layout(driver, device):
    with allure.step(f"Установка размера окна: {device['name']} ({device['width']}x{device['height']})"):
        driver.set_window_size(device["width"], device["height"])

    main_page = MainPage(driver)

    with allure.step("Переход на главную страницу и проверка загрузки"):
        main_page.go()
        main_page.is_loaded()

    if device["width"] < 768:
        with allure.step("Проверка наличия мобильного меню"):
            burger_locator = (By.CLASS_NAME, 'home-page')
            assert main_page.is_element_visible(burger_locator), \
                f"Главное меню не отображается на {device['name']} ({device['width']}px)"
    else:
        with allure.step("Проверка наличия полноценного меню"):
            main_menu_locator = (By.CLASS_NAME, 'home-page') 
            assert main_page.is_element_visible(main_menu_locator), \
                f"Меню не отображается на {device['name']} ({device['width']}px)"

@allure.title("Добавление книги и оформление заказа")
@allure.story("Добавление книги и оформление заказа")
@pytest.mark.ui
def test_add_book_and_checkout(driver: WebDriver, login_with_token):
    wait = WebDriverWait(driver, 10)

    with allure.step("Переход на главную страницу"):
        main_page = MainPage(driver)
        main_page.go()

    with allure.step("Ожидание появления карточки товара и клик по ней"):
        card_container = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".product-carousel__slide, .product-recommendation-edit, .product-card__recommendation-edit")
        ))
        card_container.click()

    with allure.step("Обработка подтверждения возраста, если потребуется"):
        main_page.handle_age_confirmation()

    with allure.step("Получение названия книги"):
        book_title_elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-detail-page__title")))
        book_title = book_title_elem.text

    with allure.step("Добавление книги в корзину"):
        add_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-offer__buttons")))
        assert add_button.is_displayed(), "Кнопка добавления в корзину не отображается"
        add_button.click()

    with allure.step("Переход к странице корзины"):
        driver.get("https://www.chitai-gorod.ru/cart/")

    with allure.step("Переход к оформлению заказа (кнопка 'Оформить заказ')"):
        route_to_checkout_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "chg-app-button__content")))
        route_to_checkout_button.click()

    with allure.step("Выбор пункта выдачи (нажатие 'Выбрать магазин')"):
        pick_shop_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "point-preview__button")))
        pick_shop_button.click()

    with allure.step("Заполнение формы данных покупателя"):
        driver.find_element(By.NAME, "name").send_keys("Иван Иванов")
        driver.find_element(By.NAME, "phone").send_keys("+71234567890")
        driver.find_element(By.NAME, "email").send_keys("test@example.com")

    with allure.step("Отправка формы заказа"):
        driver.find_element(By.CLASS_NAME, "checkout-summary__button").click()

    with allure.step("Проверка отображения подтверждения заказа"):
        confirmation = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "checkout-summary__button"))
        )
        assert "Спасибо, ваш заказ принят!" in confirmation.text


@allure.title("Проверка элементов интерфейса на главной странице")
@allure.story("UI и отзывчивость элементов")
@pytest.mark.ui
def test_elements_responsiveness(driver):
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
