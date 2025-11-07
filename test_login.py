"""
로그인 테스트
config의 DEFAULT_SERVICE 설정에 따라 WMS 또는 POS 서비스를 테스트합니다.

실행 방법:
  python test_login.py         # 브라우저 보면서 실행, 로그 저장
  pytest test_login.py         # pytest로 실행
  pytest test_login.py -v      # 상세 출력

설정 변경:
  config/config.py의 DEFAULT_SERVICE를 "wms" 또는 "pos"로 설정
"""

import sys
import pytest
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config import config
from config.constants import ServiceType


class TeeOutput:
    """콘솔과 파일에 동시 출력하는 클래스 (필터링 기능 포함)"""

    def __init__(self, file_path):
        self.file = open(file_path, 'w', encoding='utf-8')
        self.console = sys.stdout
        self.last_was_newline = False
        self.skip_patterns = [
            'platform win32',
            'rootdir:',
            'configfile:',
            'plugins:',
            'collected',
            'cachedir:',
            'metadata:',
            'JAVA_HOME:',
        ]

    def write(self, message):
        # pytest 메타데이터 필터링
        should_skip = False
        stripped = message.strip()

        # 특정 패턴이 포함된 줄 건너뛰기
        for pattern in self.skip_patterns:
            if pattern in message:
                should_skip = True
                break

        # "test session starts" 줄 건너뛰기
        if 'test session starts' in message and '=' in message:
            should_skip = True

        # "collecting" 줄 건너뛰기
        if 'collecting' in stripped or 'collected' in stripped:
            should_skip = True

        # "=" 만으로 이루어진 줄 건너뛰기 (구분선)
        if stripped and all(c == '=' for c in stripped):
            should_skip = True

        # "." 만 있는 줄 건너뛰기 (테스트 진행 표시)
        if stripped == '.':
            should_skip = True

        # 파일에는 필터링된 내용 기록
        if not should_skip:
            # 연속된 빈 줄 방지
            if message == '\n':
                if not self.last_was_newline:
                    self.file.write(message)
                    self.last_was_newline = True
            else:
                self.file.write(message)
                self.last_was_newline = False
            self.file.flush()

        # 콘솔에는 모든 내용 출력
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

    def test_login_and_navigate_to_service(self, page: Page):
        """config의 DEFAULT_SERVICE에 따라 로그인 및 서비스 네비게이션 테스트"""
        # config에서 서비스 타입 읽기
        service_type = config.DEFAULT_SERVICE

        print(f"[INFO] 테스트 대상 서비스: {service_type.upper()}")

        # 로그인
        login_page = LoginPage(page)
        login_page.login()

        # 지정된 서비스 버튼 클릭
        dashboard_page = DashboardPage(page)
        dashboard_page.click_service_button(service_type)

        # 로그인 성공 확인: 좌측 하단에 서비스명과 이메일 표시 확인
        dashboard_page.verify_login_success()

        service_name = "WMS QA" if service_type == ServiceType.WMS else "POS"
        print(f"[OK] {service_name} 로그인 테스트 성공!")


if __name__ == "__main__":
    # results 폴더 생성
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    # 타임스탬프로 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.now().strftime("%Y%m%d")

    # 날짜별 폴더 생성
    date_dir = results_dir / date_str
    date_dir.mkdir(exist_ok=True)

    log_file = date_dir / f"log_{timestamp}.txt"

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
