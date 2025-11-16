# Korean Text
코드를 생성한 후에 utf-8 기준으로 깨지는 한글이 있는지 확인해주세요. 만약 있다면 수정해주세요.
항상 한국어로 응답하세요.


코드 수정 작업을 완료한 뒤 commit을 남겨주세요. message는 최근 기록을 참고해서 적절히 작성하세요.

# SOT(Source Of Truth) Design
docs폴더의 문서를 참고하여 프로그램 구조를 파악하세요. docs/external에는 외부서비스 연동 관련 문서가 있으니 필요시 확인하여 파악하세요.

## Workflow Guard
- 신규 훅이나 자동화 스크립트를 추가할 때는 기존 개발 흐름을 방해하지 않도록 필수 메시지와 최소 부수 효과만 남기고 자연스럽게 동작하게 구성하세요.

---

# Codebase Structure

## 아키텍처 원칙

### Layered Architecture
본 프로젝트는 **4-Tier Layered Architecture**를 따릅니다:

1. **Presentation Layer** (프레젠테이션 계층)
2. **Application/Service Layer** (애플리케이션/서비스 계층)
3. **Domain/Business Logic Layer** (도메인/비즈니스 로직 계층)
4. **Data Access/Persistence Layer** (데이터 접근/영속성 계층)

### SOLID 원칙 적용

#### 1. Single Responsibility Principle (단일 책임 원칙)
- 각 모듈, 클래스, 함수는 **하나의 책임**만 가집니다.
- 예: 인증 로직은 `services/auth_service.py`, 사용자 도메인 로직은 `domain/user_domain.py`

#### 2. Open/Closed Principle (개방/폐쇄 원칙)
- 확장에는 열려있고, 수정에는 닫혀있습니다.
- 추상화(ABC, Protocol)를 통한 인터페이스 정의로 구현체 교체 가능

#### 3. Liskov Substitution Principle (리스코프 치환 원칙)
- 인터페이스 구현체는 언제든 교체 가능합니다.
- 예: `IAuthProvider` 인터페이스를 구현한 `SupabaseAuthProvider`, `CustomAuthProvider` 교체 가능

#### 4. Interface Segregation Principle (인터페이스 분리 원칙)
- 큰 인터페이스를 작은 단위로 분리합니다.
- 예: `IUserRepository`, `ICampaignRepository` 등 도메인별 인터페이스 분리

#### 5. Dependency Inversion Principle (의존성 역전 원칙)
- 고수준 모듈은 저수준 모듈에 의존하지 않습니다.
- 모두 추상화(인터페이스)에 의존합니다.
- 예: Service는 Repository 인터페이스에 의존, 구체적인 구현체는 의존성 주입(DI)

---

## Directory Structure

