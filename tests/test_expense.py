import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

BASE_URL = "http://127.0.0.1:8003"


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()


def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text


def test_home_page_loads(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL + "/")
    assert driver.title == "Expenses"
    assert driver.find_element(By.ID, "total").text.startswith("₹")


def test_summary_page_loads(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL + "/summary")
    assert driver.title == "Summary"


def test_empty_title(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL + "/add")

    driver.find_element(By.NAME, "title").clear()
    driver.find_element(By.NAME, "amount").send_keys("150")
    Select(driver.find_element(By.NAME, "category")).select_by_visible_text("Food")
    driver.find_element(By.NAME, "sb").click()

    time.sleep(2)
    assert get_alert_text(driver) == "Title cannot be empty"


def test_invalid_amount(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL + "/add")

    driver.find_element(By.NAME, "title").send_keys("Bus pass")
    driver.find_element(By.NAME, "amount").send_keys("-20")
    Select(driver.find_element(By.NAME, "category")).select_by_visible_text("Travel")
    driver.find_element(By.NAME, "sb").click()

    time.sleep(2)
    assert get_alert_text(driver) == "Amount must be greater than 0"


def test_no_category(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL + "/add")

    driver.find_element(By.NAME, "title").send_keys("Movie")
    driver.find_element(By.NAME, "amount").send_keys("200")
    driver.find_element(By.NAME, "sb").click()

    time.sleep(2)
    assert get_alert_text(driver) == "Please select a category"


def test_valid_expense(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL + "/add")

    driver.find_element(By.NAME, "title").send_keys("Lunch")
    driver.find_element(By.NAME, "amount").send_keys("120")
    Select(driver.find_element(By.NAME, "category")).select_by_visible_text("Food")
    driver.find_element(By.NAME, "sb").click()

    time.sleep(2)

    current_url = driver.current_url
    assert "/submit" in current_url, f"Expected /submit, but got: {current_url}"

    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Expense saved: Lunch for ₹120.00 under Food." in body_text, f"Success message not found: {body_text}"

    # The new expense should now appear on the home page
    driver.get(BASE_URL + "/")
    assert "Lunch" in driver.find_element(By.TAG_NAME, "table").text
