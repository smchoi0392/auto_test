"""
테스트 설정 파일
순수 설정 값만 관리합니다.
"""


# 환경별 Base URL
DEV_URL = "https://dev.sellmatewms.com"
STAGING_URL = "https://staging.sellmatewms.com"
PROD_URL = "https://sellmatewms.com"

# 기본 환경 설정
DEFAULT_ENV = "dev"

# 서비스 타입 설정
DEFAULT_SERVICE = "wms"  # "wms" 또는 "pos"

# 경로
LOGIN_PATH = "/wms-auth/login"
DASHBOARD_PATH = "/dashboard"

# 테스트 계정 정보
EMAIL = "dev@sellmate.co.kr"
PASSWORD = "sellmate1!"

# 타임아웃 설정 (밀리초)
DEFAULT_TIMEOUT = 5000
LOAD_TIMEOUT = 10000
