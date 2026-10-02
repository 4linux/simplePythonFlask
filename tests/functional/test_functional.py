import os
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

# Enderecos do ambiente que sera testado. Os valores padrao sao os do docker-compose.
APP_URL = os.environ.get("APP_URL", "http://web:5000").rstrip("/")
SELENIUM_URL = os.environ.get("SELENIUM_URL", "http://selenium:4444/wd/hub")


class AllTests(unittest.TestCase):

    # Usuario unico por execucao, para o teste poder rodar varias vezes no mesmo ambiente
    username = "devops%d" % int(time.time())
    password = "qwe123qwe"

    def setUp(self):
        self.driver = webdriver.Remote(
            command_executor=SELENIUM_URL,
            options=webdriver.FirefoxOptions())

    def tearDown(self):
        self.driver.quit()

    def test_1_user_can_register(self):
        self.driver.get(APP_URL + "/register")
        self.driver.find_element(By.ID, "name").send_keys(self.username)
        self.driver.find_element(By.ID, "email").send_keys(self.username + "@example.com")
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "confirm").send_keys(self.password)
        self.driver.find_element(By.ID, "register").click()
        print(self.driver.current_url)
        self.assertEqual(APP_URL + "/", self.driver.current_url)
        self.assertIn("Obrigado por se registrar!!!", self.driver.page_source)

    def test_2_user_can_login(self):
        self.driver.get(APP_URL)
        self.driver.find_element(By.ID, "name").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "loginbutton").click()
        print(self.driver.current_url)
        self.assertEqual(APP_URL + "/courses", self.driver.current_url)
        self.assertIn("Bem vindo ao Painel de Cursos!!!", self.driver.page_source)
        self.assertNotIn("Nenhum curso cadastrado.", self.driver.page_source)


if __name__ == "__main__":
    unittest.main(warnings='ignore')
