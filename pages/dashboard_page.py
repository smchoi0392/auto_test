from playwright.sync_api import Page, expect
from config.config import LoginConfig
from locator.locators_login import DashboardLocators


class DashboardPage:
    """대시보드 페이지 클래스"""

    def __init__(self, page: Page):
        self.page = page
        self.wms_qa_button = page.locator(DashboardLocators.WMS_QA_BUTTON)
        self.pos_button = page.locator(DashboardLocators.POS_BUTTON)

    def click_wms_qa_button(self):
        """WMS QA 버튼 클릭"""
        self.wms_qa_button.click()
        print("[OK] 'WMS QA' 버튼 클릭")
        self.page.wait_for_load_state("networkidle")

    def click_pos_button(self):
        """POS 버튼 클릭"""
        self.pos_button.click()
        print("[OK] 'POS' 버튼 클릭")
        self.page.wait_for_load_state("networkidle")

    def verify_dashboard_url(self):
        """대시보드 URL 확인"""
        dashboard_url = LoginConfig.get_dashboard_url()
        expect(self.page).to_have_url(dashboard_url, timeout=LoginConfig.DEFAULT_TIMEOUT)
        print(f"[OK] 대시보드 URL 이동 확인: {dashboard_url}")
