from selenium.webdriver.common.by import By
from Pages.BasePage import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List

class SearchPage(BasePage):
    RESULT_ITEMS: Tuple[str, str] = (By.CSS_SELECTOR, '[type="submit"]')

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_results(self) -> List[WebElement]:
        return self.wait.until(EC.visibility_of_all_elements_located(self.RESULT_ITEMS))

    def is_book_in_results(self, title: str) -> bool:
        results = self.get_results()
        for item in results:
            classes_to_check = ['product-item__title', 'search-title__head', 'search-title__sub', 'app-page-container']
        for class_name in classes_to_check:
            try:
                element = item.find_element(By.CLASS_NAME, class_name)
                item_title = element.text
                if title.lower() in item_title.lower():
                    return True
            except NoSuchElementException:
                continue
        return False

    def open_first_result(self) -> None:
        results = self.get_results()
        if results:
            results[0].click()
