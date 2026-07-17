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
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


def generate_fake_workbook(output_path: str = "fake_user_data.xlsx") -> str:
    wb = Workbook()
    ws = wb.active
    ws.title = "Users"
    ws.append(["Full Name", "Email", "Phone", "Password", "Address"])

    for _ in range(10):
        ws.append([
            fake.name(),
            fake.email(),
            fake.phone_number(),
            fake.password(length=10),
            fake.address(),
        ])

    wb.save(output_path)
    print(f"Fake data workbook created at: {output_path}")
    return output_path


def verify_contact_form_submission(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.automationexercise.com/contact_us")

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='name']"))).send_keys(fake.name())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='email']").send_keys(fake.email())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='subject']").send_keys("Automation Test Feedback")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='message']").send_keys("This is a Selenium verification message.")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='submit-button']").click()

    alert = wait.until(EC.alert_is_present())
    alert.accept()

    status_text = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "status"))).text
    assert "Success" in status_text or "success" in status_text.lower()
    print("Contact form submission verified successfully.")


def verify_invalid_login_error(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.automationexercise.com/login")

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='login-email']"))).send_keys(fake.email())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='login-password']").send_keys("wrongpassword")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='login-button']").click()

    error = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Your email or password is incorrect!')]")))
    assert error.is_displayed()
    print("Invalid login credentials error verified.")


def verify_registration_with_valid_data(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.automationexercise.com/")

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[href='/login']"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='signup-name']"))).send_keys(fake.name())
    email_input = driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-email']")
    email_input.send_keys(fake.unique.email())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-button']").click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='account-create']")))
    driver.find_element(By.ID, "id_gender1").click()
    driver.find_element(By.CSS_SELECTOR, "[data-qa='name']").clear()
    driver.find_element(By.CSS_SELECTOR, "[data-qa='name']").send_keys(fake.name())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='email']").clear()
    driver.find_element(By.CSS_SELECTOR, "[data-qa='email']").send_keys(fake.unique.email())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='password']").send_keys("StrongPass@123")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='days']").send_keys("10")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='months']").send_keys("January")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='years']").send_keys("1995")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='first_name']").send_keys(fake.first_name())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='last_name']").send_keys(fake.last_name())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='company']").send_keys(fake.company())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='address']").send_keys(fake.address())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='country']").send_keys("India")
    driver.find_element(By.CSS_SELECTOR, "[data-qa='state']").send_keys(fake.state())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='city']").send_keys(fake.city())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='zipcode']").send_keys(fake.postcode())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='mobile_number']").send_keys(fake.phone_number())
    driver.find_element(By.CSS_SELECTOR, "[data-qa='create-account']").click()

    success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='account-created']"))).text
    assert "Account Created!" in success_message
    print("Registration with valid data verified.")


def verify_email_format_validation(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.automationexercise.com/login")

    email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-qa='signup-email']")))
    email_input.clear()
    email_input.send_keys("invalid-email")
    password_input = driver.find_element(By.CSS_SELECTOR, "[data-qa='signup-name']")
    password_input.click()

    validation_message = driver.execute_script(
        "return arguments[0].validationMessage;",
        email_input,
    )
    assert validation_message.strip() != ""
    print("Email format validation checked successfully.")


def verify_product_filter_and_cart(driver: webdriver.Chrome) -> None:
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.automationexercise.com/products")

    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "features_items")))
    driver.find_element(By.XPATH, "//a[contains(text(),'Women')]" ).click()
    time.sleep(2)

    cards = driver.find_elements(By.CSS_SELECTOR, ".product-image-wrapper")
    assert len(cards) >= 2

    for product in cards[:2]:
        product.find_element(By.XPATH, ".//a[contains(text(),'Add to cart')]").click()
        time.sleep(1)

    driver.find_element(By.XPATH, "//u[contains(text(),'View Cart')]" ).click()

    rows = driver.find_elements(By.CSS_SELECTOR, "#cart_info_table tbody tr")
    assert len(rows) >= 2

    total_value = 0.0
    for row in rows[:2]:
        quantity = int(row.find_element(By.CSS_SELECTOR, ".cart_quantity_input").get_attribute("value"))
        unit_price_text = row.find_element(By.CSS_SELECTOR, ".cart_price").text.replace("Rs. ", "").replace(",", "")
        unit_price = float(unit_price_text)
        total_value += unit_price * quantity

    displayed_total = float(driver.find_element(By.CSS_SELECTOR, ".cart_total_price").text.replace("Rs. ", "").replace(",", ""))
    assert round(total_value, 2) == round(displayed_total, 2)

    quantity_input = rows[0].find_element(By.CSS_SELECTOR, ".cart_quantity_input")
    quantity_input.clear()
    quantity_input.send_keys("3")
    driver.find_element(By.CSS_SELECTOR, "[class='btn btn-default check_out']").click()
    time.sleep(1)

    updated_quantity = int(rows[0].find_element(By.CSS_SELECTOR, ".cart_quantity_input").get_attribute("value"))
    assert updated_quantity == 3
    print("Product filtering and cart calculation verified.")


def verify_file_upload_and_download() -> None:
    workspace = Path(__file__).resolve().parent
    demo_path = workspace / "upload_download_demo.html"
    sample_file = workspace / "sample_download.txt"
    sample_file.write_text("This is a sample download file for Selenium verification.", encoding="utf-8")

    valid_upload = workspace / "valid_upload.png"
    valid_upload.write_text("fake PNG content", encoding="utf-8")

    invalid_upload = workspace / "invalid_upload.txt"
    invalid_upload.write_text("bad extension", encoding="utf-8")

    driver = build_driver()
    try:
        driver.get(demo_path.as_uri())
        wait = WebDriverWait(driver, 10)

        upload_input = wait.until(EC.visibility_of_element_located((By.ID, "fileInput")))
        upload_input.send_keys(str(valid_upload))
        driver.find_element(By.XPATH, "//button[contains(text(),'Upload')]").click()
        status = wait.until(EC.visibility_of_element_located((By.ID, "uploadStatus"))).text
        assert "Valid file uploaded successfully." in status

        upload_input.clear()
        upload_input.send_keys(str(invalid_upload))
        driver.find_element(By.XPATH, "//button[contains(text(),'Upload')]").click()
        status = wait.until(EC.visibility_of_element_located((By.ID, "uploadStatus"))).text
        assert "Unsupported file format rejected." in status

        download_link = driver.find_element(By.ID, "downloadLink")
        download_url = download_link.get_attribute("href")
        assert download_url.endswith("sample_download.txt")
        print("File upload and rejection verification passed.")
    finally:
        driver.quit()


def main() -> None:
    generate_fake_workbook()
    driver = build_driver()
    try:
        verify_contact_form_submission(driver)
        verify_invalid_login_error(driver)
        verify_registration_with_valid_data(driver)
        verify_email_format_validation(driver)
        verify_product_filter_and_cart(driver)
    finally:
        driver.quit()

    verify_file_upload_and_download()


if __name__ == "__main__":
    main()
