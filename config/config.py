"""
테스트 설정 파일
URL, 테스트 계정 정보 등을 관리합니다.
"""


class Config:
    """기본 설정 클래스"""

    # 환경별 URL
    DEV_URL = "https://dev.sellmatewms.com"
    STAGING_URL = "https://staging.sellmatewms.com"
    PROD_URL = "https://sellmatewms.com"

    # 기본 환경 설정
    DEFAULT_ENV = "dev"

    # 타임아웃 설정
    DEFAULT_TIMEOUT = 5000
    LOAD_TIMEOUT = 10000


class LoginConfig(Config):
    """로그인 관련 설정"""

    # 로그인 URL
    LOGIN_PATH = "/wms-auth/login"
    DASHBOARD_PATH = "/dashboard"

    # 테스트 계정 정보
    EMAIL = "dev@sellmate.co.kr"
    PASSWORD = "sellmate1!"

    @classmethod
    def get_login_url(cls, env: str = None) -> str:
        """환경에 따른 로그인 URL 반환"""
        env = env or cls.DEFAULT_ENV

        if env == "dev":
            base_url = cls.DEV_URL
        elif env == "staging":
            base_url = cls.STAGING_URL
        elif env == "prod":
            base_url = cls.PROD_URL
        else:
            raise ValueError(f"알 수 없는 환경: {env}")

        return f"{base_url}{cls.LOGIN_PATH}"

    @classmethod
    def get_dashboard_url(cls, env: str = None) -> str:
        """환경에 따른 대시보드 URL 반환"""
        env = env or cls.DEFAULT_ENV

        if env == "dev":
            base_url = cls.DEV_URL
        elif env == "staging":
            base_url = cls.STAGING_URL
        elif env == "prod":
            base_url = cls.PROD_URL
        else:
            raise ValueError(f"알 수 없는 환경: {env}")

        return f"{base_url}{cls.DASHBOARD_PATH}"


class ExpectedTexts:
    """로그인 후 확인할 텍스트"""

    WMS_QA = "WMS QA"
    POS = "POS"
