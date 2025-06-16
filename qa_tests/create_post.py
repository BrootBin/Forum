from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://forum-production-c592.up.railway.app/login/")

    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys("M1n1B0SS")
    password_input.send_keys("123kaka123")

    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Увійти')]")
    login_button.click()

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Створити пост"))).click()

    title_input = wait.until(EC.presence_of_element_located((By.NAME, "title")))
    content_input = driver.find_element(By.NAME, "content")

    title_input.send_keys("Тестовий пост")
    content_input.send_keys("Це автоматично створений пост за допомогою Selenium.")

    category_select = Select(driver.find_element(By.NAME, "category"))
    category_select.select_by_visible_text("Гарячі")

    post_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Створити')]")
    post_button.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "post-card")))

    print("Пост створено успішно.")

    logout_button = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Вийти")))
    logout_button.click()

    print("Успішний вихід з акаунта.")

except Exception as e:
    print(f"Помилка під час виконання: {e}")

finally:
    time.sleep(2)
    driver.quit()
