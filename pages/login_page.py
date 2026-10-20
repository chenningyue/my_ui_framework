from playwright.sync_api import Page
from data.test_data import URL
class LoginPage:
    def __init__(self,page:Page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.login_button = page.locator("#loginBtn")
        self.result = page.locator("#result")

    def goto_login_page(self):
        self.page.goto(URL)

    def login(self,username,password):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()