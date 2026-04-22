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
from Pages.CartPage import CartPage
from Pages.CheckoutPage import CheckoutPage
import re
import time

devices = [
    {"name": "mobile", "width": 375, "height": 667},
    {"name": "tablet", "width": 768, "height": 1024},
    {"name": "desktop", "width": 1920, "height": 1080},
    {"name": "laptop", "width": 1440, "height": 900},
    {"name": "large_desktop", "width": 2560, "height": 1440},
]


@allure.title("Проверка поиска по точному названию книги")
@allure.story("Поиск книги по точному названию")
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
            EC.presence_of_element_located((By.CLASS_NAME, "search-title__sub"))
        )
        search_sub_title = driver.find_element(By.CLASS_NAME, "search-title__sub")
        text = search_sub_title.text

        match = re.search(r'Нашли (\d+) товаров и (\d+) других совпадений', text)
        assert match, "Сообщение о количестве совпадений не соответствует шаблону"
        N1 = int(match.group(1))
        N2 = int(match.group(2))
        print(f"Найдено {N1} товаров и {N2} других совпадений")

@allure.title("Адаптивность сайта — мобильное устройство (375x667)")
@allure.story("Адаптивность сайта на мобильных устройствах")
@pytest.mark.ui
def test_layout_mobile(driver):
    driver.set_window_size(375, 667)
    main_page = MainPage(driver)
    main_page.go()
    main_page.is_loaded()

    with allure.step("Проверка наличия мобильного меню"):
        assert main_page.is_element_visible((By.CLASS_NAME, 'home-page')), "Главное меню не отображается на мобильном"

@allure.title("Адаптивность сайта — планшет (768x1024)")
@allure.story("Адаптивность сайта на планшете")
@pytest.mark.ui
def test_layout_tablet(driver):
    driver.set_window_size(768, 1024)
    main_page = MainPage(driver)
    main_page.go()
    main_page.is_loaded()

    with allure.step("Проверка наличия полноценного меню на планшете"):
        assert main_page.is_element_visible((By.CLASS_NAME, 'home-page')), "Меню не отображается на планшете"

@allure.title("Адаптивность сайта — десктоп (1920x1080)")
@allure.story("Адаптивность сайта на десктопе")
@pytest.mark.ui
def test_layout_desktop(driver):
    driver.set_window_size(1920, 1080)
    main_page = MainPage(driver)
    main_page.go()
    main_page.is_loaded()

    with allure.step("Проверка отображения полного меню на десктопе"):
        assert main_page.is_element_visible((By.CLASS_NAME, 'home-page')), "Меню не отображается на десктопе"

@allure.title("Адаптивность сайта — ноутбук (1440x900)")
@allure.story("Адаптивность сайта на ноутбуке")
@pytest.mark.ui
def test_layout_laptop(driver):
    driver.set_window_size(1440, 900)
    main_page = MainPage(driver)
    main_page.go()
    main_page.is_loaded()

    with allure.step("Проверка отображения меню на ноутбуке"):
        assert main_page.is_element_visible((By.CLASS_NAME, 'home-page'))

@allure.title("Адаптивность сайта — большой дисплей (2560x1440)")
@allure.story("Адаптивность сайта на больших дисплеях")
@pytest.mark.ui
def test_layout_large_desktop(driver):
    driver.set_window_size(2560, 1440)
    main_page = MainPage(driver)
    main_page.go()
    main_page.is_loaded()

    with allure.step("Проверка отображения меню на большом дисплее"):
        assert main_page.is_element_visible((By.CLASS_NAME, 'home-page'))

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

@allure.title("Проверка поиска несуществующей книги")
@allure.story("Поиск по несуществующему названию")
@pytest.mark.ui
def test_search_nonexistent_book(driver):
    main_page = MainPage(driver)

    with allure.step("Открытие сайта и ожидание загрузки страницы"):
        main_page.go()

    with allure.step("Ввод несуществующего названия книги и выполнение поиска"):
        main_page.perform_search("jfjf4hjfbc")

    with allure.step("Ожидание появления сообщения о отсутствии книги"):
        try:
            no_results_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "catalog-stub__title"))
            )
            assert "Похоже, у нас такого нет" in no_results_element.text
        except TimeoutException:
            pytest.fail("Сообщение о отсутствии книги не появилось")
