from playwright.sync_api import Page, expect
from config import config
from config.utils import get_dashboard_url
from locator.locators_login import DashboardLocators


class DashboardPage:
    """대시보드 페이지 클래스"""

    def __init__(self, page: Page):
        self.page = page
        self.clicked_service_type = None
        self.user_email = config.EMAIL

    def click_service_button(self, service_type: str = None):
        """서비스 타입에 따라 동적으로 버튼 클릭"""
        service_type = service_type or config.DEFAULT_SERVICE
        self.clicked_service_type = service_type  # 클릭한 서비스 타입 저장

        # 서비스 타입에 해당하는 로케이터 가져오기
        if service_type not in DashboardLocators.SERVICE_BUTTONS:
            raise ValueError(f"알 수 없는 서비스 타입: {service_type}")

        locator = DashboardLocators.SERVICE_BUTTONS[service_type]
        service_name = DashboardLocators.SERVICE_NAMES[service_type]

        # 동적으로 버튼 클릭
        self.page.locator(locator).click()
        print(f"[OK] '{service_name}' 버튼 클릭")
        self.page.wait_for_load_state("networkidle")

    def verify_login_success(self):
        """로그인 성공 확인: URL, 서비스명, 이메일 표시 확인"""
        # 클릭한 서비스명 가져오기
        service_name = DashboardLocators.SERVICE_NAMES.get(self.clicked_service_type, "")

        try:
            # 1. URL이 대시보드로 이동했는지 확인
            current_url = self.page.url
            expected_url = get_dashboard_url()
            assert expected_url in current_url, f"예상 URL: {expected_url}, 실제 URL: {current_url}"
            print(f"[OK] 대시보드 URL 이동 확인: {current_url}")

            # 2. 서비스명이 페이지에 표시되는지 확인
            service_locator = self.page.get_by_text(service_name, exact=True)
            expect(service_locator).to_be_visible(timeout=config.DEFAULT_TIMEOUT)
            print(f"[OK] 서비스명 '{service_name}' 표시 확인")

            # 3. 이메일이 페이지에 표시되는지 확인
            email_locator = self.page.get_by_text(self.user_email, exact=True)
            expect(email_locator).to_be_visible(timeout=config.DEFAULT_TIMEOUT)
            print(f"[OK] 이메일 '{self.user_email}' 표시 확인")

            print("[OK] 로그인 성공 확인 완료")

        except Exception as e:
            print(f"[ERROR] 로그인 성공 확인 실패: {str(e)}")
            # 디버깅을 위해 현재 페이지의 텍스트 내용 일부 출력
            page_content = self.page.text_content('body')
            print(f"[DEBUG] 페이지 내용 일부: {page_content[:500] if page_content else 'None'}...")
            raise
