import pytest
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import BASE_URL, ACCESS_TOKEN, REFRESH_TOKEN
from Pages.api_client import ApiClient

@pytest.fixture(scope='session')
def api_urls():
    return {
        'API_1': BASE_URL,
    }

@pytest.fixture(scope='session')
def api_client():
    """Fixture для API клиента"""
    client = ApiClient(base_url=BASE_URL, token=ACCESS_TOKEN)
    yield client
    client.close()

@pytest.fixture(scope='session')
def authenticated_session():
    """Fixture для аутентифицированной сессии"""
    session = requests.Session()
    if ACCESS_TOKEN:
        session.headers.update({'Authorization': f'Bearer {ACCESS_TOKEN}'})
    yield session
    session.close()

@pytest.fixture(scope='function')
def driver():
    """Fixture для веб-драйвера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope='function')
def login_with_token(driver):
    """Fixture для логина через токены"""
    driver.get('https://www.chitai-gorod.ru/')
    if ACCESS_TOKEN:
        driver.add_cookie({'name': 'access_token', 'value': ACCESS_TOKEN})
    if REFRESH_TOKEN:
        driver.add_cookie({'name': 'refresh_token', 'value': REFRESH_TOKEN})
    driver.refresh()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'app-search')))

@pytest.fixture(scope='function')
def authenticated_driver(driver):
    login_with_token(driver)
    return driver
