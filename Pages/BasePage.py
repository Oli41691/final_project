from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple, Any

class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(self.driver, 10)

    def find(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """
        Находит элемент по локатору с ожиданием.
        :param locator: tuple, например (By.ID, 'element_id')
        :param timeout: время ожидания
        :return: WebElement
        """
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Элемент по локатору {locator} не найден за {timeout} секунд"
        )

    def click(self, locator: Tuple[str, str]) -> None:
        """
        Кликает по элементу
        :param locator: tuple
        """
        element = self.find(locator)
        element.click()

    def enter_text(self, locator: Tuple[str, str], text: str) -> None:
        """
        Вводит текст в поле
        :param locator: tuple
        :param text: str
        """
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Проверяет видимость элемента
        :param locator: tuple
        :param timeout: время ожидания
        :return: bool
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: int = 10) -> None:
        """
        Ждет, пока элемент станет кликабельным
        """
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал кликабельным за {timeout} секунд"
        )

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """
        Скроллит страницу до элемента
        """
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_text(self, locator: Tuple[str, str]) -> str:
        element = self.find(locator)
        return element.text
