from selenium import webdriver

driver = webdriver.Chrome()
driver.execute_script("window.open('https://www.google.com', '_blank');")
driver.switch_to.window(driver.window_handles[-1])