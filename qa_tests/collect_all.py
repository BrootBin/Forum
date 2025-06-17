from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://forum-production-c592.up.railway.app/")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "post-card")))

posts = driver.find_elements(By.CLASS_NAME, "post-card")

print(f"Кількість постів на форумі: {len(posts)}")

driver.quit()
