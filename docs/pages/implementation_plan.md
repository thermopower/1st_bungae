# 전체 페이지 구현 계획서
# 체험단 매칭 플랫폼 "1st_bungae"

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | 전체 페이지 구현 계획서 |
| **프로젝트명** | 1st_bungae |
| **버전** | 1.0.0 |
| **작성일** | 2025-11-14 |
| **아키텍처** | 4-Tier Layered Architecture |

---

## 목차

1. [개요](#1-개요)
2. [공통 페이지 구현 계획](#2-공통-페이지-구현-계획)
   - [2.1 홈 (Home) - 체험단 탐색](#21-홈-home---체험단-탐색)
   - [2.2 로그인 (Login)](#22-로그인-login)
   - [2.3 회원가입 (Register)](#23-회원가입-register)
3. [회원 유형 등록 페이지 구현 계획](#3-회원-유형-등록-페이지-구현-계획)
   - [3.1 광고주 정보 등록](#31-광고주-정보-등록)
   - [3.2 인플루언서 정보 등록](#32-인플루언서-정보-등록)
4. [체험단 관련 페이지 구현 계획](#4-체험단-관련-페이지-구현-계획)
   - [4.1 체험단 상세 (Campaign Detail)](#41-체험단-상세-campaign-detail)
   - [4.2 체험단 지원 (Campaign Application)](#42-체험단-지원-campaign-application)
5. [광고주 전용 페이지 구현 계획](#5-광고주-전용-페이지-구현-계획)
   - [5.1 광고주 대시보드](#51-광고주-대시보드)
   - [5.2 광고주 체험단 상세](#52-광고주-체험단-상세)
6. [테스트 전략](#6-테스트-전략)
7. [구현 우선순위](#7-구현-우선순위)

---

## 1. 개요

### 1.1 문서 목적

본 문서는 체험단 매칭 플랫폼 "1st_bungae"의 모든 페이지에 대한 구현 계획을 정의합니다. 각 페이지는 **4-Tier Layered Architecture**를 따르며, TDD(Test-Driven Development) 프로세스를 통해 구현됩니다.

### 1.2 아키텍처 개요

```
┌─────────────────────────────────┐
│   Presentation Layer            │  Routes, Forms, Schemas, Templates
├─────────────────────────────────┤
│   Application/Service Layer     │  Services, Interfaces
├─────────────────────────────────┤
│   Domain/Business Logic Layer   │  Entities, Business Rules, Exceptions
├─────────────────────────────────┤
│   Infrastructure Layer          │  Models, Repositories, Mappers, External Services
└─────────────────────────────────┘
```

### 1.3 구현 원칙

1. **Layered Architecture**: 각 계층의 책임을 명확히 분리
2. **SOLID 원칙**: 단일 책임, 개방/폐쇄, 리스코프 치환, 인터페이스 분리, 의존성 역전
3. **TDD (Test-Driven Development)**: Red → Green → Refactor 사이클
4. **DI (Dependency Injection)**: Flask 앱 팩토리에서 의존성 주입
5. **Clean Code**: 명확한 네이밍, 작은 함수, 적절한 추상화

---

## 2. 공통 페이지 구현 계획

### 2.1 홈 (Home) - 체험단 탐색

#### 페이지 정보
- **URL**: `/`
- **접근 권한**: 모든 사용자 (비로그인 포함)
- **관련 유스케이스**: UC-005 (체험단 탐색)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/main_routes.py

@main_bp.route('/')
def home():
    """
    홈 페이지 - 체험단 목록 표시
    GET 파라미터:
    - page: 페이지 번호 (기본값: 1)
    - sort: 정렬 기준 (latest, deadline, popular)
    - category: 카테고리 필터 (Phase 2)
    """
    pass
```

##### Forms
- 해당 없음 (검색/필터 폼은 Phase 2)

##### Schemas
```python
# app/presentation/schemas/campaign_schemas.py

@dataclass
class CampaignListItemDTO:
    """체험단 목록 아이템 DTO"""
    id: int
    title: str
    description_short: str  # 100자 이하
    image_url: Optional[str]
    quota: int
    application_count: int
    deadline: date
    business_name: str
    status: str
```

##### Templates
```html
<!-- app/presentation/templates/home.html -->
- 체험단 카드 목록 (12개/페이지)
- 페이지네이션
- 정렬 드롭다운 (최신순, 마감임박순, 인기순)
```

#### Application Layer

##### Services
```python
# app/application/services/campaign_service.py

class CampaignService:
    def list_recruiting_campaigns(
        self,
        page: int = 1,
        per_page: int = 12,
        sort: str = 'latest'
    ) -> Tuple[List[CampaignListItemDTO], int]:
        """
        모집 중인 체험단 목록 조회
        Returns: (campaigns, total_count)
        """
        pass
```

##### Interfaces
```python
# app/application/interfaces/i_campaign_service.py

class ICampaignService(ABC):
    @abstractmethod
    def list_recruiting_campaigns(
        self, page: int, per_page: int, sort: str
    ) -> Tuple[List[CampaignListItemDTO], int]:
        pass
```

#### Domain Layer

##### Entities
```python
# app/domain/entities/campaign.py

@dataclass
class Campaign:
    """체험단 도메인 엔티티"""
    id: Optional[int]
    advertiser_id: int
    title: str
    description: str
    quota: int
    start_date: date
    end_date: date
    benefits: str
    conditions: str
    image_url: Optional[str]
    status: CampaignStatus
    created_at: datetime
    closed_at: Optional[datetime]

    def is_recruiting(self) -> bool:
        """모집 중인지 확인"""
        return self.status == CampaignStatus.RECRUITING
```

##### Business Rules
```python
# app/domain/business_rules/campaign_rules.py

class CampaignRules:
    @staticmethod
    def can_close_early(campaign: Campaign) -> bool:
        """조기종료 가능 여부 검증"""
        return campaign.status == CampaignStatus.RECRUITING
```

##### Exceptions
```python
# app/domain/exceptions/campaign_exceptions.py

class CampaignNotFoundException(DomainException):
    pass

class CampaignAlreadyClosedException(DomainException):
    pass
```

#### Infrastructure Layer

##### Models
```python
# app/infrastructure/persistence/models/campaign_model.py

class CampaignModel(db.Model):
    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    # ... 기타 컬럼
```

##### Repositories
```python
# app/infrastructure/repositories/campaign_repository.py

class CampaignRepository(ICampaignRepository):
    def find_recruiting_campaigns(
        self, skip: int, limit: int, sort: str
    ) -> List[Campaign]:
        """모집 중인 체험단 조회"""
        pass
```

##### Mappers
```python
# app/infrastructure/persistence/mappers/campaign_mapper.py

class CampaignMapper:
    @staticmethod
    def to_entity(model: CampaignModel) -> Campaign:
        """ORM 모델 → 도메인 엔티티"""
        pass

    @staticmethod
    def to_model(entity: Campaign) -> CampaignModel:
        """도메인 엔티티 → ORM 모델"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/business_rules/test_campaign_rules.py
def test_can_close_early_when_recruiting():
    # Given: 모집 중인 체험단
    # When: can_close_early 호출
    # Then: True 반환
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_campaign_service.py
def test_list_recruiting_campaigns():
    # Given: DB에 모집 중인 체험단 3개 존재
    # When: list_recruiting_campaigns 호출
    # Then: 3개의 체험단 반환
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_main_routes.py
def test_home_page_displays_campaigns(client):
    # Given: 모집 중인 체험단 존재
    # When: GET /
    # Then: 200 OK, 체험단 목록 표시
    pass
```

---

### 2.2 로그인 (Login)

#### 페이지 정보
- **URL**: `/auth/login`
- **접근 권한**: 비로그인 사용자만
- **관련 유스케이스**: UC-002 (로그인)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/auth_routes.py

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    로그인 페이지
    GET: 로그인 폼 표시
    POST: 로그인 처리
    """
    pass
```

##### Forms
```python
# app/presentation/forms/auth_forms.py

class LoginForm(FlaskForm):
    """로그인 폼"""
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요'),
        Email(message='올바른 이메일 형식을 입력해주세요')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요')
    ])
    submit = SubmitField('로그인')
```

##### Schemas
```python
# app/presentation/schemas/auth_schemas.py

@dataclass
class LoginRequestDTO:
    """로그인 요청 DTO"""
    email: str
    password: str

@dataclass
class LoginResponseDTO:
    """로그인 응답 DTO"""
    user_id: str
    email: str
    role: Optional[str]
    access_token: str
    refresh_token: str
```

##### Templates
```html
<!-- app/presentation/templates/auth/login.html -->
- 이메일 입력 필드
- 비밀번호 입력 필드
- 로그인 버튼
- 회원가입 링크
```

#### Application Layer

##### Services
```python
# app/application/services/auth_service.py

class AuthService:
    def login(self, email: str, password: str) -> LoginResponseDTO:
        """
        로그인 처리
        1. Supabase Auth 인증
        2. User 정보 조회
        3. 역할 확인 (Advertiser/Influencer)
        4. 세션 생성
        """
        pass

    def get_redirect_url_after_login(self, user_id: str) -> str:
        """로그인 후 리다이렉트 URL 결정"""
        pass
```

##### Interfaces
```python
# app/application/interfaces/i_auth_service.py

class IAuthService(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> LoginResponseDTO:
        pass

    @abstractmethod
    def get_redirect_url_after_login(self, user_id: str) -> str:
        pass
```

#### Domain Layer

##### Entities
```python
# app/domain/entities/user.py

@dataclass
class User:
    """사용자 도메인 엔티티"""
    id: str  # UUID
    email: str
    role: Optional[UserRole]
    created_at: datetime

    def has_role(self) -> bool:
        """역할이 등록되었는지 확인"""
        return self.role is not None
```

##### Business Rules
```python
# app/domain/business_rules/user_rules.py

class UserRules:
    @staticmethod
    def determine_redirect_url(user: User) -> str:
        """사용자 역할에 따른 리다이렉트 URL 결정"""
        if not user.has_role():
            return '/role-selection'
        elif user.role == UserRole.ADVERTISER:
            return '/advertiser/dashboard'
        elif user.role == UserRole.INFLUENCER:
            return '/'
        else:
            raise ValueError(f"Unknown role: {user.role}")
```

##### Exceptions
```python
# app/domain/exceptions/auth_exceptions.py

class InvalidCredentialsException(DomainException):
    """이메일 또는 비밀번호 불일치"""
    pass

class EmailNotVerifiedException(DomainException):
    """이메일 미인증 (Phase 2)"""
    pass
```

#### Infrastructure Layer

##### Models
```python
# app/infrastructure/persistence/models/user_model.py

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True)  # UUID
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

##### Repositories
```python
# app/infrastructure/repositories/user_repository.py

class UserRepository(IUserRepository):
    def find_by_id(self, user_id: str) -> Optional[User]:
        """사용자 ID로 조회"""
        pass

    def find_by_email(self, email: str) -> Optional[User]:
        """이메일로 조회"""
        pass
```

##### External Services
```python
# app/infrastructure/external/supabase/supabase_auth.py

class SupabaseAuthProvider(IAuthProvider):
    def authenticate(self, email: str, password: str) -> AuthResult:
        """Supabase Auth로 인증"""
        pass

    def create_session(self, user_id: str) -> SessionTokens:
        """세션 토큰 생성"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/business_rules/test_user_rules.py
def test_determine_redirect_url_for_advertiser():
    # Given: 광고주 역할을 가진 사용자
    # When: determine_redirect_url 호출
    # Then: '/advertiser/dashboard' 반환
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_auth_service.py
def test_login_success():
    # Given: 등록된 사용자 (이메일, 비밀번호)
    # When: login 호출
    # Then: LoginResponseDTO 반환
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_auth_routes.py
def test_login_redirects_to_dashboard_for_advertiser(client):
    # Given: 광고주 사용자
    # When: POST /auth/login
    # Then: 302 Redirect to /advertiser/dashboard
    pass
```

---

### 2.3 회원가입 (Register)

#### 페이지 정보
- **URL**: `/auth/register`
- **접근 권한**: 비로그인 사용자만
- **관련 유스케이스**: UC-001 (회원가입)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/auth_routes.py

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    회원가입 페이지
    GET: 회원가입 폼 표시
    POST: 회원가입 처리
    """
    pass
```

##### Forms
```python
# app/presentation/forms/auth_forms.py

class RegisterForm(FlaskForm):
    """회원가입 폼"""
    email = StringField('이메일', validators=[
        DataRequired(message='이메일을 입력해주세요'),
        Email(message='올바른 이메일 형식을 입력해주세요')
    ])
    password = PasswordField('비밀번호', validators=[
        DataRequired(message='비밀번호를 입력해주세요'),
        Length(min=8, message='비밀번호는 최소 8자 이상이어야 합니다'),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)', message='비밀번호는 영문과 숫자를 포함해야 합니다')
    ])
    password_confirm = PasswordField('비밀번호 확인', validators=[
        DataRequired(message='비밀번호 확인을 입력해주세요'),
        EqualTo('password', message='비밀번호가 일치하지 않습니다')
    ])
    submit = SubmitField('회원가입')
```

##### Schemas
```python
# app/presentation/schemas/auth_schemas.py

@dataclass
class RegisterRequestDTO:
    """회원가입 요청 DTO"""
    email: str
    password: str

@dataclass
class RegisterResponseDTO:
    """회원가입 응답 DTO"""
    user_id: str
    email: str
```

##### Templates
```html
<!-- app/presentation/templates/auth/register.html -->
- 이메일 입력 필드
- 비밀번호 입력 필드
- 비밀번호 확인 입력 필드
- 회원가입 버튼
- 로그인 링크
```

#### Application Layer

##### Services
```python
# app/application/services/auth_service.py

class AuthService:
    def register(self, email: str, password: str) -> RegisterResponseDTO:
        """
        회원가입 처리
        1. Supabase Auth 회원가입
        2. User 테이블에 레코드 생성
        3. 세션 생성
        """
        pass
```

#### Domain Layer

##### Business Rules
```python
# app/domain/business_rules/user_rules.py

class UserRules:
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """비밀번호 강도 검증"""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Za-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
```

##### Exceptions
```python
# app/domain/exceptions/auth_exceptions.py

class EmailAlreadyExistsException(DomainException):
    """이메일 중복"""
    pass

class WeakPasswordException(DomainException):
    """비밀번호 강도 미달"""
    pass
```

#### Infrastructure Layer

##### External Services
```python
# app/infrastructure/external/supabase/supabase_auth.py

class SupabaseAuthProvider(IAuthProvider):
    def create_user(self, email: str, password: str) -> AuthUserCreationResult:
        """Supabase Auth에 사용자 생성"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/business_rules/test_user_rules.py
def test_validate_password_strength_with_valid_password():
    # Given: 영문+숫자 8자 이상 비밀번호
    # When: validate_password_strength 호출
    # Then: True 반환
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_auth_service.py
def test_register_creates_user_in_db():
    # Given: 유효한 이메일, 비밀번호
    # When: register 호출
    # Then: User 테이블에 레코드 생성
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_auth_routes.py
def test_register_redirects_to_role_selection(client):
    # Given: 유효한 회원가입 정보
    # When: POST /auth/register
    # Then: 302 Redirect to /role-selection
    pass
```

---

## 3. 회원 유형 등록 페이지 구현 계획

### 3.1 광고주 정보 등록

#### 페이지 정보
- **URL**: `/advertiser/register`
- **접근 권한**: 로그인 사용자 (역할 미등록)
- **관련 유스케이스**: UC-004 (광고주 정보 등록)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/advertiser_routes.py

@advertiser_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_advertiser():
    """
    광고주 정보 등록 페이지
    GET: 등록 폼 표시
    POST: 정보 등록 처리
    """
    pass
```

##### Forms
```python
# app/presentation/forms/advertiser_forms.py

class AdvertiserRegistrationForm(FlaskForm):
    """광고주 정보 등록 폼"""
    # 공통 정보
    name = StringField('이름', validators=[
        DataRequired(message='이름을 입력해주세요'),
        Length(min=2, max=100, message='이름은 2자 이상 100자 이하여야 합니다')
    ])
    birth_date = DateField('생년월일', validators=[
        DataRequired(message='생년월일을 입력해주세요')
    ])
    phone_number = StringField('휴대폰번호', validators=[
        DataRequired(message='휴대폰번호를 입력해주세요'),
        Regexp(r'^010-\d{4}-\d{4}$', message='올바른 휴대폰번호 형식을 입력해주세요 (010-XXXX-XXXX)')
    ])

    # 광고주 전용 정보
    business_name = StringField('업체명', validators=[
        DataRequired(message='업체명을 입력해주세요')
    ])
    address = StringField('주소', validators=[
        DataRequired(message='주소를 입력해주세요')
    ])
    business_phone = StringField('업장 전화번호', validators=[
        DataRequired(message='업장 전화번호를 입력해주세요')
    ])
    business_number = StringField('사업자등록번호', validators=[
        DataRequired(message='사업자등록번호를 입력해주세요'),
        Regexp(r'^\d{10}$', message='사업자등록번호는 10자리 숫자여야 합니다')
    ])
    representative_name = StringField('대표자명', validators=[
        DataRequired(message='대표자명을 입력해주세요')
    ])
    submit = SubmitField('등록')
```

##### Schemas
```python
# app/presentation/schemas/advertiser_schemas.py

@dataclass
class AdvertiserRegistrationRequestDTO:
    """광고주 정보 등록 요청 DTO"""
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    business_name: str
    address: str
    business_phone: str
    business_number: str
    representative_name: str
```

##### Templates
```html
<!-- app/presentation/templates/advertiser/register.html -->
- 공통 정보 입력 필드 (이름, 생년월일, 휴대폰번호)
- 광고주 전용 정보 입력 필드
- 등록 버튼
```

#### Application Layer

##### Services
```python
# app/application/services/advertiser_service.py

class AdvertiserService:
    def register_advertiser(self, dto: AdvertiserRegistrationRequestDTO) -> None:
        """
        광고주 정보 등록
        1. 중복 등록 검증
        2. 사업자등록번호 중복 검증
        3. User 테이블 업데이트 (role='advertiser')
        4. Advertiser 테이블 레코드 생성
        트랜잭션으로 처리
        """
        pass
```

##### Interfaces
```python
# app/application/interfaces/i_advertiser_service.py

class IAdvertiserService(ABC):
    @abstractmethod
    def register_advertiser(self, dto: AdvertiserRegistrationRequestDTO) -> None:
        pass
```

#### Domain Layer

##### Entities
```python
# app/domain/entities/advertiser.py

@dataclass
class Advertiser:
    """광고주 도메인 엔티티"""
    id: Optional[int]
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    business_name: str
    address: str
    business_phone: str
    business_number: str
    representative_name: str
    created_at: datetime
```

##### Value Objects
```python
# app/domain/value_objects/business_number.py

@dataclass(frozen=True)
class BusinessNumber:
    """사업자등록번호 값 객체"""
    value: str

    def __post_init__(self):
        if not re.match(r'^\d{10}$', self.value):
            raise ValueError('사업자등록번호는 10자리 숫자여야 합니다')
```

##### Business Rules
```python
# app/domain/business_rules/advertiser_rules.py

class AdvertiserRules:
    @staticmethod
    def can_register(user: User) -> bool:
        """광고주 등록 가능 여부 검증"""
        return not user.has_role()
```

##### Exceptions
```python
# app/domain/exceptions/advertiser_exceptions.py

class AdvertiserAlreadyRegisteredException(DomainException):
    """광고주 정보 이미 등록됨"""
    pass

class BusinessNumberAlreadyExistsException(DomainException):
    """사업자등록번호 중복"""
    pass
```

#### Infrastructure Layer

##### Models
```python
# app/infrastructure/persistence/models/advertiser_model.py

class AdvertiserModel(db.Model):
    __tablename__ = 'advertiser'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    business_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    business_phone = db.Column(db.String(20), nullable=False)
    business_number = db.Column(db.String(10), unique=True, nullable=False)
    representative_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

##### Repositories
```python
# app/infrastructure/repositories/advertiser_repository.py

class AdvertiserRepository(IAdvertiserRepository):
    def save(self, advertiser: Advertiser) -> Advertiser:
        """광고주 정보 저장"""
        pass

    def find_by_user_id(self, user_id: str) -> Optional[Advertiser]:
        """사용자 ID로 광고주 조회"""
        pass

    def exists_by_business_number(self, business_number: str) -> bool:
        """사업자등록번호 중복 검증"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/value_objects/test_business_number.py
def test_business_number_with_valid_format():
    # Given: 10자리 숫자
    # When: BusinessNumber 생성
    # Then: 정상 생성
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_advertiser_service.py
def test_register_advertiser_creates_records():
    # Given: 유효한 광고주 정보
    # When: register_advertiser 호출
    # Then: User.role='advertiser', Advertiser 테이블 레코드 생성
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_advertiser_routes.py
def test_register_advertiser_redirects_to_dashboard(client):
    # Given: 로그인된 사용자, 유효한 광고주 정보
    # When: POST /advertiser/register
    # Then: 302 Redirect to /advertiser/dashboard
    pass
```

---

### 3.2 인플루언서 정보 등록

#### 페이지 정보
- **URL**: `/influencer/register`
- **접근 권한**: 로그인 사용자 (역할 미등록)
- **관련 유스케이스**: UC-005 (인플루언서 정보 등록)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/influencer_routes.py

@influencer_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_influencer():
    """
    인플루언서 정보 등록 페이지
    GET: 등록 폼 표시
    POST: 정보 등록 처리
    """
    pass
```

##### Forms
```python
# app/presentation/forms/influencer_forms.py

class InfluencerRegistrationForm(FlaskForm):
    """인플루언서 정보 등록 폼"""
    # 공통 정보
    name = StringField('이름', validators=[
        DataRequired(message='이름을 입력해주세요'),
        Length(min=2, max=100)
    ])
    birth_date = DateField('생년월일', validators=[
        DataRequired(message='생년월일을 입력해주세요')
    ])
    phone_number = StringField('휴대폰번호', validators=[
        DataRequired(message='휴대폰번호를 입력해주세요'),
        Regexp(r'^010-\d{4}-\d{4}$', message='올바른 휴대폰번호 형식을 입력해주세요')
    ])

    # 인플루언서 전용 정보
    channel_name = StringField('SNS 채널명', validators=[
        DataRequired(message='SNS 채널명을 입력해주세요')
    ])
    channel_url = URLField('채널 링크', validators=[
        DataRequired(message='채널 링크를 입력해주세요'),
        URL(message='올바른 URL 형식을 입력해주세요')
    ])
    follower_count = IntegerField('팔로워 수', validators=[
        DataRequired(message='팔로워 수를 입력해주세요'),
        NumberRange(min=0, message='팔로워 수는 0 이상이어야 합니다')
    ])
    submit = SubmitField('등록')
```

##### Schemas
```python
# app/presentation/schemas/influencer_schemas.py

@dataclass
class InfluencerRegistrationRequestDTO:
    """인플루언서 정보 등록 요청 DTO"""
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    channel_name: str
    channel_url: str
    follower_count: int
```

##### Templates
```html
<!-- app/presentation/templates/influencer/register.html -->
- 공통 정보 입력 필드 (이름, 생년월일, 휴대폰번호)
- 인플루언서 전용 정보 입력 필드
- 등록 버튼
```

#### Application Layer

##### Services
```python
# app/application/services/influencer_service.py

class InfluencerService:
    def register_influencer(self, dto: InfluencerRegistrationRequestDTO) -> None:
        """
        인플루언서 정보 등록
        1. 중복 등록 검증
        2. User 테이블 업데이트 (role='influencer')
        3. Influencer 테이블 레코드 생성
        트랜잭션으로 처리
        """
        pass
```

#### Domain Layer

##### Entities
```python
# app/domain/entities/influencer.py

@dataclass
class Influencer:
    """인플루언서 도메인 엔티티"""
    id: Optional[int]
    user_id: str
    name: str
    birth_date: date
    phone_number: str
    channel_name: str
    channel_url: str
    follower_count: int
    created_at: datetime
```

##### Value Objects
```python
# app/domain/value_objects/social_channel.py

@dataclass(frozen=True)
class SocialChannel:
    """SNS 채널 값 객체"""
    name: str
    url: str

    def __post_init__(self):
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError('채널 URL은 http:// 또는 https://로 시작해야 합니다')
```

##### Business Rules
```python
# app/domain/business_rules/influencer_rules.py

class InfluencerRules:
    @staticmethod
    def can_register(user: User) -> bool:
        """인플루언서 등록 가능 여부 검증"""
        return not user.has_role()
```

#### Infrastructure Layer

##### Models
```python
# app/infrastructure/persistence/models/influencer_model.py

class InfluencerModel(db.Model):
    __tablename__ = 'influencer'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    channel_name = db.Column(db.String(100), nullable=False)
    channel_url = db.Column(db.Text, nullable=False)
    follower_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

##### Repositories
```python
# app/infrastructure/repositories/influencer_repository.py

class InfluencerRepository(IInfluencerRepository):
    def save(self, influencer: Influencer) -> Influencer:
        """인플루언서 정보 저장"""
        pass

    def find_by_user_id(self, user_id: str) -> Optional[Influencer]:
        """사용자 ID로 인플루언서 조회"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/value_objects/test_social_channel.py
def test_social_channel_with_valid_url():
    # Given: https:// URL
    # When: SocialChannel 생성
    # Then: 정상 생성
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_influencer_service.py
def test_register_influencer_creates_records():
    # Given: 유효한 인플루언서 정보
    # When: register_influencer 호출
    # Then: User.role='influencer', Influencer 테이블 레코드 생성
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_influencer_routes.py
def test_register_influencer_redirects_to_home(client):
    # Given: 로그인된 사용자, 유효한 인플루언서 정보
    # When: POST /influencer/register
    # Then: 302 Redirect to /
    pass
```

---

## 4. 체험단 관련 페이지 구현 계획

### 4.1 체험단 상세 (Campaign Detail)

#### 페이지 정보
- **URL**: `/campaign/<int:campaign_id>`
- **접근 권한**: 모든 사용자 (비로그인 포함)
- **관련 유스케이스**: UC-006 (체험단 상세 조회)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/campaign_routes.py

@campaign_bp.route('/<int:campaign_id>')
def campaign_detail(campaign_id: int):
    """
    체험단 상세 페이지
    GET: 체험단 정보 및 광고주 정보 표시
    """
    pass
```

##### Schemas
```python
# app/presentation/schemas/campaign_schemas.py

@dataclass
class CampaignDetailDTO:
    """체험단 상세 DTO"""
    id: int
    title: str
    description: str
    image_url: Optional[str]
    quota: int
    application_count: int
    start_date: date
    end_date: date
    benefits: str
    conditions: str
    status: str
    business_name: str
    business_address: str
    can_apply: bool  # 인플루언서가 지원 가능한지 여부
    already_applied: bool  # 이미 지원했는지 여부
```

##### Templates
```html
<!-- app/presentation/templates/campaign/detail.html -->
- 체험단 이미지
- 제목, 설명
- 모집 인원 / 지원자 수
- 모집 기간
- 제공 혜택, 체험 조건
- 광고주 정보 (업체명, 주소)
- 지원하기 버튼 (조건부 표시)
```

#### Application Layer

##### Services
```python
# app/application/services/campaign_service.py

class CampaignService:
    def get_campaign_detail(
        self, campaign_id: int, user_id: Optional[str]
    ) -> CampaignDetailDTO:
        """
        체험단 상세 정보 조회
        user_id가 있으면 지원 가능 여부 및 지원 여부 확인
        """
        pass
```

#### Domain Layer

##### Business Rules
```python
# app/domain/business_rules/campaign_rules.py

class CampaignRules:
    @staticmethod
    def can_apply(
        campaign: Campaign,
        influencer: Optional[Influencer],
        already_applied: bool
    ) -> bool:
        """지원 가능 여부 검증"""
        if not influencer:
            return False
        if not campaign.is_recruiting():
            return False
        if already_applied:
            return False
        return True
```

#### Infrastructure Layer

##### Repositories
```python
# app/infrastructure/repositories/campaign_repository.py

class CampaignRepository(ICampaignRepository):
    def find_by_id(self, campaign_id: int) -> Optional[Campaign]:
        """체험단 ID로 조회"""
        pass

    def get_application_count(self, campaign_id: int) -> int:
        """지원자 수 조회"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/business_rules/test_campaign_rules.py
def test_can_apply_returns_false_when_already_applied():
    # Given: 이미 지원한 인플루언서
    # When: can_apply 호출
    # Then: False 반환
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_campaign_service.py
def test_get_campaign_detail_includes_application_count():
    # Given: 지원자 3명이 있는 체험단
    # When: get_campaign_detail 호출
    # Then: application_count=3
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_campaign_routes.py
def test_campaign_detail_displays_apply_button_for_influencer(client):
    # Given: 인플루언서 로그인, 모집 중인 체험단
    # When: GET /campaign/<id>
    # Then: 200 OK, 지원하기 버튼 표시
    pass
```

---

### 4.2 체험단 지원 (Campaign Application)

#### 페이지 정보
- **URL**: `/campaign/<int:campaign_id>/apply`
- **접근 권한**: 인플루언서 (정보 등록 완료)
- **관련 유스케이스**: UC-007 (체험단 지원)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/campaign_routes.py

@campaign_bp.route('/<int:campaign_id>/apply', methods=['GET', 'POST'])
@login_required
@influencer_required
def apply_campaign(campaign_id: int):
    """
    체험단 지원 페이지
    GET: 지원 폼 표시
    POST: 지원 처리
    """
    pass
```

##### Forms
```python
# app/presentation/forms/campaign_forms.py

class CampaignApplicationForm(FlaskForm):
    """체험단 지원 폼"""
    application_reason = TextAreaField('지원 사유', validators=[
        Length(max=1000, message='지원 사유는 1000자 이하여야 합니다')
    ])
    submit = SubmitField('지원하기')
```

##### Schemas
```python
# app/presentation/schemas/application_schemas.py

@dataclass
class ApplicationCreateRequestDTO:
    """체험단 지원 요청 DTO"""
    campaign_id: int
    influencer_id: int
    application_reason: Optional[str]
```

##### Templates
```html
<!-- app/presentation/templates/campaign/apply.html -->
- 체험단 정보 요약 (제목, 모집 인원)
- 지원 사유 입력 (선택)
- 지원하기 버튼
```

#### Application Layer

##### Services
```python
# app/application/services/application_service.py

class ApplicationService:
    def apply_to_campaign(self, dto: ApplicationCreateRequestDTO) -> None:
        """
        체험단 지원 처리
        1. 인플루언서 정보 등록 여부 검증
        2. 체험단 모집 중 상태 검증
        3. 중복 지원 검증
        4. Application 테이블 레코드 생성
        """
        pass
```

##### Interfaces
```python
# app/application/interfaces/i_application_service.py

class IApplicationService(ABC):
    @abstractmethod
    def apply_to_campaign(self, dto: ApplicationCreateRequestDTO) -> None:
        pass
```

#### Domain Layer

##### Entities
```python
# app/domain/entities/application.py

@dataclass
class Application:
    """체험단 지원 도메인 엔티티"""
    id: Optional[int]
    campaign_id: int
    influencer_id: int
    application_reason: Optional[str]
    status: ApplicationStatus
    applied_at: datetime
```

##### Business Rules
```python
# app/domain/business_rules/application_rules.py

class ApplicationRules:
    @staticmethod
    def can_apply(
        campaign: Campaign,
        influencer: Influencer,
        already_applied: bool
    ) -> Tuple[bool, Optional[str]]:
        """
        지원 가능 여부 검증
        Returns: (가능 여부, 에러 메시지)
        """
        if not campaign.is_recruiting():
            return False, '모집이 종료된 체험단입니다'
        if already_applied:
            return False, '이미 지원한 체험단입니다'
        return True, None
```

##### Exceptions
```python
# app/domain/exceptions/application_exceptions.py

class AlreadyAppliedException(DomainException):
    """중복 지원"""
    pass

class CampaignNotRecruitingException(DomainException):
    """모집 종료된 체험단"""
    pass
```

#### Infrastructure Layer

##### Models
```python
# app/infrastructure/persistence/models/application_model.py

class ApplicationModel(db.Model):
    __tablename__ = 'application'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    application_reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='APPLIED')
    applied_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('campaign_id', 'influencer_id', name='uq_application_campaign_influencer'),
    )
```

##### Repositories
```python
# app/infrastructure/repositories/application_repository.py

class ApplicationRepository(IApplicationRepository):
    def save(self, application: Application) -> Application:
        """지원 정보 저장"""
        pass

    def exists_by_campaign_and_influencer(
        self, campaign_id: int, influencer_id: int
    ) -> bool:
        """중복 지원 검증"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/business_rules/test_application_rules.py
def test_can_apply_returns_false_when_campaign_closed():
    # Given: 모집 종료된 체험단
    # When: can_apply 호출
    # Then: (False, '모집이 종료된 체험단입니다')
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_application_service.py
def test_apply_to_campaign_creates_application():
    # Given: 인플루언서, 모집 중인 체험단
    # When: apply_to_campaign 호출
    # Then: Application 테이블에 레코드 생성
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_campaign_routes.py
def test_apply_campaign_redirects_to_detail(client):
    # Given: 인플루언서 로그인, 모집 중인 체험단
    # When: POST /campaign/<id>/apply
    # Then: 302 Redirect to /campaign/<id>
    pass
```

---

## 5. 광고주 전용 페이지 구현 계획

### 5.1 광고주 대시보드

#### 페이지 정보
- **URL**: `/advertiser/dashboard`
- **접근 권한**: 광고주
- **관련 유스케이스**: UC-008 (광고주 대시보드)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/advertiser_routes.py

@advertiser_bp.route('/dashboard')
@login_required
@advertiser_required
def dashboard():
    """
    광고주 대시보드
    GET: 내 체험단 목록 표시 (모집중, 진행중, 완료)
    """
    pass
```

##### Schemas
```python
# app/presentation/schemas/campaign_schemas.py

@dataclass
class AdvertiserCampaignListItemDTO:
    """광고주 체험단 목록 아이템 DTO"""
    id: int
    title: str
    quota: int
    application_count: int
    end_date: date
    status: str
    created_at: datetime
```

##### Templates
```html
<!-- app/presentation/templates/advertiser/dashboard.html -->
- 체험단 생성 버튼
- 모집 중인 체험단 목록
- 진행 중인 체험단 목록 (Phase 2)
- 완료된 체험단 목록 (Phase 2)
```

#### Application Layer

##### Services
```python
# app/application/services/campaign_service.py

class CampaignService:
    def list_campaigns_by_advertiser(
        self, advertiser_id: int
    ) -> Dict[str, List[AdvertiserCampaignListItemDTO]]:
        """
        광고주의 체험단 목록 조회
        Returns: {'recruiting': [...], 'closed': [...], 'selected': [...]}
        """
        pass

    def create_campaign(self, dto: CampaignCreateRequestDTO) -> Campaign:
        """
        체험단 생성
        1. 광고주 권한 검증
        2. 입력 검증 (모집 기간, 모집 인원)
        3. 이미지 업로드 (Supabase Storage)
        4. Campaign 테이블 레코드 생성
        """
        pass
```

#### Domain Layer

##### Business Rules
```python
# app/domain/business_rules/campaign_rules.py

class CampaignRules:
    @staticmethod
    def validate_campaign_dates(start_date: date, end_date: date) -> bool:
        """모집 기간 검증"""
        today = date.today()
        if start_date < today:
            return False
        if end_date <= start_date:
            return False
        return True
```

#### Infrastructure Layer

##### Repositories
```python
# app/infrastructure/repositories/campaign_repository.py

class CampaignRepository(ICampaignRepository):
    def find_by_advertiser_id(self, advertiser_id: int) -> List[Campaign]:
        """광고주의 체험단 목록 조회"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/business_rules/test_campaign_rules.py
def test_validate_campaign_dates_with_valid_dates():
    # Given: 시작일이 오늘 이후, 종료일이 시작일 이후
    # When: validate_campaign_dates 호출
    # Then: True 반환
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_campaign_service.py
def test_list_campaigns_by_advertiser_groups_by_status():
    # Given: 광고주가 모집중 2개, 종료 1개 체험단 보유
    # When: list_campaigns_by_advertiser 호출
    # Then: {'recruiting': [2개], 'closed': [1개]}
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_advertiser_routes.py
def test_dashboard_displays_campaigns(client):
    # Given: 광고주 로그인, 체험단 3개 보유
    # When: GET /advertiser/dashboard
    # Then: 200 OK, 체험단 3개 표시
    pass
```

---

### 5.2 광고주 체험단 상세

#### 페이지 정보
- **URL**: `/advertiser/campaign/<int:campaign_id>`
- **접근 권한**: 광고주 (본인 체험단만)
- **관련 유스케이스**: UC-009 (광고주 체험단 관리)

#### Presentation Layer

##### Routes
```python
# app/presentation/routes/advertiser_routes.py

@advertiser_bp.route('/campaign/<int:campaign_id>')
@login_required
@advertiser_required
def campaign_detail(campaign_id: int):
    """
    광고주 체험단 상세 페이지
    GET: 체험단 정보 및 지원자 목록 표시
    """
    pass

@advertiser_bp.route('/campaign/<int:campaign_id>/close', methods=['POST'])
@login_required
@advertiser_required
def close_campaign(campaign_id: int):
    """
    체험단 모집 조기종료
    POST: 모집 종료 처리
    """
    pass

@advertiser_bp.route('/campaign/<int:campaign_id>/select', methods=['POST'])
@login_required
@advertiser_required
def select_influencers(campaign_id: int):
    """
    인플루언서 선정
    POST: 선정된 인플루언서 상태 업데이트
    """
    pass
```

##### Schemas
```python
# app/presentation/schemas/application_schemas.py

@dataclass
class ApplicationDetailDTO:
    """지원자 상세 DTO"""
    id: int
    influencer_id: int
    influencer_name: str
    channel_name: str
    channel_url: str
    follower_count: int
    application_reason: Optional[str]
    applied_at: datetime
    status: str
```

##### Templates
```html
<!-- app/presentation/templates/advertiser/campaign_detail.html -->
- 체험단 정보
- 지원자 목록 (이름, SNS 채널, 팔로워 수, 지원 사유)
- 조기종료 버튼 (모집 중일 때)
- 인플루언서 선정 버튼 (모집 종료 후)
```

#### Application Layer

##### Services
```python
# app/application/services/campaign_service.py

class CampaignService:
    def close_campaign_early(self, campaign_id: int, advertiser_id: int) -> None:
        """
        체험단 모집 조기종료
        1. 소유권 검증
        2. 모집 중 상태 검증
        3. Campaign.status='CLOSED' 업데이트
        """
        pass

    def select_influencers(
        self,
        campaign_id: int,
        advertiser_id: int,
        selected_application_ids: List[int]
    ) -> None:
        """
        인플루언서 선정
        1. 소유권 검증
        2. 모집 종료 상태 검증
        3. 선정 인원 검증
        4. Application 상태 업데이트 (SELECTED/REJECTED)
        5. Campaign.status='SELECTED' 업데이트
        트랜잭션으로 처리
        """
        pass
```

#### Domain Layer

##### Business Rules
```python
# app/domain/business_rules/campaign_rules.py

class CampaignRules:
    @staticmethod
    def can_close_early(campaign: Campaign) -> bool:
        """조기종료 가능 여부 검증"""
        return campaign.status == CampaignStatus.RECRUITING

    @staticmethod
    def can_select_influencers(campaign: Campaign) -> bool:
        """인플루언서 선정 가능 여부 검증"""
        return campaign.status == CampaignStatus.CLOSED

    @staticmethod
    def validate_selection_count(campaign: Campaign, selected_count: int) -> bool:
        """선정 인원 검증"""
        return selected_count <= campaign.quota
```

##### Exceptions
```python
# app/domain/exceptions/campaign_exceptions.py

class CampaignNotOwnedException(DomainException):
    """체험단 소유권 없음"""
    pass

class InvalidCampaignStatusException(DomainException):
    """잘못된 체험단 상태"""
    pass

class SelectionQuotaExceededException(DomainException):
    """선정 인원 초과"""
    pass
```

#### Infrastructure Layer

##### Repositories
```python
# app/infrastructure/repositories/application_repository.py

class ApplicationRepository(IApplicationRepository):
    def find_by_campaign_id(self, campaign_id: int) -> List[Application]:
        """체험단의 지원자 목록 조회"""
        pass

    def update_status_bulk(
        self,
        application_ids: List[int],
        status: ApplicationStatus
    ) -> None:
        """지원 상태 일괄 업데이트"""
        pass
```

#### 테스트 전략

##### Unit Tests
```python
# tests/unit/domain/business_rules/test_campaign_rules.py
def test_can_select_influencers_returns_true_when_closed():
    # Given: 모집 종료 상태의 체험단
    # When: can_select_influencers 호출
    # Then: True 반환
    pass
```

##### Integration Tests
```python
# tests/integration/services/test_campaign_service.py
def test_select_influencers_updates_statuses():
    # Given: 모집 종료된 체험단, 지원자 5명
    # When: select_influencers 호출 (3명 선정)
    # Then: 3명 SELECTED, 2명 REJECTED
    pass
```

##### E2E Tests
```python
# tests/e2e/routes/test_advertiser_routes.py
def test_close_campaign_updates_status(client):
    # Given: 광고주 로그인, 모집 중인 체험단
    # When: POST /advertiser/campaign/<id>/close
    # Then: Campaign.status='CLOSED'
    pass
```

---

## 6. 테스트 전략

### 6.1 TDD 프로세스 (Red → Green → Refactor)

모든 구현은 **TDD 프로세스**를 따릅니다:

1. **RED Phase**: 실패하는 테스트 작성
   - 가장 간단한 시나리오부터 시작
   - 테스트가 올바른 이유로 실패하는지 확인

2. **GREEN Phase**: 최소한의 코드로 테스트 통과
   - "Fake it till you make it" 접근
   - YAGNI 원칙 준수

3. **REFACTOR Phase**: 코드 개선
   - 중복 제거
   - 네이밍 개선
   - 구조 단순화
   - 테스트는 계속 통과 상태 유지

### 6.2 테스트 피라미드

```
      /\
     /  \     E2E Tests (10%)
    /____\
   /      \   Integration Tests (20%)
  /________\
 /          \ Unit Tests (70%)
/____________\
```

### 6.3 테스트 품질: FIRST 원칙

- **Fast**: 밀리초 단위, 빠른 실행
- **Independent**: 공유 상태 없음, 독립적 실행
- **Repeatable**: 동일한 결과 보장
- **Self-validating**: Pass/Fail 자동 판정
- **Timely**: 코드 작성 직전에 테스트 작성

### 6.4 테스트 구조: AAA 패턴

```python
def test_example():
    # Arrange: 테스트 데이터 및 의존성 설정
    user = create_test_user()

    # Act: 함수/메서드 실행
    result = service.do_something(user)

    # Assert: 기대 결과 검증
    assert result is not None
    assert result.status == 'success'
```

### 6.5 목(Mock) 전략

#### Unit Tests
- 외부 의존성은 모두 Mock
- 순수 비즈니스 로직만 테스트

#### Integration Tests
- Repository는 실제 DB 사용 (TestDB)
- 외부 서비스는 Mock (Supabase)

#### E2E Tests
- Flask Test Client 사용
- DB는 실제 DB 사용 (TestDB)
- 외부 서비스는 Mock (Supabase)

---

## 7. 구현 우선순위

### Phase 1 (Week 1-2): 인증 및 사용자 관리
1. 회원가입 (Register)
2. 로그인 (Login)
3. 로그아웃 (Logout)
4. 광고주 정보 등록
5. 인플루언서 정보 등록

### Phase 2 (Week 3): 체험단 관리
1. 홈 (Home) - 체험단 탐색
2. 체험단 상세 (Campaign Detail)
3. 광고주 대시보드
4. 체험단 생성 (Advertiser Dashboard 내)

### Phase 3 (Week 4): 체험단 지원 및 선정
1. 체험단 지원 (Campaign Application)
2. 광고주 체험단 상세
3. 모집 조기종료
4. 인플루언서 선정

---

## 8. 참고 문서

- `docs/prd.md`: 제품 요구사항 문서
- `docs/userflow.md`: 사용자 플로우
- `docs/database.md`: 데이터베이스 설계
- `docs/rules/tdd.md`: TDD 프로세스
- `CLAUDE.md`: 아키텍처 가이드

---

**문서 끝**
