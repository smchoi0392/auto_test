from playwright.sync_api import Page
from config import config
from config.utils import get_login_url
from locator.locators_login import LoginPageLocators


class LoginPage:
    """로그인 페이지 클래스"""

    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator(LoginPageLocators.EMAIL_INPUT)
        self.password_input = page.locator(LoginPageLocators.PASSWORD_INPUT)
        self.login_button = page.locator(LoginPageLocators.LOGIN_BUTTON)

    def goto_login_page(self):
        """로그인 페이지로 이동"""
        login_url = get_login_url()
        self.page.goto(login_url)
        print(f"[OK] 로그인 페이지 접속: {login_url}")

    def fill_email(self, email: str):
        """이메일 입력"""
        self.email_input.fill(email)
        print(f"[OK] 이메일 입력: {email}")

    def fill_password(self, password: str):
        """비밀번호 입력"""
        self.password_input.fill(password)
        print(f"[OK] 비밀번호 입력: {'*' * len(password)}")

    def click_login_button(self):
        """로그인 버튼 클릭"""
        self.login_button.click()
        print("[OK] 로그인 버튼 클릭")

    def wait_for_page_load(self):
        """페이지 로딩 대기"""
        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        print(f"[OK] 현재 URL: {current_url}")

    def login(self, email: str = None, password: str = None):
        """로그인 수행 (전체 프로세스)"""
        if email is None:
            email = config.EMAIL
        if password is None:
            password = config.PASSWORD

        self.goto_login_page()
        self.fill_email(email)
        self.fill_password(password)
        self.click_login_button()
        self.wait_for_page_load()