```
1st_bungae/
├── app/
│   ├── __init__.py                    # Flask 앱 팩토리
│   ├── config.py                      # 설정 (환경변수 로드)
│   ├── extensions.py                  # Flask 확장 초기화
│   │
│   ├── presentation/                  # Presentation Layer
│   │   ├── __init__.py
│   │   ├── routes/                    # 라우트 (HTTP 엔드포인트)
│   │   │   ├── __init__.py
│   │   │   ├── main_routes.py        # 홈, 체험단 탐색
│   │   │   ├── auth_routes.py        # 로그인, 회원가입
│   │   │   ├── advertiser_routes.py  # 광고주 전용 라우트
│   │   │   ├── influencer_routes.py  # 인플루언서 전용 라우트
│   │   │   └── campaign_routes.py    # 체험단 관련 라우트
│   │   │
│   │   ├── forms/                     # WTForms (폼 검증)
│   │   │   ├── __init__.py
│   │   │   ├── auth_forms.py         # 로그인/회원가입 폼
│   │   │   ├── advertiser_forms.py   # 광고주 정보 등록 폼
│   │   │   ├── influencer_forms.py   # 인플루언서 정보 등록 폼
│   │   │   └── campaign_forms.py     # 체험단 등록 폼
│   │   │
│   │   ├── schemas/                   # DTO (Data Transfer Object)
│   │   │   ├── __init__.py
│   │   │   ├── auth_schemas.py       # 인증 요청/응답 DTO
│   │   │   ├── advertiser_schemas.py # 광고주 DTO
│   │   │   ├── influencer_schemas.py # 인플루언서 DTO
│   │   │   └── campaign_schemas.py   # 체험단 DTO
│   │   │
│   │   └── templates/                 # Jinja2 템플릿
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── auth/
│   │       │   ├── login.html
│   │       │   └── register.html
│   │       ├── advertiser/
│   │       │   ├── dashboard.html
│   │       │   └── campaign_detail.html
│   │       ├── influencer/
│   │       │   └── profile.html
│   │       └── campaign/
│   │           ├── list.html
│   │           ├── detail.html
│   │           └── apply.html
│   │
│   ├── application/                   # Application/Service Layer
│   │   ├── __init__.py
│   │   ├── services/                  # 애플리케이션 서비스 (유스케이스)
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # 인증/인가 서비스
│   │   │   ├── user_service.py       # 사용자 관리 서비스
│   │   │   ├── advertiser_service.py # 광고주 서비스
│   │   │   ├── influencer_service.py # 인플루언서 서비스
│   │   │   ├── campaign_service.py   # 체험단 관리 서비스
│   │   │   └── application_service.py # 체험단 지원 서비스
│   │   │
│   │   └── interfaces/                # 서비스 인터페이스 (ABC)
│   │       ├── __init__.py
│   │       ├── i_auth_service.py
│   │       ├── i_user_service.py
│   │       └── i_campaign_service.py
│   │
│   ├── domain/                        # Domain/Business Logic Layer
│   │   ├── __init__.py
│   │   ├── entities/                  # 도메인 엔티티 (순수 비즈니스 객체)
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # 사용자 엔티티
│   │   │   ├── advertiser.py         # 광고주 엔티티
│   │   │   ├── influencer.py         # 인플루언서 엔티티
│   │   │   ├── campaign.py           # 체험단 엔티티
│   │   │   └── application.py        # 지원 엔티티
│   │   │
│   │   ├── value_objects/             # 값 객체 (불변 객체)
│   │   │   ├── __init__.py
│   │   │   ├── email.py              # 이메일 값 객체
│   │   │   ├── phone_number.py       # 전화번호 값 객체
│   │   │   ├── business_number.py    # 사업자번호 값 객체
│   │   │   └── social_channel.py     # SNS 채널 값 객체
│   │   │
│   │   ├── business_rules/            # 비즈니스 규칙 (도메인 로직)
│   │   │   ├── __init__.py
│   │   │   ├── campaign_rules.py     # 체험단 규칙 (모집 종료, 선정 등)
│   │   │   ├── application_rules.py  # 지원 규칙 (자격 검증)
│   │   │   └── user_rules.py         # 사용자 규칙 (권한 검증)
│   │   │
│   │   └── exceptions/                # 도메인 예외
│   │       ├── __init__.py
│   │       ├── base.py               # 베이스 도메인 예외
│   │       ├── auth_exceptions.py    # 인증 예외
│   │       ├── campaign_exceptions.py # 체험단 예외
│   │       └── validation_exceptions.py # 검증 예외
│   │
│   ├── infrastructure/                # Data Access/Persistence Layer
│   │   ├── __init__.py
│   │   ├── persistence/               # 영속성 (ORM 모델)
│   │   │   ├── __init__.py
│   │   │   ├── models/               # SQLAlchemy 모델
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_model.py     # User 테이블 모델
│   │   │   │   ├── advertiser_model.py # Advertiser 테이블 모델
│   │   │   │   ├── influencer_model.py # Influencer 테이블 모델
│   │   │   │   ├── campaign_model.py  # Campaign 테이블 모델
│   │   │   │   └── application_model.py # Application 테이블 모델
│   │   │   │
│   │   │   └── mappers/              # 도메인 엔티티 ↔ ORM 모델 매퍼
│   │   │       ├── __init__.py
│   │   │       ├── user_mapper.py
│   │   │       ├── campaign_mapper.py
│   │   │       └── application_mapper.py
│   │   │
│   │   ├── repositories/              # Repository 구현체
│   │   │   ├── __init__.py
│   │   │   ├── interfaces/           # Repository 인터페이스
│   │   │   │   ├── __init__.py
│   │   │   │   ├── i_user_repository.py
│   │   │   │   ├── i_advertiser_repository.py
│   │   │   │   ├── i_influencer_repository.py
│   │   │   │   ├── i_campaign_repository.py
│   │   │   │   └── i_application_repository.py
│   │   │   │
│   │   │   ├── user_repository.py    # User Repository 구현
│   │   │   ├── advertiser_repository.py
│   │   │   ├── influencer_repository.py
│   │   │   ├── campaign_repository.py
│   │   │   └── application_repository.py
│   │   │
│   │   └── external/                  # 외부 서비스 연동
│   │       ├── __init__.py
│   │       ├── interfaces/           # 외부 서비스 인터페이스
│   │       │   ├── __init__.py
│   │       │   ├── i_auth_provider.py   # 인증 제공자 인터페이스
│   │       │   └── i_storage_provider.py # 스토리지 제공자 인터페이스
│   │       │
│   │       ├── supabase/             # Supabase 구현체
│   │       │   ├── __init__.py
│   │       │   ├── supabase_client.py   # Supabase 클라이언트
│   │       │   ├── supabase_auth.py     # Supabase Auth 구현
│   │       │   └── supabase_storage.py  # Supabase Storage 구현
│   │       │
│   │       └── email/                # 이메일 서비스
│   │           ├── __init__.py
│   │           └── email_sender.py
│   │
│   └── shared/                        # 공통 유틸리티
│       ├── __init__.py
│       ├── utils/                     # 범용 유틸리티
│       │   ├── __init__.py
│       │   ├── datetime_utils.py     # 날짜/시간 유틸
│       │   ├── string_utils.py       # 문자열 유틸
│       │   └── validation_utils.py   # 검증 유틸
│       │
│       ├── decorators/                # 데코레이터
│       │   ├── __init__.py
│       │   ├── auth_decorators.py    # 인증 데코레이터
│       │   └── error_decorators.py   # 에러 핸들링 데코레이터
│       │
│       └── constants/                 # 상수
│           ├── __init__.py
│           ├── user_constants.py
│           └── campaign_constants.py
│
├── migrations/                        # Alembic 마이그레이션
│   ├── versions/
│   └── env.py
│
├── tests/                             # 테스트
│   ├── __init__.py
│   ├── unit/                         # 단위 테스트
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/                  # 통합 테스트
│   │   ├── repositories/
│   │   └── services/
│   └── e2e/                          # E2E 테스트
│       └── routes/
│
├── docs/                              # 문서
│   ├── requirement.md
│   ├── tech_stack_recommendation.md
│   ├── rules/
│   │   └── tdd.md
│   └── external/                     # 외부 서비스 문서
│
├── app.py                             # 애플리케이션 엔트리포인트
├── requirements.txt                   # Python 의존성
├── render.yaml                        # Render 배포 설정
├── .env.example                       # 환경변수 예시
├── .gitignore
└── README.md
```

