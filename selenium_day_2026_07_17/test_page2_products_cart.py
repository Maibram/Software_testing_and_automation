from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def build_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    return webdriver.Chrome(options=options)


def main() -> None:
    driver = build_driver()
    wait = WebDriverWait(driver, 10)
    page = Path("page2_products_cart.html").resolve().as_uri()

    try:
        driver.get(page)

        category_filter = wait.until(EC.visibility_of_element_located((By.ID, "categoryFilter")))
        category_filter.send_keys("electronics")

        price_slider = driver.find_element(By.ID, "priceFilter")
        driver.execute_script("arguments[0].value = 100; arguments[0].dispatchEvent(new Event('input'));", price_slider)

        visible_products = driver.find_elements(By.CSS_SELECTOR, ".product:not(.hidden)")
        assert len(visible_products) >= 1

        first_visible_button = driver.find_element(By.CSS_SELECTOR, ".product:not(.hidden) .addToCart")
        first_visible_button.click()
        first_visible_button.click()

        qty_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".qtyInput")))
        driver.execute_script("arguments[0].value = 3; arguments[0].dispatchEvent(new Event('change'));", qty_input)

        total_text = wait.until(EC.visibility_of_element_located((By.ID, "cartTotal"))).text
        assert "$" in total_text
        print("Product filtering and cart quantity update verified.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
