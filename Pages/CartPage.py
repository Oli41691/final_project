from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from Pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import List

class CartPage(BasePage):
    CART_ITEMS: Tuple[str, str] = (By.CLASS_NAME, 'chg-app-button')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def open(self) -> None:
        self.click(self.CART_ITEMS)

    def get_items_count(self) -> int:
        items: List[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
        return len(items)

    def is_item_in_cart(self, title: str) -> bool:
        items: List[WebElement] = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
        for item in items:
            item_title: str = item.find_element(By.CLASS_NAME, 'cart-item__title').text
            if title.lower() in item_title.lower():
                return True
        return False