---

## Top-Level Building Blocks

### 1. Presentation Layer (프레젠테이션 계층)
**책임**: HTTP 요청/응답 처리, 사용자 인터페이스 렌더링

- **Routes**: HTTP 엔드포인트 정의
  - `main_routes.py`: 홈, 체험단 탐색
  - `auth_routes.py`: 로그인, 회원가입
  - `advertiser_routes.py`: 광고주 대시보드, 체험단 관리
  - `influencer_routes.py`: 인플루언서 프로필, 체험단 지원
  - `campaign_routes.py`: 체험단 상세, 지원

- **Forms**: WTForms를 사용한 폼 검증 및 CSRF 보호
  - 각 도메인별 입력 검증

- **Schemas**: DTO (Data Transfer Object)
  - API 요청/응답 데이터 구조 정의
  - Presentation과 Application 계층 간 데이터 전달

- **Templates**: Jinja2 템플릿 (SSR)
  - Bootstrap 5 기반 UI

**의존성**: `Application Layer (Services)`만 의존

---

### 2. Application/Service Layer (애플리케이션/서비스 계층)
**책임**: 유스케이스 구현, 트랜잭션 관리, 도메인 로직 오케스트레이션

- **Services**: 애플리케이션 서비스 (비즈니스 플로우)
  - `auth_service.py`: 로그인, 회원가입, 토큰 관리
  - `user_service.py`: 사용자 정보 관리
  - `advertiser_service.py`: 광고주 정보 등록/수정
  - `influencer_service.py`: 인플루언서 정보 등록/수정
  - `campaign_service.py`: 체험단 생성, 모집 종료, 선정
  - `application_service.py`: 체험단 지원, 지원 내역 조회

- **Interfaces**: 서비스 인터페이스 (ABC)
  - 서비스 계약 정의
  - 테스트 시 Mock 객체 생성 용이

**의존성**:
- `Domain Layer (Entities, Business Rules)`에 의존
- `Infrastructure Layer (Repositories, External Services)`의 **인터페이스**에 의존

---

