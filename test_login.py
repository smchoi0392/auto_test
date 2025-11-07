"""
테스트 실행 스크립트
python test_login.py 명령으로 테스트를 실행합니다.
"""

import sys
import io
import pytest
from datetime import datetime
from pathlib import Path


class TeeOutput:
    """콘솔과 파일에 동시 출력하는 클래스"""

    def __init__(self, file_path, console_encoding='utf-8'):
        self.file = open(file_path, 'w', encoding='utf-8')
        self.console = sys.stdout
        self.console_encoding = console_encoding

    def write(self, message):
        # 파일에 UTF-8로 저장
        self.file.write(message)
        self.file.flush()

        # 콘솔에 출력 (Windows CMD 인코딩 처리)
        try:
            self.console.write(message)
        except UnicodeEncodeError:
            # 콘솔에서 표시할 수 없는 문자는 ? 로 대체
            safe_message = message.encode('cp949', errors='replace').decode('cp949')
            self.console.write(safe_message)
        self.console.flush()

    def flush(self):
        self.file.flush()
        self.console.flush()

    def close(self):
        self.file.close()

    def isatty(self):
        """터미널 여부 확인"""
        return self.console.isatty() if hasattr(self.console, 'isatty') else False

    def fileno(self):
        """파일 디스크립터 반환"""
        return self.console.fileno() if hasattr(self.console, 'fileno') else None


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
            "test/test_login_suite.py",
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
