"""
로그인 테스트
WMS와 POS 서비스 로그인 및 네비게이션을 테스트합니다.

실행 방법:
  python test_login.py         # 브라우저 보면서 실행, 로그 저장
  pytest test_login.py         # pytest로 실행
  pytest test_login.py -v      # 상세 출력
"""

import sys
import pytest
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.constants import ServiceType


class TeeOutput:
    """콘솔과 파일에 동시 출력하는 클래스"""

    def __init__(self, file_path):
        self.file = open(file_path, 'w', encoding='utf-8')
        self.console = sys.stdout

    def write(self, message):
        self.file.write(message)
        self.file.flush()
        try:
            self.console.write(message)
        except UnicodeEncodeError:
            safe_message = message.encode('cp949', errors='replace').decode('cp949')
            self.console.write(safe_message)
        self.console.flush()

    def flush(self):
        self.file.flush()
        self.console.flush()

    def close(self):
        self.file.close()

    def isatty(self):
        return self.console.isatty() if hasattr(self.console, 'isatty') else False

    def fileno(self):
        return self.console.fileno() if hasattr(self.console, 'fileno') else None


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


if __name__ == "__main__":
    # results 폴더 생성
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # 타임스탬프로 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = results_dir / f"log_{timestamp}.txt"

    print(f"테스트 로그 저장 위치: {log_file}")
    print("=" * 80)
    print()

    # 출력을 콘솔과 파일에 동시 기록
    tee = TeeOutput(log_file)
    tee.write(f"테스트 실행 시간: {timestamp}\n")
    tee.write("=" * 80 + "\n\n")

    # sys.stdout과 sys.stderr를 리다이렉트
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = tee
    sys.stderr = tee

    try:
        # pytest 실행 옵션
        args = [
            __file__,  # 현재 파일
            "--headed",  # 브라우저 표시
            "-v",  # 상세 출력
            "-s",  # print 출력 표시
        ]

        # 사용자가 추가 옵션을 입력한 경우 함께 전달
        if len(sys.argv) > 1:
            args.extend(sys.argv[1:])

        # pytest 실행
        exit_code = pytest.main(args)

    finally:
        # stdout/stderr 복원
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        tee.close()

    # 테스트 완료 메시지
    print()
    print("=" * 80)
    if exit_code == 0:
        print(f"[OK] 테스트 성공! 로그 파일: {log_file}")
    else:
        print(f"[ERROR] 테스트 실패! 로그 파일: {log_file}")

    sys.exit(exit_code)