### 3. Domain/Business Logic Layer (도메인/비즈니스 로직 계층)
**책임**: 순수 비즈니스 로직, 도메인 규칙

- **Entities**: 도메인 엔티티 (비즈니스 객체)
  - `user.py`: 사용자 엔티티
  - `advertiser.py`: 광고주 엔티티
  - `influencer.py`: 인플루언서 엔티티
  - `campaign.py`: 체험단 엔티티
  - `application.py`: 지원 엔티티

- **Value Objects**: 불변 값 객체
  - `email.py`: 이메일 검증 로직 포함
  - `phone_number.py`: 전화번호 포맷 검증
  - `business_number.py`: 사업자번호 검증
  - `social_channel.py`: SNS 채널 URL 검증

- **Business Rules**: 비즈니스 규칙
  - `campaign_rules.py`:
    - 모집 종료 가능 여부 검증
    - 인플루언서 선정 가능 여부 검증
  - `application_rules.py`:
    - 지원 자격 검증 (인플루언서 정보 등록 여부)
    - 중복 지원 방지
  - `user_rules.py`:
    - 권한 검증 (광고주/인플루언서)

- **Exceptions**: 도메인 예외
  - 비즈니스 규칙 위반 시 발생하는 예외

**의존성**: **없음** (순수 Python, 외부 프레임워크 의존 금지)

---

### 4. Infrastructure/Data Access Layer (인프라/데이터 접근 계층)
**책임**: 데이터 영속성, 외부 서비스 연동

#### 4.1 Persistence (영속성)
- **Models**: SQLAlchemy ORM 모델
  - 데이터베이스 테이블 정의
  - PostgreSQL 매핑

- **Mappers**: 도메인 엔티티 ↔ ORM 모델 변환
  - 도메인 계층과 영속성 계층 분리
  - 예: `UserMapper.to_entity()`, `UserMapper.to_model()`

#### 4.2 Repositories (저장소)
- **Interfaces**: Repository 인터페이스
  - CRUD 메서드 정의
  - 도메인 중심 쿼리 메서드 (예: `find_by_email()`)

- **Implementations**: Repository 구현체
  - SQLAlchemy를 사용한 데이터 접근
  - 트랜잭션 처리

#### 4.3 External (외부 서비스)
- **Interfaces**: 외부 서비스 인터페이스
  - `i_auth_provider.py`: 인증 제공자 계약
  - `i_storage_provider.py`: 스토리지 제공자 계약

- **Supabase**: Supabase 구현체
  - `supabase_auth.py`: Supabase Auth 연동
  - `supabase_storage.py`: Supabase Storage 연동
  - `supabase_client.py`: Supabase 클라이언트 초기화

- **Email**: 이메일 서비스
  - 이메일 인증 발송

**의존성**:
- `Domain Layer (Entities)`에 의존
- 외부 라이브러리 (SQLAlchemy, Supabase, etc.)에 의존

---

### 5. Shared (공통 모듈)
**책임**: 계층 간 공유되는 유틸리티, 상수, 데코레이터

- **Utils**: 범용 유틸리티
  - 날짜/시간, 문자열, 검증 유틸

- **Decorators**: 데코레이터
  - `@login_required`: 로그인 검증
  - `@advertiser_required`: 광고주 권한 검증
  - `@influencer_required`: 인플루언서 권한 검증

- **Constants**: 상수
  - 사용자 역할, 체험단 상태 등

**의존성**: 없음 (순수 유틸리티)

---

## 의존성 흐름 (Dependency Flow)

```
Presentation Layer
    ↓ (depends on)
Application Layer
    ↓ (depends on)
Domain Layer (비즈니스 로직)
    ↑ (implements)
Infrastructure Layer
```

**핵심 원칙**:
1. **상위 계층**은 **하위 계층**에 의존
2. **하위 계층**은 **상위 계층**을 모름
3. **Domain Layer**는 **가장 독립적** (외부 의존성 없음)
4. **Infrastructure Layer**는 **인터페이스**를 통해 **Domain/Application**과 통신

---

## 계층 간 데이터 흐름 예시

### 예: 체험단 지원 (Influencer applies to Campaign)

