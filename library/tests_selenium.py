from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.auth import get_user_model
import time

User = get_user_model()

class LibraryLoginTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)
        
        self.email = 'viktoriia_test@example.com'
        self.password = 'secure12345'
        
        if not User.objects.filter(email=self.email).exists():
            User.objects.create_user(
                email=self.email, 
                password=self.password,
                first_name="Viktoriia",
                last_name="Sikorska",
                role=1 
            )
        super().setUp()

    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def test_login_logout_process(self):
        self.browser.get(f"{self.live_server_url}/auth/login/")
        time.sleep(1)

        self.browser.find_element(By.NAME, "email").send_keys(self.email)
        self.browser.find_element(By.NAME, "password").send_keys(self.password)

        submit_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        self.browser.execute_script("arguments[0].click();", submit_btn)
        
        time.sleep(2)
        self.assertIn("Welcome", self.browser.page_source)
        self.assertIn("Logout", self.browser.page_source)

        logout_button = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Logout')]")
        self.browser.execute_script("arguments[0].click();", logout_button)
        
        time.sleep(1)
        self.assertIn("Login", self.browser.page_source)

    def test_failed_login(self):
        self.browser.get(f"{self.live_server_url}/auth/login/")
        self.browser.find_element(By.NAME, "email").send_keys(self.email)
        self.browser.find_element(By.NAME, "password").send_keys("wrong_pass_123")
        
        submit_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        self.browser.execute_script("arguments[0].click();", submit_btn)
 
        time.sleep(1)
        error_msg = self.browser.find_element(By.CLASS_NAME, "alert-danger").text
        self.assertIn("Invalid email or password", error_msg)