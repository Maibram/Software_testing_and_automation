from pathlib import Path

from faker import Faker
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


def main() -> None:
    driver = build_driver()
    wait = WebDriverWait(driver, 10)
    page = Path("page1_contact_login_registration.html").resolve().as_uri()

    try:
        driver.get(page)

        wait.until(EC.visibility_of_element_located((By.ID, "contactName"))).send_keys(fake.name())
        driver.find_element(By.ID, "contactEmail").send_keys(fake.email())
        driver.find_element(By.ID, "contactSubject").send_keys("Feedback")
        driver.find_element(By.ID, "contactMessage").send_keys("This is a Selenium validation message.")
        driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
        contact_status = wait.until(EC.visibility_of_element_located((By.ID, "contactStatus"))).text
        assert "Contact form submitted successfully." in contact_status
        print("Contact form submission verified.")

        driver.get(page)
        wait.until(EC.visibility_of_element_located((By.ID, "loginEmail"))).send_keys("invalid@example.com")
        driver.find_element(By.ID, "loginPassword").send_keys("wrongpass")
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        login_error = wait.until(EC.visibility_of_element_located((By.ID, "loginError"))).text
        assert "incorrect" in login_error.lower()
        print("Invalid login error verified.")

        driver.get(page)
        wait.until(EC.visibility_of_element_located((By.ID, "regName"))).send_keys(fake.name())
        driver.find_element(By.ID, "regEmail").send_keys(fake.email())
        driver.find_element(By.ID, "regPassword").send_keys("StrongPass@123")
        driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
        register_status = wait.until(EC.visibility_of_element_located((By.ID, "registerStatus"))).text
        assert "Account Created!" in register_status
        print("Registration verified.")

        driver.get(page)
        email_field = wait.until(EC.visibility_of_element_located((By.ID, "regEmail")))
        email_field.clear()
        email_field.send_keys("bad-email")
        email_field.send_keys(" ")
        validation_message = driver.execute_script("return arguments[0].validationMessage;", email_field)
        assert validation_message.strip() != ""
        print("Email validation verified.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
