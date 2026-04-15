from Pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

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
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)