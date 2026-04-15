from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple

class ProductPage(BasePage):
    PRODUCT_TITLE: Tuple[str, str] = (By.TAG_NAME, 'h1')
    ADD_TO_CART_BTN: Tuple[str, str] = (By.CLASS_NAME, 'product-buy__button')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_title(self) -> str:
        return self.get_text(self.PRODUCT_TITLE)

    def add_to_cart(self) -> None:
        self.click(self.ADD_TO_CART_BTN)
