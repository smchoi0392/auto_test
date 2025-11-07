import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.constants import ServiceType


class TestLogin:
    """로그인 테스트 클래스"""

    @pytest.mark.parametrize("service_type", [ServiceType.WMS, ServiceType.POS])
    def test_login_and_navigate_to_service(self, page: Page, service_type: str):
        """WMS와 POS 각 1번씩 테스트 - 로그인 후 각 서비스 버튼 클릭 및 대시보드 이동"""
        # 로그인
        login_page = LoginPage(page)
        login_page.login()

        # 지정된 서비스 버튼 클릭 및 대시보드 이동 확인
        dashboard_page = DashboardPage(page)
        dashboard_page.click_service_button(service_type)
        dashboard_page.verify_dashboard_url()

        service_name = "WMS QA" if service_type == ServiceType.WMS else "POS"
        print(f"[OK] {service_name} 버튼 클릭 테스트 성공!")
