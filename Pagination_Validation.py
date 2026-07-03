from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Launch Chrome
driver = webdriver.Chrome()
driver.maximize_window()

# Open the webpage
driver.get("https://datatables.net/examples/data_sources/ajax.html")

wait = WebDriverWait(driver, 15)

# Wait until the table is loaded
wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#example tbody tr"))
)

# -------------------- PAGE 1 --------------------
page1_rows = driver.find_elements(By.CSS_SELECTOR, "#example tbody tr")

page1_data = []
for row in page1_rows:
    page1_data.append(row.text)

print("Page 1")
for r in page1_data:
    print(r)

# Verify there are 10 rows
assert len(page1_data) == 10

# Total records text
info_before = driver.find_element(By.ID, "example_info").text
print("\nInfo Before:", info_before)

# -------------------- GO TO PAGE 2 --------------------

page2 = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class,'dt-paging-button') and text()='2']")
    )
)
page2.click()

# Wait until active page becomes 2
wait.until(
    EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, "button.dt-paging-button.current"),
        "2"
    )
)

# Wait until first row changes
wait.until(
    lambda d: d.find_elements(By.CSS_SELECTOR, "#example tbody tr")[0].text != page1_data[0]
)

# -------------------- PAGE 2 --------------------
page2_rows = driver.find_elements(By.CSS_SELECTOR, "#example tbody tr")

page2_data = []
for row in page2_rows:
    page2_data.append(row.text)

print("\nPage 2")
for r in page2_data:
    print(r)

# Verify there are 10 rows
assert len(page2_data) == 10

# Verify records are different
assert page1_data != page2_data

# Verify active page number
current_page = driver.find_element(
    By.CSS_SELECTOR,
    "button.dt-paging-button.current"
).text

assert current_page == "2"

# Verify total entries remain same
info_after = driver.find_element(By.ID, "example_info").text

print("\nInfo After:", info_after)

before_total = info_before.split("of ")[1].split(" entries")[0]
after_total = info_after.split("of ")[1].split(" entries")[0]

assert before_total == after_total

print("\n==============================")
print("Pagination Validation Passed")
print("==============================")

driver.quit()