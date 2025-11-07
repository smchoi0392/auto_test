"""
유틸리티 함수들
URL 생성 등의 헬퍼 함수를 제공합니다.
"""

from config import config


def get_base_url(env: str = None) -> str:
    """환경에 따른 Base URL 반환"""
    env = env or config.DEFAULT_ENV

    if env == "dev":
        return config.DEV_URL
    elif env == "staging":
        return config.STAGING_URL
    elif env == "prod":
        return config.PROD_URL
    else:
        raise ValueError(f"알 수 없는 환경: {env}")


def get_login_url(env: str = None) -> str:
    """환경에 따른 로그인 URL 반환"""
    base_url = get_base_url(env)
    return f"{base_url}{config.LOGIN_PATH}"


def get_dashboard_url(env: str = None) -> str:
    """환경에 따른 대시보드 URL 반환"""
    base_url = get_base_url(env)
    return f"{base_url}{config.DASHBOARD_PATH}"
