from Pages.BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Tuple

class CheckoutPage(BasePage):
    NAME_INPUT: Tuple[str, str] = (By.NAME, "name")
    EMAIL_INPUT: Tuple[str, str] = (By.NAME, "email")
    PHONE_INPUT: Tuple[str, str] = (By.NAME, "phone")
    SUBMIT_BTN: Tuple[str, str] = (By.NAME, "submit")
    CHOOSE_STORE_BTN: Tuple[str, str] = (By.CLASS_NAME, "chg-app-button__content")
    PICKUP_POINT_BTN: Tuple[str, str] = (By.CLASS_NAME, "gtme-rocket-point-info")
    PAYMENT_OPTION: Tuple[str, str] = (By.CLASS_NAME, "payments-item__title")
    
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def fill_form(self, name: str, email: str, phone: str) -> None:
        self.enter_text(self.NAME_INPUT, name)
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PHONE_INPUT, phone)

    def submit_order(self) -> None:
        self.click(self.SUBMIT_BTN)

    def select_store_and_pay(self) -> None:
        self.click(self.CHOOSE_STORE_BTN)
        self.wait.until(EC.element_to_be_clickable(self.PICKUP_POINT_BTN))
        self.click(self.PICKUP_POINT_BTN)
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_OPTION))
        self.click(self.PAYMENT_OPTION)
