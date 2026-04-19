from Pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging


class MainPage(BasePage):
    URL: str = "https://www.chitai-gorod.ru/"
    SEARCH_INPUT: tuple = (By.ID, 'app-search')
    SEARCH_BUTTON: tuple = (By.CLASS_NAME, 'search-form__button-search')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def go(self) -> None:
        self.driver.get(self.URL)

    def is_loaded(self) -> WebDriverWait:
        return self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUT))

    def perform_search(self, query: str):
        search_input = WebDriverWait(self.driver, 15).until(
        EC.presence_of_element_located(self.SEARCH_INPUT))
        search_input.send_keys(query)

        search_button = WebDriverWait(self.driver, 20).until(
        EC.visibility_of_element_located(self.SEARCH_BUTTON))
        search_button.click()
    
    def handle_age_confirmation(self, timeout=3) -> None:
        try:
            modal = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-modal-content__content')))
            button = WebDriverWait(self.driver, 1).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'chg-app-button--primary')))
            button.click()
        except TimeoutException:
            logging.info("Модальное окно подтверждения не появилось.")
        except NoSuchElementException:
            logging.info("Кнопка подтверждения не найдена.")
        except Exception as e:
            logging.error(f"Ошибка при обработке подтверждения возраста: {e}")
