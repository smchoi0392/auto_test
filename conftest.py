"""
pytest 설정 파일
테스트 실행 시 공통 설정을 관리합니다.
"""

import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    브라우저 컨텍스트 설정
    - 클릭한 요소 하이라이트 표시
    - 동작 속도 조절
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},  # 화면 크기 설정
    }


@pytest.fixture(scope="function")
def page(context):
    """
    페이지 픽스처 - 각 테스트마다 새 페이지 생성
    클릭한 요소를 하이라이트 표시하는 스크립트 추가
    """
    page = context.new_page()

    # 클릭한 요소를 하이라이트 표시하는 JavaScript 추가
    page.add_init_script("""
        // 클릭 이벤트를 감지하여 하이라이트 표시
        document.addEventListener('click', (e) => {
            const element = e.target;
            const originalOutline = element.style.outline;
            const originalBackground = element.style.backgroundColor;

            // 빨간 테두리와 배경색 추가
            element.style.outline = '3px solid red';
            element.style.backgroundColor = 'rgba(255, 0, 0, 0.1)';

            // 1초 후 원래대로 복원
            setTimeout(() => {
                element.style.outline = originalOutline;
                element.style.backgroundColor = originalBackground;
            }, 1000);
        }, true);

        // 입력 필드에 포커스 시 하이라이트
        document.addEventListener('focus', (e) => {
            const element = e.target;
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.style.outline = '3px solid blue';
                element.style.backgroundColor = 'rgba(0, 0, 255, 0.1)';
            }
        }, true);

        // 입력 필드에서 포커스 해제 시 복원
        document.addEventListener('blur', (e) => {
            const element = e.target;
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.style.outline = '';
                element.style.backgroundColor = '';
            }
        }, true);
    """)

    yield page
    page.close()
