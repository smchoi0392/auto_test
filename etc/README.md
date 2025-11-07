# SellmateWMS 로그인 자동화 테스트

Python + Playwright를 사용한 웹 애플리케이션 자동화 테스트입니다.

## 프로젝트 구조

```
python_tests/
├── requirements.txt      # Python 패키지 의존성
├── pytest.ini           # pytest 설정 파일
├── test_login.py        # 로그인 테스트
└── README.md           # 이 파일
```

## 설치 방법

### 1. Python 가상환경 생성 (권장)

```bash
cd python_tests
python -m venv venv
```

### 2. 가상환경 활성화

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. Playwright 브라우저 설치

```bash
playwright install
```

또는 Chromium만 설치:
```bash
playwright install chromium
```

## 테스트 실행 방법

### 기본 실행

```bash
pytest test_login.py
```

### 브라우저를 보면서 실행 (Headed 모드)

```bash
pytest test_login.py --headed
```

### 특정 브라우저로 실행

```bash
pytest test_login.py --browser chromium
pytest test_login.py --browser firefox
pytest test_login.py --browser webkit
```

### 느리게 실행 (디버깅용)

```bash
pytest test_login.py --headed --slowmo 1000
```

### 상세한 로그 출력

```bash
pytest test_login.py -v -s
```

## 테스트 내용

### test_login.py

**test_login_success**: 로그인 기능 테스트

1. 로그인 페이지 접속: https://dev.sellmatewms.com/wms-auth/login
2. 이메일 입력: dev@sellmate.co.kr
3. 비밀번호 입력: sellmate1!
4. 로그인 버튼 클릭
5. 로그인 성공 확인 (URL 변경 체크)

## 트러블슈팅

### 문제: 요소를 찾을 수 없다는 에러

실제 웹페이지의 HTML 구조를 확인하고 `test_login.py`의 선택자(selector)를 수정해야 합니다.

브라우저 개발자 도구(F12)를 열어서 실제 요소의 id, name, class 등을 확인하세요.

### 문제: 브라우저가 실행되지 않음

```bash
playwright install
```

명령어로 브라우저를 다시 설치해보세요.

## 추가 기능 개발 예정

- [ ] 로그아웃 테스트
- [ ] 잘못된 비밀번호 입력 테스트
- [ ] 빈 필드 제출 테스트
- [ ] 스크린샷 캡처 기능
- [ ] 테스트 리포트 생성

## 참고 자료

- [Playwright Python 문서](https://playwright.dev/python/)
- [pytest 문서](https://docs.pytest.org/)
