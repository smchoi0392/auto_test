"""
페이지 요소 로케이터 관리 파일
UI 요소 선택자를 중앙에서 관리합니다.
"""


class LoginPageLocators:
    """로그인 페이지의 요소 로케이터"""

    # 입력 필드
    EMAIL_INPUT = 'input[type="email"]'
    PASSWORD_INPUT = 'input[type="password"]'

    # 버튼
    SUBMIT_BUTTON = 'button[type="submit"]'
    LOGIN_BUTTON = 'button[type="submit"]'  # alias


class DashboardLocators:
    """대시보드 페이지의 요소 로케이터"""

    # 텍스트 요소 (표시 확인용)
    WMS_QA_TEXT = 'text=WMS QA'
    POS_TEXT = 'text=POS'

    # 버튼 요소 (클릭용)
    WMS_QA_BUTTON = 'text=WMS QA'
    POS_BUTTON = 'text=POS'
