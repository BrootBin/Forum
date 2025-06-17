from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://forum-production-c592.up.railway.app/register/")

    username = f"testuser{random.randint(1000,9999)}"
    password = f"TestPassword{random.randint(1000,9999)}"

    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password1")
    confirm_input = driver.find_element(By.NAME, "password2")

    username_input.send_keys(username)
    email_input.send_keys(f"{username}@example.com")
    password_input.send_keys(password)
    confirm_input.send_keys(password)

    register_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Зареєструватися')]")
    register_btn.click()

    wait.until(EC.url_changes("https://forum-production-c592.up.railway.app/register/"))

    current_url = driver.current_url
    expected_url = "https://forum-production-c592.up.railway.app/"

    print(f"Користувача створено: {username}")
    print(f"Пароль: {password}")

except Exception as e:
    print(f"Помилка під час реєстрації: {e}")

finally:
    time.sleep(2)
    driver.quit()
