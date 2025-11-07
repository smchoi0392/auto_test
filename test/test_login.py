import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


class TestLogin:
    """로그인 테스트 클래스"""

    def test_login_and_navigate_to_wms_qa(self, page: Page):
        """WMS QA 버튼 클릭 후 대시보드 이동 테스트"""
        # 로그인
        login_page = LoginPage(page)
        login_page.login()

        # WMS QA 버튼 클릭 및 대시보드 이동 확인
        dashboard_page = DashboardPage(page)
        dashboard_page.click_wms_qa_button()
        dashboard_page.verify_dashboard_url()

        print("[OK] WMS QA 버튼 클릭 테스트 성공!")

    def test_login_and_navigate_to_pos(self, page: Page):
        """POS 버튼 클릭 후 대시보드 이동 테스트"""
        # 로그인
        login_page = LoginPage(page)
        login_page.login()

        # POS 버튼 클릭 및 대시보드 이동 확인
        dashboard_page = DashboardPage(page)
        dashboard_page.click_pos_button()
        dashboard_page.verify_dashboard_url()

        print("[OK] POS 버튼 클릭 테스트 성공!")
