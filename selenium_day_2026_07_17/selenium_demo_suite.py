from __future__ import annotations

import os
import re
import time
from pathlib import Path

from faker import Faker
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

fake = Faker()


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def create_fake_excel(output_file: str = "fake_user_data.xlsx") -> str:
    wb = Workbook()
    ws = wb.active
    ws.title = "FakeUsers"
    ws.append(["Name", "Email", "Phone", "Address", "Company"])

    for _ in range(10):
        ws.append([
            fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.address(),
            fake.company(),
        ])

    wb.save(output_file)
    print(f"Fake workbook created: {output_file}")
    return output_file


def verify_contact_form(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get(Path("automation_demo.html").resolve().as_uri())

    wait.until(EC.visibility_of_element_located((By.ID, "contactName"))).send_keys(fake.name())
    driver.find_element(By.ID, "contactEmail").send_keys(fake.email())
    driver.find_element(By.ID, "contactSubject").send_keys("Feedback")
    driver.find_element(By.ID, "contactMessage").send_keys("Message for Selenium validation.")
    driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()

    status_text = wait.until(EC.visibility_of_element_located((By.ID, "contactStatus"))).text
    assert "submitted successfully" in status_text.lower()
    print("Contact form submission verified.")


def verify_invalid_login(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get(Path("automation_demo.html").resolve().as_uri())

    wait.until(EC.visibility_of_element_located((By.ID, "loginEmail"))).send_keys("invalid@example.com")
    driver.find_element(By.ID, "loginPassword").send_keys("wrongpass")
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()

    error_text = wait.until(EC.visibility_of_element_located((By.ID, "loginError"))).text
    assert "incorrect" in error_text.lower()
    print("Invalid login error verified.")


def verify_registration(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get(Path("automation_demo.html").resolve().as_uri())

    wait.until(EC.visibility_of_element_located((By.ID, "regName"))).send_keys(fake.name())
    driver.find_element(By.ID, "regEmail").send_keys(fake.email())
    driver.find_element(By.ID, "regPassword").send_keys("StrongPass@123")
    driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()

    status_text = wait.until(EC.visibility_of_element_located((By.ID, "registerStatus"))).text
    assert "Account Created!" in status_text
    print("Registration verified.")


def verify_email_validation(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get(Path("automation_demo.html").resolve().as_uri())

    email_field = wait.until(EC.visibility_of_element_located((By.ID, "regEmail")))
    email_field.clear()
    email_field.send_keys("bad-email")
    email_field.send_keys(" ")

    validation_message = driver.execute_script("return arguments[0].validationMessage;", email_field)
    assert validation_message.strip() != ""
    print("Email format validation verified.")


def verify_product_filter_and_cart(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get(Path("automation_demo.html").resolve().as_uri())

    price_slider = wait.until(EC.visibility_of_element_located((By.ID, "priceFilter")))
    category_filter = driver.find_element(By.ID, "categoryFilter")
    category_filter.send_keys("electronics")
    driver.execute_script("arguments[0].value = 100; arguments[0].dispatchEvent(new Event('input'));", price_slider)

    visible_products = driver.find_elements(By.CSS_SELECTOR, ".product:not(.hidden)")
    assert len(visible_products) >= 1

    visible_add_buttons = driver.find_elements(By.CSS_SELECTOR, ".product:not(.hidden) .addToCart")
    assert len(visible_add_buttons) >= 1

    for _ in range(2):
        visible_add_buttons[0].click()
        time.sleep(0.5)
        visible_add_buttons = driver.find_elements(By.CSS_SELECTOR, ".product:not(.hidden) .addToCart")

    cart_rows = driver.find_elements(By.CSS_SELECTOR, "#cartBody tr")
    assert len(cart_rows) >= 1

    qty_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".qtyInput")))
    driver.execute_script("arguments[0].value = 3; arguments[0].dispatchEvent(new Event('change'));", qty_input)

    total_text = wait.until(EC.visibility_of_element_located((By.ID, "cartTotal"))).text
    assert "$" in total_text
    print("Product filtering and cart quantity update verified.")


def verify_file_upload_and_download(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get(Path("automation_demo.html").resolve().as_uri())

    upload_input = wait.until(EC.visibility_of_element_located((By.ID, "fileInput")))
    valid_file = Path("valid_upload.png")
    valid_file.write_text("fake png data", encoding="utf-8")
    upload_input.send_keys(str(valid_file.resolve()))
    driver.find_element(By.XPATH, "//button[contains(text(),'Upload')]").click()
    upload_status = wait.until(EC.visibility_of_element_located((By.ID, "uploadStatus"))).text
    assert "Valid file uploaded successfully." in upload_status

    invalid_file = Path("invalid_upload.txt")
    invalid_file.write_text("invalid", encoding="utf-8")
    upload_input.clear()
    upload_input.send_keys(str(invalid_file.resolve()))
    driver.find_element(By.XPATH, "//button[contains(text(),'Upload')]").click()
    upload_status = wait.until(EC.visibility_of_element_located((By.ID, "uploadStatus"))).text
    assert "Unsupported file format rejected." in upload_status

    download_link = driver.find_element(By.ID, "downloadLink")
    assert download_link.get_attribute("href").endswith("sample_download.txt")
    print("File upload and download verification passed.")


def main() -> None:
    create_fake_excel()
    driver = build_driver()
    try:
        verify_contact_form(driver)
        verify_invalid_login(driver)
        verify_registration(driver)
        verify_email_validation(driver)
        verify_product_filter_and_cart(driver)
        verify_file_upload_and_download(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