```
1. Presentation Layer (influencer_routes.py)
   ↓ HTTP POST /campaign/<id>/apply
   ↓ Form 검증 (InfluencerApplicationForm)

2. Application Layer (application_service.py)
   ↓ apply_to_campaign(campaign_id, user_id)
   ↓ 비즈니스 플로우 오케스트레이션

3. Domain Layer
   ↓ application_rules.py: can_apply(user, campaign)
   ↓ 지원 자격 검증 (인플루언서 정보 등록 여부)
   ↓ 중복 지원 검증
   ↓ Application 엔티티 생성

4. Infrastructure Layer (application_repository.py)
   ↓ save(application_entity)
   ↓ ApplicationMapper.to_model(application_entity)
   ↓ SQLAlchemy로 DB 저장
```

---

## 분리 기준 (Separation Criteria)

### ✅ 1. Presentation과 Business Logic 분리
- **Presentation**: `app/presentation/routes`, `forms`, `templates`
- **Business Logic**: `app/domain/business_rules`, `entities`
- **분리 방법**: Routes는 Service만 호출, 도메인 로직 직접 접근 금지

### ✅ 2. Pure Business Logic과 Persistence 분리
- **Pure Business Logic**: `app/domain/` (순수 Python)
- **Persistence**: `app/infrastructure/persistence/` (SQLAlchemy)
- **분리 방법**:
  - Domain Entities는 ORM 의존성 없음
  - Mapper를 통한 Entity ↔ Model 변환

### ✅ 3. Internal Logic과 External Contract 분리
- **Internal Logic**: `app/application/services`, `app/domain`
- **External Contract**: `app/infrastructure/external/interfaces`
- **분리 방법**:
  - 인터페이스 정의 (ABC)
  - 외부 서비스 구현체는 Infrastructure에서 구현
  - Service는 인터페이스에만 의존

### ✅ 4. 단일 책임 원칙 (Single Responsibility)
- 각 모듈은 하나의 책임만 가짐
- 예:
  - `auth_service.py`: 인증/인가만 담당
  - `campaign_service.py`: 체험단 관리만 담당
  - `application_service.py`: 지원 관리만 담당

---

## 의존성 주입 (Dependency Injection)

### Flask 앱 팩토리에서 DI 구성

```python
# app/__init__.py
def create_app():
    app = Flask(__name__)

    # Repository 인스턴스 생성
    user_repo = UserRepository(db)
    campaign_repo = CampaignRepository(db)

    # External Services 인스턴스 생성
    auth_provider = SupabaseAuthProvider()

    # Service 인스턴스 생성 (DI)
    auth_service = AuthService(user_repo, auth_provider)
    campaign_service = CampaignService(campaign_repo, user_repo)

    # Routes에 Service 주입
    app.register_blueprint(create_auth_routes(auth_service))
    app.register_blueprint(create_campaign_routes(campaign_service))

    return app
```

---

## 테스트 전략

### Unit Tests (단위 테스트)
- **Domain Layer**: 순수 비즈니스 로직 테스트
  - `tests/unit/domain/test_campaign_rules.py`
  - Mock 없이 순수 함수 테스트

### Integration Tests (통합 테스트)
- **Service + Repository**: 실제 DB 연동 테스트
  - `tests/integration/services/test_campaign_service.py`
  - TestDB 사용 (SQLite in-memory)

### E2E Tests (End-to-End)
- **Routes**: HTTP 요청/응답 테스트
  - `tests/e2e/routes/test_campaign_routes.py`
  - Flask Test Client 사용

---

## 확장 가능성 (Extensibility)

### 외부 서비스 교체 예시

#### Supabase Auth → Custom Auth 전환
```python
# 기존: SupabaseAuthProvider
# 신규: CustomAuthProvider

# 변경 필요: app/__init__.py (DI 설정)
# auth_provider = SupabaseAuthProvider()  # 기존
auth_provider = CustomAuthProvider()      # 신규

# 변경 불필요:
# - auth_service.py (인터페이스에 의존)
# - auth_routes.py (서비스에만 의존)
```

---

## 마이그레이션 가이드

### 현재 구조 → 신규 구조 전환

1. **Step 1**: `app/domain/` 생성 및 엔티티 이동
2. **Step 2**: `app/infrastructure/persistence/models/` 생성 및 ORM 모델 분리
3. **Step 3**: `app/infrastructure/repositories/` 생성 및 Repository 구현
4. **Step 4**: `app/application/services/` 생성 및 Service 이동
5. **Step 5**: `app/presentation/routes/` 생성 및 Routes 리팩토링
6. **Step 6**: DI 설정 (`app/__init__.py`)

---

## 참고 문서
- `docs/requirement.md`: 기능 요구사항
- `docs/tech_stack_recommendation.md`: 기술 스택
- `docs/rules/tdd.md`: TDD 규칙
