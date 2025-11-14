# 공통 모듈 설계 및 구현 계획
# 체험단 매칭 플랫폼 "1st_bungae"

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | 공통 모듈 설계 및 구현 계획 |
| **프로젝트명** | 1st_bungae |
| **버전** | 1.0.0 |
| **작성일** | 2025-11-14 |
| **목적** | TDD 기반 공통 모듈 구현 계획 수립 |

---

## 목차

1. [개요](#1-개요)
2. [공통 모듈 목록](#2-공통-모듈-목록)
3. [모듈별 TDD 구현 계획](#3-모듈별-tdd-구현-계획)
4. [구현 순서](#4-구현-순서)
5. [검증 체크리스트](#5-검증-체크리스트)

---

## 1. 개요

### 1.1 설계 원칙

#### 최소한의 설계 (YAGNI 원칙)
- 현재 요구사항에 필요한 기능만 구현
- 미래의 확장성을 위한 과도한 추상화 지양
- 실제 사용 사례가 나타날 때 리팩토링

#### TDD 필수 준수
- **RED → GREEN → REFACTOR** 사이클 엄격히 준수
- 테스트가 없는 코드는 작성하지 않음
- 모든 공통 모듈은 80% 이상의 테스트 커버리지 필수

#### Layered Architecture 준수
- 각 모듈은 명확한 계층에 속함
- 계층 간 의존성 방향 준수
- 인터페이스를 통한 느슨한 결합

---

### 1.2 기술 스택

| 구분 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **언어** | Python | 3.11+ | 백엔드 언어 |
| **프레임워크** | Flask | 3.0+ | 웹 프레임워크 |
| **ORM** | SQLAlchemy | 2.0+ | 데이터베이스 ORM |
| **인증** | Supabase Auth | 2.4.2 | 외부 인증 서비스 |
| **스토리지** | Supabase Storage | 2.4.2 | 파일 저장소 |
| **폼 검증** | Flask-WTF | 1.2.1 | 폼 검증 및 CSRF |
| **테스트** | pytest | 7.4+ | 테스트 프레임워크 |

---

## 2. 공통 모듈 목록

### 2.1 Infrastructure Layer (인프라 계층)

#### 2.1.1 Supabase Auth 연동
- **위치**: `app/infrastructure/external/supabase/supabase_auth.py`
- **목적**: Supabase Auth API 연동 (회원가입, 로그인, 로그아웃)
- **인터페이스**: `app/infrastructure/external/interfaces/i_auth_provider.py`

#### 2.1.2 Supabase Storage 연동
- **위치**: `app/infrastructure/external/supabase/supabase_storage.py`
- **목적**: Supabase Storage API 연동 (파일 업로드, 다운로드, 삭제)
- **인터페이스**: `app/infrastructure/external/interfaces/i_storage_provider.py`

#### 2.1.3 Database 설정
- **위치**: `app/config.py`, `app/extensions.py`
- **목적**: SQLAlchemy 데이터베이스 연결 설정
- **환경변수**: `.env` 파일 관리

---

### 2.2 Domain Layer (도메인 계층)

#### 2.2.1 Value Objects (값 객체)
- **이메일**: `app/domain/value_objects/email.py`
- **전화번호**: `app/domain/value_objects/phone_number.py`
- **사업자등록번호**: `app/domain/value_objects/business_number.py`
- **소셜 채널**: `app/domain/value_objects/social_channel.py`

#### 2.2.2 Domain Exceptions (도메인 예외)
- **베이스 예외**: `app/domain/exceptions/base.py`
- **인증 예외**: `app/domain/exceptions/auth_exceptions.py`
- **검증 예외**: `app/domain/exceptions/validation_exceptions.py`

---

### 2.3 Shared Layer (공유 유틸리티)

#### 2.3.1 Decorators (데코레이터)
- **인증 데코레이터**: `app/shared/decorators/auth_decorators.py`
  - `@login_required`: 로그인 필수
  - `@advertiser_required`: 광고주 권한 필수
  - `@influencer_required`: 인플루언서 권한 필수

#### 2.3.2 Utils (유틸리티)
- **날짜/시간 유틸**: `app/shared/utils/datetime_utils.py`
- **문자열 유틸**: `app/shared/utils/string_utils.py`
- **검증 유틸**: `app/shared/utils/validation_utils.py`

#### 2.3.3 Constants (상수)
- **사용자 상수**: `app/shared/constants/user_constants.py`
- **체험단 상수**: `app/shared/constants/campaign_constants.py`

---

## 3. 모듈별 TDD 구현 계획

---

## 3.1 Supabase Auth 연동

### 개요
- **목적**: Supabase Auth API를 사용한 이메일 기반 회원가입/로그인/로그아웃
- **파일 위치**:
  - 인터페이스: `app/infrastructure/external/interfaces/i_auth_provider.py`
  - 구현체: `app/infrastructure/external/supabase/supabase_auth.py`
  - 테스트: `tests/unit/infrastructure/external/test_supabase_auth.py`

---

### 테스트 시나리오 (TDD First)

#### 3.1.1 회원가입 테스트

**정상 케이스**
- Given: 유효한 이메일(test@example.com)과 비밀번호(Password123!)
- When: `sign_up(email, password)` 호출
- Then:
  - Supabase Auth API 호출 성공
  - User 객체 반환 (id, email 포함)

**경계 케이스**
- Given: 최소 길이 비밀번호(8자)
- When: `sign_up(email, password)` 호출
- Then: 정상적으로 회원가입 성공

**에러 케이스**
- Given: 이미 등록된 이메일
- When: `sign_up(email, password)` 호출
- Then: `AuthException` 발생 (message: "Email already registered")

- Given: 잘못된 이메일 형식
- When: `sign_up(invalid_email, password)` 호출
- Then: `ValidationException` 발생

- Given: 짧은 비밀번호(7자 이하)
- When: `sign_up(email, short_password)` 호출
- Then: `ValidationException` 발생 (message: "Password must be at least 8 characters")

---

#### 3.1.2 로그인 테스트

**정상 케이스**
- Given: 등록된 사용자의 이메일과 비밀번호
- When: `sign_in(email, password)` 호출
- Then:
  - 로그인 성공
  - Session 객체 반환 (access_token, refresh_token 포함)

**에러 케이스**
- Given: 존재하지 않는 이메일
- When: `sign_in(email, password)` 호출
- Then: `AuthException` 발생 (message: "Invalid credentials")

- Given: 잘못된 비밀번호
- When: `sign_in(email, wrong_password)` 호출
- Then: `AuthException` 발생 (message: "Invalid credentials")

---

#### 3.1.3 로그아웃 테스트

**정상 케이스**
- Given: 로그인된 사용자의 access_token
- When: `sign_out(access_token)` 호출
- Then:
  - 로그아웃 성공
  - 세션 무효화

**에러 케이스**
- Given: 유효하지 않은 access_token
- When: `sign_out(invalid_token)` 호출
- Then: `AuthException` 발생 (message: "Invalid token")

---

### 구현 계획 (TDD 사이클)

#### Phase 1: 회원가입 기능

**1. RED: 테스트 작성 및 실패 확인**
- 파일: `tests/unit/infrastructure/external/test_supabase_auth.py`
- 시나리오: 정상 케이스, 이메일 중복, 비밀번호 검증
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py::test_sign_up_success -v`
- 예상: FAILED (SupabaseAuthProvider 클래스 미구현)

**2. GREEN: 최소 구현**
- 파일: `app/infrastructure/external/supabase/supabase_auth.py`
- 구현:
  ```python
  class SupabaseAuthProvider(IAuthProvider):
      def sign_up(self, email: str, password: str) -> User:
          # Supabase Auth API 호출
          response = self.client.auth.sign_up({
              "email": email,
              "password": password
          })
          return User(id=response.user.id, email=response.user.email)
  ```
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py::test_sign_up_success -v`
- 예상: PASSED

**3. REFACTOR: 코드 개선**
- 예외 처리 추가 (Supabase API 에러 → AuthException 변환)
- 로깅 추가
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: 로그인 기능

**1. RED: 테스트 작성**
- 파일: `tests/unit/infrastructure/external/test_supabase_auth.py`
- 시나리오: 정상 로그인, 잘못된 이메일, 잘못된 비밀번호
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py::test_sign_in_success -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/infrastructure/external/supabase/supabase_auth.py`
- 구현: `sign_in()` 메서드 추가
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py::test_sign_in_success -v`
- 예상: PASSED

**3. REFACTOR: 중복 제거, 에러 처리 개선**
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py -v`
- 예상: PASSED (유지)

---

#### Phase 3: 로그아웃 기능

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py::test_sign_out_success -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: `sign_out()` 메서드 추가
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py::test_sign_out_success -v`
- 예상: PASSED

**3. REFACTOR: 전체 코드 리뷰 및 개선**
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py -v`
- 예상: PASSED (유지)

---

### 검증 체크리스트

- [ ] 모든 테스트 시나리오 작성 완료 (정상/경계/에러)
- [ ] RED Phase: 모든 테스트 실패 확인 (FAILED)
- [ ] GREEN Phase: 모든 테스트 통과 확인 (PASSED)
- [ ] REFACTOR Phase: 리팩토링 후 테스트 통과 유지
- [ ] 테스트 커버리지 80% 이상
- [ ] 에러 케이스 테스트 포함
- [ ] Mock을 사용한 Supabase API 호출 격리
- [ ] 문서화 완료 (Docstring, 타입 힌트)

---

## 3.2 Value Objects (값 객체)

### 개요
- **목적**: 불변 값 객체로 도메인 로직 캡슐화 및 검증
- **파일 위치**: `app/domain/value_objects/`
- **테스트 위치**: `tests/unit/domain/value_objects/`

---

### 3.2.1 Email (이메일)

#### 테스트 시나리오

**정상 케이스**
- Given: 유효한 이메일 주소 "user@example.com"
- When: `Email(value="user@example.com")` 생성
- Then: Email 객체 생성 성공, `value` 속성으로 접근 가능

**경계 케이스**
- Given: 최소 길이 이메일 "a@b.c"
- When: `Email(value="a@b.c")` 생성
- Then: Email 객체 생성 성공

**에러 케이스**
- Given: 잘못된 형식 "invalid-email"
- When: `Email(value="invalid-email")` 생성
- Then: `ValidationException` 발생 (message: "Invalid email format")

- Given: 빈 문자열 ""
- When: `Email(value="")` 생성
- Then: `ValidationException` 발생

- Given: None
- When: `Email(value=None)` 생성
- Then: `ValidationException` 발생

---

#### 구현 계획 (TDD 사이클)

**Phase 1: Email Value Object**

**1. RED: 테스트 작성**
- 파일: `tests/unit/domain/value_objects/test_email.py`
- 실행: `pytest tests/unit/domain/value_objects/test_email.py::test_email_valid -v`
- 예상: FAILED (Email 클래스 미구현)

**2. GREEN: 최소 구현**
- 파일: `app/domain/value_objects/email.py`
- 구현:
  ```python
  import re
  from app.domain.exceptions.validation_exceptions import ValidationException

  class Email:
      EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

      def __init__(self, value: str):
          if not value or not isinstance(value, str):
              raise ValidationException("Email cannot be empty")
          if not re.match(self.EMAIL_REGEX, value):
              raise ValidationException("Invalid email format")
          self._value = value

      @property
      def value(self) -> str:
          return self._value

      def __eq__(self, other):
          if not isinstance(other, Email):
              return False
          return self._value == other._value

      def __hash__(self):
          return hash(self._value)

      def __str__(self):
          return self._value
  ```
- 실행: `pytest tests/unit/domain/value_objects/test_email.py -v`
- 예상: PASSED

**3. REFACTOR: 불변성 보장**
- `@property` 사용하여 `value` 속성을 읽기 전용으로 변경
- `__repr__()` 메서드 추가
- 실행: `pytest tests/unit/domain/value_objects/test_email.py -v`
- 예상: PASSED (유지)

---

### 3.2.2 PhoneNumber (전화번호)

#### 테스트 시나리오

**정상 케이스**
- Given: 유효한 전화번호 "010-1234-5678"
- When: `PhoneNumber(value="010-1234-5678")` 생성
- Then: PhoneNumber 객체 생성 성공

**경계 케이스**
- Given: 하이픈 없는 전화번호 "01012345678"
- When: `PhoneNumber(value="01012345678")` 생성
- Then: 자동으로 "010-1234-5678" 형식으로 변환

**에러 케이스**
- Given: 잘못된 형식 "010-12-34"
- When: `PhoneNumber(value="010-12-34")` 생성
- Then: `ValidationException` 발생 (message: "Invalid phone number format")

- Given: 010으로 시작하지 않는 번호 "011-1234-5678"
- When: `PhoneNumber(value="011-1234-5678")` 생성
- Then: `ValidationException` 발생 (message: "Phone number must start with 010")

---

#### 구현 계획 (TDD 사이클)

**Phase 1: PhoneNumber Value Object**

**1. RED: 테스트 작성**
- 파일: `tests/unit/domain/value_objects/test_phone_number.py`
- 실행: `pytest tests/unit/domain/value_objects/test_phone_number.py -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/domain/value_objects/phone_number.py`
- 구현: 정규식 검증 및 자동 포맷팅
- 실행: `pytest tests/unit/domain/value_objects/test_phone_number.py -v`
- 예상: PASSED

**3. REFACTOR: 포맷팅 로직 개선**
- 하이픈 자동 추가 로직 분리
- 실행: `pytest tests/unit/domain/value_objects/test_phone_number.py -v`
- 예상: PASSED (유지)

---

### 3.2.3 BusinessNumber (사업자등록번호)

#### 테스트 시나리오

**정상 케이스**
- Given: 유효한 사업자등록번호 "1234567890" (10자리 숫자)
- When: `BusinessNumber(value="1234567890")` 생성
- Then: BusinessNumber 객체 생성 성공

**경계 케이스**
- Given: 하이픈 포함 "123-45-67890"
- When: `BusinessNumber(value="123-45-67890")` 생성
- Then: 자동으로 하이픈 제거하여 "1234567890"로 저장

**에러 케이스**
- Given: 9자리 숫자 "123456789"
- When: `BusinessNumber(value="123456789")` 생성
- Then: `ValidationException` 발생 (message: "Business number must be 10 digits")

- Given: 문자 포함 "12345678AB"
- When: `BusinessNumber(value="12345678AB")` 생성
- Then: `ValidationException` 발생 (message: "Business number must contain only digits")

---

#### 구현 계획 (TDD 사이클)

**Phase 1: BusinessNumber Value Object**

**1. RED: 테스트 작성**
- 파일: `tests/unit/domain/value_objects/test_business_number.py`
- 실행: `pytest tests/unit/domain/value_objects/test_business_number.py -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/domain/value_objects/business_number.py`
- 구현: 10자리 숫자 검증, 하이픈 제거
- 실행: `pytest tests/unit/domain/value_objects/test_business_number.py -v`
- 예상: PASSED

**3. REFACTOR: 검증 로직 개선**
- 실행: `pytest tests/unit/domain/value_objects/test_business_number.py -v`
- 예상: PASSED (유지)

---

### 3.2.4 SocialChannel (소셜 채널)

#### 테스트 시나리오

**정상 케이스**
- Given: 유효한 URL "https://www.youtube.com/@test"
- When: `SocialChannel(channel_name="테스트 채널", url="https://www.youtube.com/@test")` 생성
- Then: SocialChannel 객체 생성 성공

**경계 케이스**
- Given: http:// URL "http://blog.naver.com/test"
- When: `SocialChannel(channel_name="블로그", url="http://blog.naver.com/test")` 생성
- Then: 정상 생성 (http, https 모두 허용)

**에러 케이스**
- Given: 잘못된 URL "not-a-url"
- When: `SocialChannel(channel_name="채널", url="not-a-url")` 생성
- Then: `ValidationException` 발생 (message: "Invalid URL format")

- Given: 빈 채널명
- When: `SocialChannel(channel_name="", url="https://example.com")` 생성
- Then: `ValidationException` 발생 (message: "Channel name cannot be empty")

---

#### 구현 계획 (TDD 사이클)

**Phase 1: SocialChannel Value Object**

**1. RED: 테스트 작성**
- 파일: `tests/unit/domain/value_objects/test_social_channel.py`
- 실행: `pytest tests/unit/domain/value_objects/test_social_channel.py -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/domain/value_objects/social_channel.py`
- 구현: URL 검증 (정규식 또는 urllib.parse 사용)
- 실행: `pytest tests/unit/domain/value_objects/test_social_channel.py -v`
- 예상: PASSED

**3. REFACTOR: URL 검증 로직 개선**
- 실행: `pytest tests/unit/domain/value_objects/test_social_channel.py -v`
- 예상: PASSED (유지)

---

### 검증 체크리스트 (Value Objects)

- [ ] 모든 Value Object에 대한 테스트 시나리오 작성
- [ ] RED-GREEN-REFACTOR 사이클 준수
- [ ] 불변성 보장 (읽기 전용 속성)
- [ ] `__eq__`, `__hash__`, `__str__`, `__repr__` 메서드 구현
- [ ] 에러 케이스 테스트 포함
- [ ] 테스트 커버리지 80% 이상
- [ ] 문서화 완료

---

## 3.3 권한 관리 데코레이터

### 개요
- **목적**: Flask 라우트에서 사용자 권한 검증
- **파일 위치**: `app/shared/decorators/auth_decorators.py`
- **테스트 위치**: `tests/unit/shared/decorators/test_auth_decorators.py`

---

### 테스트 시나리오

#### 3.3.1 `@login_required` 데코레이터

**정상 케이스**
- Given: 로그인된 사용자 (session에 user_id 존재)
- When: `@login_required`가 적용된 라우트 접근
- Then: 정상적으로 라우트 함수 실행

**에러 케이스**
- Given: 로그인하지 않은 사용자 (session에 user_id 없음)
- When: `@login_required`가 적용된 라우트 접근
- Then: 로그인 페이지로 리다이렉트 (302)

---

#### 3.3.2 `@advertiser_required` 데코레이터

**정상 케이스**
- Given: 로그인된 광고주 (session에 user_id 존재, DB에 Advertiser 레코드 존재)
- When: `@advertiser_required`가 적용된 라우트 접근
- Then: 정상적으로 라우트 함수 실행

**에러 케이스**
- Given: 로그인했지만 광고주 정보 미등록
- When: `@advertiser_required`가 적용된 라우트 접근
- Then: 403 Forbidden 또는 광고주 정보 등록 페이지로 리다이렉트

- Given: 로그인한 인플루언서 (Advertiser 아님)
- When: `@advertiser_required`가 적용된 라우트 접근
- Then: 403 Forbidden

---

#### 3.3.3 `@influencer_required` 데코레이터

**정상 케이스**
- Given: 로그인된 인플루언서 (session에 user_id 존재, DB에 Influencer 레코드 존재)
- When: `@influencer_required`가 적용된 라우트 접근
- Then: 정상적으로 라우트 함수 실행

**에러 케이스**
- Given: 로그인했지만 인플루언서 정보 미등록
- When: `@influencer_required`가 적용된 라우트 접근
- Then: 403 Forbidden 또는 인플루언서 정보 등록 페이지로 리다이렉트

- Given: 로그인한 광고주 (Influencer 아님)
- When: `@influencer_required`가 적용된 라우트 접근
- Then: 403 Forbidden

---

### 구현 계획 (TDD 사이클)

#### Phase 1: `@login_required` 데코레이터

**1. RED: 테스트 작성**
- 파일: `tests/unit/shared/decorators/test_auth_decorators.py`
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py::test_login_required_authenticated -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/shared/decorators/auth_decorators.py`
- 구현:
  ```python
  from functools import wraps
  from flask import session, redirect, url_for

  def login_required(f):
      @wraps(f)
      def decorated_function(*args, **kwargs):
          if 'user_id' not in session:
              return redirect(url_for('auth.login'))
          return f(*args, **kwargs)
      return decorated_function
  ```
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py::test_login_required_authenticated -v`
- 예상: PASSED

**3. REFACTOR: 리다이렉트 URL 개선**
- 현재 URL을 `next` 파라미터로 전달
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: `@advertiser_required` 데코레이터

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py::test_advertiser_required_success -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: Advertiser 테이블 조회 로직 추가
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py::test_advertiser_required_success -v`
- 예상: PASSED

**3. REFACTOR: Repository 의존성 주입**
- DB 직접 조회 → Repository를 통한 조회로 변경
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py -v`
- 예상: PASSED (유지)

---

#### Phase 3: `@influencer_required` 데코레이터

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py::test_influencer_required_success -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: Influencer 테이블 조회 로직 추가
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py::test_influencer_required_success -v`
- 예상: PASSED

**3. REFACTOR: 중복 로직 제거**
- `advertiser_required`와 `influencer_required`의 공통 로직 추출
- 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py -v`
- 예상: PASSED (유지)

---

### 검증 체크리스트

- [ ] 모든 데코레이터에 대한 테스트 시나리오 작성
- [ ] RED-GREEN-REFACTOR 사이클 준수
- [ ] Mock을 사용한 DB 조회 격리
- [ ] 로그인 리다이렉트 시 `next` 파라미터 포함
- [ ] 에러 케이스 테스트 포함
- [ ] 테스트 커버리지 80% 이상
- [ ] 문서화 완료

---

## 3.4 공통 유틸리티

### 개요
- **목적**: 범용 헬퍼 함수 제공
- **파일 위치**: `app/shared/utils/`
- **테스트 위치**: `tests/unit/shared/utils/`

---

### 3.4.1 DateTimeUtils (날짜/시간 유틸)

#### 테스트 시나리오

**정상 케이스**
- Given: 날짜 문자열 "2025-11-14"
- When: `parse_date("2025-11-14")` 호출
- Then: `datetime.date(2025, 11, 14)` 반환

- Given: 두 날짜 `date1 = 2025-11-14`, `date2 = 2025-11-20`
- When: `days_between(date1, date2)` 호출
- Then: `6` 반환

**에러 케이스**
- Given: 잘못된 형식 "2025/11/14"
- When: `parse_date("2025/11/14")` 호출
- Then: `ValidationException` 발생 (message: "Invalid date format, expected YYYY-MM-DD")

---

#### 구현 계획 (TDD 사이클)

**Phase 1: 날짜 파싱**

**1. RED: 테스트 작성**
- 파일: `tests/unit/shared/utils/test_datetime_utils.py`
- 실행: `pytest tests/unit/shared/utils/test_datetime_utils.py::test_parse_date_valid -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/shared/utils/datetime_utils.py`
- 구현: `parse_date()` 함수
- 실행: `pytest tests/unit/shared/utils/test_datetime_utils.py::test_parse_date_valid -v`
- 예상: PASSED

**3. REFACTOR: 예외 처리 개선**
- 실행: `pytest tests/unit/shared/utils/test_datetime_utils.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: 날짜 간 일수 계산

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/shared/utils/test_datetime_utils.py::test_days_between -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: `days_between()` 함수
- 실행: `pytest tests/unit/shared/utils/test_datetime_utils.py::test_days_between -v`
- 예상: PASSED

**3. REFACTOR: 코드 정리**
- 실행: `pytest tests/unit/shared/utils/test_datetime_utils.py -v`
- 예상: PASSED (유지)

---

### 3.4.2 StringUtils (문자열 유틸)

#### 테스트 시나리오

**정상 케이스**
- Given: 문자열 "Hello World"
- When: `truncate("Hello World", max_length=5)` 호출
- Then: "Hello..." 반환

- Given: 문자열 "  test  "
- When: `normalize_whitespace("  test  ")` 호출
- Then: "test" 반환 (앞뒤 공백 제거)

**경계 케이스**
- Given: 짧은 문자열 "Hi"
- When: `truncate("Hi", max_length=10)` 호출
- Then: "Hi" 반환 (원본 그대로)

---

#### 구현 계획 (TDD 사이클)

**Phase 1: 문자열 자르기**

**1. RED: 테스트 작성**
- 파일: `tests/unit/shared/utils/test_string_utils.py`
- 실행: `pytest tests/unit/shared/utils/test_string_utils.py::test_truncate -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/shared/utils/string_utils.py`
- 구현: `truncate()` 함수
- 실행: `pytest tests/unit/shared/utils/test_string_utils.py::test_truncate -v`
- 예상: PASSED

**3. REFACTOR: suffix 옵션 추가**
- 실행: `pytest tests/unit/shared/utils/test_string_utils.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: 공백 정규화

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/shared/utils/test_string_utils.py::test_normalize_whitespace -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: `normalize_whitespace()` 함수
- 실행: `pytest tests/unit/shared/utils/test_string_utils.py::test_normalize_whitespace -v`
- 예상: PASSED

**3. REFACTOR: 정규식 패턴 최적화**
- 실행: `pytest tests/unit/shared/utils/test_string_utils.py -v`
- 예상: PASSED (유지)

---

### 3.4.3 ValidationUtils (검증 유틸)

#### 테스트 시나리오

**정상 케이스**
- Given: 값 5, 범위 1~10
- When: `is_in_range(5, min_value=1, max_value=10)` 호출
- Then: `True` 반환

- Given: 리스트 `["apple", "banana"]`, 값 "apple"
- When: `is_in_list("apple", ["apple", "banana"])` 호출
- Then: `True` 반환

**경계 케이스**
- Given: 값 1, 범위 1~10
- When: `is_in_range(1, min_value=1, max_value=10)` 호출
- Then: `True` 반환 (경계 포함)

- Given: 값 10, 범위 1~10
- When: `is_in_range(10, min_value=1, max_value=10)` 호출
- Then: `True` 반환 (경계 포함)

**에러 케이스**
- Given: 값 0, 범위 1~10
- When: `is_in_range(0, min_value=1, max_value=10)` 호출
- Then: `False` 반환

- Given: 값 11, 범위 1~10
- When: `is_in_range(11, min_value=1, max_value=10)` 호출
- Then: `False` 반환

---

#### 구현 계획 (TDD 사이클)

**Phase 1: 범위 검증**

**1. RED: 테스트 작성**
- 파일: `tests/unit/shared/utils/test_validation_utils.py`
- 실행: `pytest tests/unit/shared/utils/test_validation_utils.py::test_is_in_range -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/shared/utils/validation_utils.py`
- 구현: `is_in_range()` 함수
- 실행: `pytest tests/unit/shared/utils/test_validation_utils.py::test_is_in_range -v`
- 예상: PASSED

**3. REFACTOR: 타입 검증 추가**
- 실행: `pytest tests/unit/shared/utils/test_validation_utils.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: 리스트 포함 검증

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/shared/utils/test_validation_utils.py::test_is_in_list -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: `is_in_list()` 함수
- 실행: `pytest tests/unit/shared/utils/test_validation_utils.py::test_is_in_list -v`
- 예상: PASSED

**3. REFACTOR: 대소문자 무시 옵션 추가**
- 실행: `pytest tests/unit/shared/utils/test_validation_utils.py -v`
- 예상: PASSED (유지)

---

### 검증 체크리스트 (유틸리티)

- [ ] 모든 유틸리티 함수에 대한 테스트 시나리오 작성
- [ ] RED-GREEN-REFACTOR 사이클 준수
- [ ] 순수 함수로 작성 (부작용 없음)
- [ ] 에러 케이스 테스트 포함
- [ ] 테스트 커버리지 80% 이상
- [ ] 문서화 완료 (Docstring, 예제 포함)

---

## 3.5 Domain Exceptions (도메인 예외)

### 개요
- **목적**: 비즈니스 로직에서 발생하는 예외를 명확히 표현
- **파일 위치**: `app/domain/exceptions/`
- **테스트 위치**: `tests/unit/domain/exceptions/`

---

### 3.5.1 예외 계층 구조

```
DomainException (베이스)
├── ValidationException (검증 실패)
│   ├── InvalidEmailException
│   ├── InvalidPhoneNumberException
│   └── InvalidBusinessNumberException
├── AuthException (인증/인가 실패)
│   ├── InvalidCredentialsException
│   ├── EmailAlreadyExistsException
│   └── UnauthorizedException
└── BusinessRuleException (비즈니스 규칙 위반)
    ├── CampaignClosedException
    ├── DuplicateApplicationException
    └── QuotaExceededException
```

---

### 테스트 시나리오

#### 정상 케이스
- Given: 예외 클래스 `ValidationException`
- When: `raise ValidationException("Invalid email")` 발생
- Then:
  - 예외 메시지 "Invalid email" 포함
  - `DomainException`의 서브클래스

**에러 메시지 형식**
- Given: 예외 클래스 `InvalidEmailException`
- When: `str(InvalidEmailException("test@example"))` 호출
- Then: "Invalid email format: test@example" 반환

---

### 구현 계획 (TDD 사이클)

#### Phase 1: 베이스 예외 클래스

**1. RED: 테스트 작성**
- 파일: `tests/unit/domain/exceptions/test_base.py`
- 실행: `pytest tests/unit/domain/exceptions/test_base.py::test_domain_exception -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/domain/exceptions/base.py`
- 구현:
  ```python
  class DomainException(Exception):
      """모든 도메인 예외의 베이스 클래스"""
      def __init__(self, message: str):
          self.message = message
          super().__init__(self.message)
  ```
- 실행: `pytest tests/unit/domain/exceptions/test_base.py -v`
- 예상: PASSED

**3. REFACTOR: HTTP 상태 코드 추가**
- 각 예외 클래스에 `http_status_code` 속성 추가
- 실행: `pytest tests/unit/domain/exceptions/test_base.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: ValidationException

**1. RED: 테스트 작성**
- 파일: `tests/unit/domain/exceptions/test_validation_exceptions.py`
- 실행: `pytest tests/unit/domain/exceptions/test_validation_exceptions.py -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/domain/exceptions/validation_exceptions.py`
- 구현: `ValidationException`, `InvalidEmailException` 등
- 실행: `pytest tests/unit/domain/exceptions/test_validation_exceptions.py -v`
- 예상: PASSED

**3. REFACTOR: 예외 메시지 템플릿화**
- 실행: `pytest tests/unit/domain/exceptions/test_validation_exceptions.py -v`
- 예상: PASSED (유지)

---

#### Phase 3: AuthException

**1. RED: 테스트 작성**
- 파일: `tests/unit/domain/exceptions/test_auth_exceptions.py`
- 실행: `pytest tests/unit/domain/exceptions/test_auth_exceptions.py -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/domain/exceptions/auth_exceptions.py`
- 구현: `AuthException`, `InvalidCredentialsException` 등
- 실행: `pytest tests/unit/domain/exceptions/test_auth_exceptions.py -v`
- 예상: PASSED

**3. REFACTOR: HTTP 상태 코드 할당**
- `InvalidCredentialsException`: 401
- `EmailAlreadyExistsException`: 409
- `UnauthorizedException`: 403
- 실행: `pytest tests/unit/domain/exceptions/test_auth_exceptions.py -v`
- 예상: PASSED (유지)

---

### 검증 체크리스트

- [ ] 모든 예외 클래스에 대한 테스트 작성
- [ ] RED-GREEN-REFACTOR 사이클 준수
- [ ] 예외 계층 구조 명확히 정의
- [ ] HTTP 상태 코드 매핑
- [ ] 에러 메시지 형식 통일
- [ ] 문서화 완료 (언제 사용하는지 명시)

---

## 3.6 Database 설정

### 개요
- **목적**: SQLAlchemy 데이터베이스 연결 및 설정
- **파일 위치**:
  - 설정: `app/config.py`
  - 확장: `app/extensions.py`
  - 앱 팩토리: `app/__init__.py`
- **테스트 위치**: `tests/unit/test_config.py`

---

### 테스트 시나리오

#### 3.6.1 환경변수 로드 테스트

**정상 케이스**
- Given: `.env` 파일에 `DATABASE_URL=postgresql://...` 설정
- When: `Config` 클래스 로드
- Then: `Config.SQLALCHEMY_DATABASE_URI`에 값 로드됨

**에러 케이스**
- Given: `.env` 파일에 `DATABASE_URL` 미설정
- When: `Config` 클래스 로드
- Then: `ConfigurationException` 발생 (message: "DATABASE_URL not set")

---

#### 3.6.2 SQLAlchemy 초기화 테스트

**정상 케이스**
- Given: Flask 앱과 유효한 `Config`
- When: `db.init_app(app)` 호출
- Then: SQLAlchemy 정상 초기화

**통합 테스트**
- Given: 초기화된 Flask 앱
- When: `db.session.execute(text("SELECT 1"))` 실행
- Then: 쿼리 실행 성공

---

### 구현 계획 (TDD 사이클)

#### Phase 1: Config 클래스

**1. RED: 테스트 작성**
- 파일: `tests/unit/test_config.py`
- 실행: `pytest tests/unit/test_config.py::test_config_loads_database_url -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/config.py`
- 구현:
  ```python
  import os
  from dotenv import load_dotenv

  load_dotenv()

  class Config:
      SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
      SQLALCHEMY_TRACK_MODIFICATIONS = False
      SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

      if not SQLALCHEMY_DATABASE_URI:
          raise ValueError("DATABASE_URL not set in environment variables")
  ```
- 실행: `pytest tests/unit/test_config.py::test_config_loads_database_url -v`
- 예상: PASSED

**3. REFACTOR: 환경별 Config 클래스 분리**
- `DevelopmentConfig`, `ProductionConfig`, `TestConfig` 분리
- 실행: `pytest tests/unit/test_config.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: SQLAlchemy 초기화

**1. RED: 통합 테스트 작성**
- 파일: `tests/integration/test_database.py`
- 실행: `pytest tests/integration/test_database.py::test_db_connection -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/extensions.py`
- 구현:
  ```python
  from flask_sqlalchemy import SQLAlchemy

  db = SQLAlchemy()
  ```
- 파일: `app/__init__.py`
- 구현:
  ```python
  from flask import Flask
  from app.extensions import db
  from app.config import Config

  def create_app(config_class=Config):
      app = Flask(__name__)
      app.config.from_object(config_class)

      db.init_app(app)

      return app
  ```
- 실행: `pytest tests/integration/test_database.py::test_db_connection -v`
- 예상: PASSED

**3. REFACTOR: 마이그레이션 설정 추가**
- Flask-Migrate 추가
- 실행: `pytest tests/integration/test_database.py -v`
- 예상: PASSED (유지)

---

### 검증 체크리스트

- [ ] 환경변수 로드 테스트 작성
- [ ] SQLAlchemy 초기화 테스트 작성
- [ ] 통합 테스트: 실제 DB 연결 확인
- [ ] 환경별 Config 분리 (Development, Production, Test)
- [ ] Flask-Migrate 설정 완료
- [ ] 문서화 완료 (환경변수 목록 명시)

---

## 3.7 Supabase Storage 연동

### 개요
- **목적**: Supabase Storage API를 사용한 파일 업로드/다운로드/삭제
- **파일 위치**:
  - 인터페이스: `app/infrastructure/external/interfaces/i_storage_provider.py`
  - 구현체: `app/infrastructure/external/supabase/supabase_storage.py`
  - 테스트: `tests/unit/infrastructure/external/test_supabase_storage.py`

---

### 테스트 시나리오

#### 3.7.1 파일 업로드 테스트

**정상 케이스**
- Given: 유효한 파일 객체 (JPEG 이미지)
- When: `upload(bucket="campaigns", file=file_obj, filename="test.jpg")` 호출
- Then:
  - 업로드 성공
  - 파일 URL 반환

**경계 케이스**
- Given: 큰 파일 (4.9MB)
- When: `upload(bucket="campaigns", file=large_file, filename="large.jpg")` 호출
- Then: 정상 업로드 (5MB 이하)

**에러 케이스**
- Given: 초과 크기 파일 (5.1MB)
- When: `upload(bucket="campaigns", file=oversized_file, filename="oversized.jpg")` 호출
- Then: `StorageException` 발생 (message: "File size exceeds 5MB limit")

- Given: 지원하지 않는 파일 형식 (.exe)
- When: `upload(bucket="campaigns", file=exe_file, filename="virus.exe")` 호출
- Then: `StorageException` 발생 (message: "File type not supported")

---

#### 3.7.2 파일 다운로드 테스트

**정상 케이스**
- Given: 업로드된 파일의 경로 "campaigns/test.jpg"
- When: `get_public_url(bucket="campaigns", path="test.jpg")` 호출
- Then: 공개 URL 반환

**에러 케이스**
- Given: 존재하지 않는 파일 경로
- When: `get_public_url(bucket="campaigns", path="nonexistent.jpg")` 호출
- Then: `StorageException` 발생 (message: "File not found")

---

#### 3.7.3 파일 삭제 테스트

**정상 케이스**
- Given: 업로드된 파일의 경로 "campaigns/test.jpg"
- When: `delete(bucket="campaigns", path="test.jpg")` 호출
- Then: 삭제 성공

**에러 케이스**
- Given: 존재하지 않는 파일 경로
- When: `delete(bucket="campaigns", path="nonexistent.jpg")` 호출
- Then: `StorageException` 발생 (message: "File not found")

---

### 구현 계획 (TDD 사이클)

#### Phase 1: 파일 업로드

**1. RED: 테스트 작성**
- 파일: `tests/unit/infrastructure/external/test_supabase_storage.py`
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py::test_upload_success -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 파일: `app/infrastructure/external/supabase/supabase_storage.py`
- 구현:
  ```python
  class SupabaseStorageProvider(IStorageProvider):
      def upload(self, bucket: str, file, filename: str) -> str:
          # 파일 크기 검증
          # 파일 형식 검증
          # Supabase Storage API 호출
          response = self.client.storage.from_(bucket).upload(filename, file)
          return self.get_public_url(bucket, filename)
  ```
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py::test_upload_success -v`
- 예상: PASSED

**3. REFACTOR: 검증 로직 분리**
- `_validate_file_size()`, `_validate_file_type()` 메서드 추가
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py -v`
- 예상: PASSED (유지)

---

#### Phase 2: 파일 다운로드 (공개 URL 생성)

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py::test_get_public_url -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: `get_public_url()` 메서드
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py::test_get_public_url -v`
- 예상: PASSED

**3. REFACTOR: URL 캐싱 로직 추가**
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py -v`
- 예상: PASSED (유지)

---

#### Phase 3: 파일 삭제

**1. RED: 테스트 작성**
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py::test_delete_success -v`
- 예상: FAILED

**2. GREEN: 최소 구현**
- 구현: `delete()` 메서드
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py::test_delete_success -v`
- 예상: PASSED

**3. REFACTOR: 예외 처리 개선**
- 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py -v`
- 예상: PASSED (유지)

---

### 검증 체크리스트

- [ ] 모든 Storage 기능에 대한 테스트 시나리오 작성
- [ ] RED-GREEN-REFACTOR 사이클 준수
- [ ] Mock을 사용한 Supabase API 호출 격리
- [ ] 파일 크기 및 형식 검증 로직 포함
- [ ] 에러 케이스 테스트 포함
- [ ] 테스트 커버리지 80% 이상
- [ ] 문서화 완료

---

## 4. 구현 순서

### 4.1 Phase 1: 기초 인프라 (Week 1)

#### 우선순위 1
1. **Config 및 Database 설정**
   - `app/config.py`: 환경변수 로드
   - `app/extensions.py`: SQLAlchemy 초기화
   - 테스트: `tests/unit/test_config.py`
   - 실행: `pytest tests/unit/test_config.py -v`

2. **Domain Exceptions**
   - `app/domain/exceptions/base.py`: 베이스 예외
   - `app/domain/exceptions/validation_exceptions.py`
   - `app/domain/exceptions/auth_exceptions.py`
   - 테스트: `tests/unit/domain/exceptions/`
   - 실행: `pytest tests/unit/domain/exceptions/ -v`

---

### 4.2 Phase 2: Value Objects (Week 1)

#### 우선순위 2
3. **Email Value Object**
   - `app/domain/value_objects/email.py`
   - 테스트: `tests/unit/domain/value_objects/test_email.py`
   - 실행: `pytest tests/unit/domain/value_objects/test_email.py -v`

4. **PhoneNumber Value Object**
   - `app/domain/value_objects/phone_number.py`
   - 테스트: `tests/unit/domain/value_objects/test_phone_number.py`
   - 실행: `pytest tests/unit/domain/value_objects/test_phone_number.py -v`

5. **BusinessNumber Value Object**
   - `app/domain/value_objects/business_number.py`
   - 테스트: `tests/unit/domain/value_objects/test_business_number.py`
   - 실행: `pytest tests/unit/domain/value_objects/test_business_number.py -v`

6. **SocialChannel Value Object**
   - `app/domain/value_objects/social_channel.py`
   - 테스트: `tests/unit/domain/value_objects/test_social_channel.py`
   - 실행: `pytest tests/unit/domain/value_objects/test_social_channel.py -v`

---

### 4.3 Phase 3: 외부 서비스 연동 (Week 2)

#### 우선순위 3
7. **Supabase Auth 연동**
   - 인터페이스: `app/infrastructure/external/interfaces/i_auth_provider.py`
   - 구현체: `app/infrastructure/external/supabase/supabase_auth.py`
   - 테스트: `tests/unit/infrastructure/external/test_supabase_auth.py`
   - 실행: `pytest tests/unit/infrastructure/external/test_supabase_auth.py -v`

8. **Supabase Storage 연동**
   - 인터페이스: `app/infrastructure/external/interfaces/i_storage_provider.py`
   - 구현체: `app/infrastructure/external/supabase/supabase_storage.py`
   - 테스트: `tests/unit/infrastructure/external/test_supabase_storage.py`
   - 실행: `pytest tests/unit/infrastructure/external/test_supabase_storage.py -v`

---

### 4.4 Phase 4: 공통 유틸리티 및 데코레이터 (Week 2)

#### 우선순위 4
9. **DateTimeUtils**
   - `app/shared/utils/datetime_utils.py`
   - 테스트: `tests/unit/shared/utils/test_datetime_utils.py`
   - 실행: `pytest tests/unit/shared/utils/test_datetime_utils.py -v`

10. **StringUtils**
    - `app/shared/utils/string_utils.py`
    - 테스트: `tests/unit/shared/utils/test_string_utils.py`
    - 실행: `pytest tests/unit/shared/utils/test_string_utils.py -v`

11. **ValidationUtils**
    - `app/shared/utils/validation_utils.py`
    - 테스트: `tests/unit/shared/utils/test_validation_utils.py`
    - 실행: `pytest tests/unit/shared/utils/test_validation_utils.py -v`

12. **Auth Decorators**
    - `app/shared/decorators/auth_decorators.py`
    - 테스트: `tests/unit/shared/decorators/test_auth_decorators.py`
    - 실행: `pytest tests/unit/shared/decorators/test_auth_decorators.py -v`

---

### 4.5 Phase 5: 상수 정의 (Week 2)

#### 우선순위 5
13. **User Constants**
    - `app/shared/constants/user_constants.py`
    - 테스트: 간단한 값 검증 테스트
    - 실행: `pytest tests/unit/shared/constants/test_user_constants.py -v`

14. **Campaign Constants**
    - `app/shared/constants/campaign_constants.py`
    - 테스트: 간단한 값 검증 테스트
    - 실행: `pytest tests/unit/shared/constants/test_campaign_constants.py -v`

---

## 5. 검증 체크리스트

### 5.1 전체 프로젝트 검증

#### TDD 프로세스 준수
- [ ] 모든 모듈이 RED → GREEN → REFACTOR 사이클을 거쳤는가?
- [ ] 테스트가 먼저 작성되었는가?
- [ ] 테스트 실패를 확인한 후 구현했는가?
- [ ] 리팩토링 후에도 테스트가 통과하는가?

#### 테스트 품질 (FIRST 원칙)
- [ ] **Fast**: 모든 단위 테스트가 밀리초 단위로 실행되는가?
- [ ] **Independent**: 테스트 간 공유 상태가 없는가?
- [ ] **Repeatable**: 매번 동일한 결과를 반환하는가?
- [ ] **Self-validating**: Pass/Fail만으로 판단 가능한가?
- [ ] **Timely**: 구현 직전에 작성되었는가?

#### 테스트 커버리지
- [ ] 전체 테스트 커버리지 80% 이상
- [ ] 모든 공통 모듈에 대한 단위 테스트 존재
- [ ] 정상 케이스 + 경계 케이스 + 에러 케이스 포함

#### 코드 품질
- [ ] 타입 힌트 사용 (Python 3.11+)
- [ ] Docstring 작성 완료
- [ ] Black 포매터 적용
- [ ] Pylint/Flake8 린팅 통과

#### 문서화
- [ ] 각 모듈의 목적 및 사용법 문서화
- [ ] 테스트 시나리오 문서화
- [ ] 환경변수 목록 명시 (`.env.example`)
- [ ] README에 공통 모듈 설치 및 사용법 추가

---

### 5.2 Phase별 검증

#### Phase 1 완료 기준
- [ ] Config 클래스 구현 및 테스트 통과
- [ ] SQLAlchemy 초기화 및 통합 테스트 통과
- [ ] 모든 Domain Exceptions 구현 및 테스트 통과

#### Phase 2 완료 기준
- [ ] 4개의 Value Objects 구현 및 테스트 통과
- [ ] 불변성 보장 검증
- [ ] `__eq__`, `__hash__` 메서드 구현

#### Phase 3 완료 기준
- [ ] Supabase Auth 연동 구현 및 테스트 통과
- [ ] Supabase Storage 연동 구현 및 테스트 통과
- [ ] Mock을 사용한 외부 API 호출 격리

#### Phase 4 완료 기준
- [ ] 3개의 Utils 모듈 구현 및 테스트 통과
- [ ] Auth Decorators 구현 및 테스트 통과
- [ ] Flask 통합 테스트 통과

#### Phase 5 완료 기준
- [ ] 2개의 Constants 모듈 구현 및 테스트 통과
- [ ] 전체 프로젝트 통합 테스트 통과

---

### 5.3 최종 검증

#### 전체 테스트 실행
```bash
# 모든 단위 테스트 실행
pytest tests/unit/ -v

# 모든 통합 테스트 실행
pytest tests/integration/ -v

# 전체 테스트 실행
pytest tests/ -v

# 테스트 커버리지 확인
pytest --cov=app tests/ --cov-report=html
```

#### 커버리지 목표
- 전체: 80% 이상
- Domain Layer: 90% 이상
- Infrastructure Layer: 70% 이상
- Shared Layer: 85% 이상

---

## 6. 참고 문서

- `docs/prd.md`: 제품 요구사항 정의
- `docs/database.md`: 데이터베이스 설계
- `docs/userflow.md`: 사용자 플로우
- `docs/tech_stack_recommendation.md`: 기술 스택 권장사항
- `docs/rules/tdd.md`: TDD 프로세스 가이드라인
- `CLAUDE.md`: Layered Architecture 설계

---

## 7. 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| 1.0.0 | 2025-11-14 | 초기 공통 모듈 설계 및 TDD 구현 계획 작성 | Claude |

---

**문서 끝**
