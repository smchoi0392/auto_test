"""
페이지 요소 로케이터 관리 파일
UI 요소 선택자를 중앙에서 관리합니다.
"""

from config.constants import ServiceType


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

    # 서비스별 버튼 로케이터 매핑
    SERVICE_BUTTONS = {
        ServiceType.WMS: 'text=WMS QA',
        ServiceType.POS: 'text=POS',
    }

    # 서비스별 이름 매핑
    SERVICE_NAMES = {
        ServiceType.WMS: 'WMS QA',
        ServiceType.POS: 'POS',
    }

    # 좌측 하단 사용자 정보 영역
    # 실제 페이지 구조에 맞게 수정 필요
    USER_INFO_SECTION = '[class*="user"], [class*="profile"], aside, nav'  # 좌측 영역
    SERVICE_NAME_DISPLAY = None  # 동적으로 설정됨
    USER_EMAIL_DISPLAY = None  # 동적으로 설정됨
