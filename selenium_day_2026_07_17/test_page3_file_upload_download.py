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
    page = Path("page3_file_upload_download.html").resolve().as_uri()

    valid_file = Path("valid_upload.png")
    valid_file.write_text("fake PNG content", encoding="utf-8")

    invalid_file = Path("invalid_upload.txt")
    invalid_file.write_text("invalid file content", encoding="utf-8")

    try:
        driver.get(page)

        upload_input = wait.until(EC.visibility_of_element_located((By.ID, "fileInput")))
        upload_input.send_keys(str(valid_file.resolve()))
        driver.find_element(By.XPATH, "//button[contains(text(),'Upload')]").click()
        valid_status = wait.until(EC.visibility_of_element_located((By.ID, "uploadStatus"))).text
        assert "Valid file uploaded successfully." in valid_status
        print("Valid file upload verified.")

        upload_input.clear()
        upload_input.send_keys(str(invalid_file.resolve()))
        driver.find_element(By.XPATH, "//button[contains(text(),'Upload')]").click()
        invalid_status = wait.until(EC.visibility_of_element_located((By.ID, "uploadStatus"))).text
        assert "Unsupported file format rejected." in invalid_status
        print("Unsupported file rejection verified.")

        download_link = driver.find_element(By.ID, "downloadLink")
        assert download_link.get_attribute("href").endswith("sample_download.txt")
        print("Download link verified.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
