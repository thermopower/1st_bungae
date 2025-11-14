# 페이지별 상태관리 설계 문서

## 개요

본 디렉토리는 1st_bungae 체험단 플랫폼의 각 페이지별 클라이언트 측 상태관리 설계 문서를 포함하고 있습니다.

### 프로젝트 특징
- **아키텍처**: Flask SSR (Server-Side Rendering)
- **프론트엔드**: Bootstrap 5 + Vanilla JavaScript
- **상태관리**: 필요한 페이지에만 클라이언트 측 상태관리 적용

---

## 페이지 목록

### 1. 공통 페이지

#### 홈 (Home) - 체험단 탐색
- **경로**: `/docs/pages/home/state.md`
- **URL**: `/`
- **상태관리**: ✅ 필요 (필터링, 검색, 정렬, 페이지네이션)
- **주요 기능**:
  - 체험단 목록 조회
  - 검색 및 필터링
  - 정렬 (최신순, 마감임박순, 인기순)
  - 페이지네이션

#### 로그인 (Login)
- **경로**: `/docs/pages/login/state.md`
- **URL**: `/auth/login`
- **상태관리**: ✅ 필요 (폼 유효성 검사, 에러 처리)
- **주요 기능**:
  - 이메일/비밀번호 입력
  - 클라이언트 측 유효성 검사
  - 에러 메시지 표시
  - 로딩 상태 관리

#### 회원가입 (Register)
- **경로**: `/docs/pages/register/state.md`
- **URL**: `/auth/register`
- **상태관리**: ✅ 필요 (폼 유효성 검사, 비밀번호 강도 체크)
- **주요 기능**:
  - 이메일/비밀번호/비밀번호 확인 입력
  - 비밀번호 강도 실시간 표시
  - 비밀번호 일치 검증
  - 클라이언트 측 유효성 검사

---

### 2. 사용자 정보 등록

#### 광고주/인플루언서 정보 등록
- **경로**: `/docs/pages/user-registration/state.md`
- **URL**:
  - 광고주: `/advertiser/register`
  - 인플루언서: `/influencer/register`
- **상태관리**: ✅ 필요 (복잡한 폼 유효성 검사, 주소 검색, 자동 포맷팅)
- **주요 기능**:
  - 공통 정보 입력 (이름, 생년월일, 휴대폰번호)
  - 광고주: 사업자 정보 입력 (업체명, 주소, 사업자등록번호 등)
  - 인플루언서: SNS 채널 정보 입력 (채널명, URL, 팔로워 수)
  - 전화번호 자동 포맷팅
  - Daum 주소 검색 API 연동 (광고주)

---

### 3. 체험단 관련

#### 체험단 상세 / 체험단 지원
- **경로**: `/docs/pages/campaign/state.md`
- **URL**:
  - 상세: `/campaign/<campaign_id>`
  - 지원: `/campaign/<campaign_id>/apply`
- **상태관리**: ✅ 필요 (모달, 공유 기능, 지원 폼)
- **주요 기능**:
  - 체험단 정보 조회
  - 이미지 확대 모달
  - 공유 기능 (URL 복사 / 네이티브 공유)
  - 지원 메시지 작성 (선택사항)
  - 지원 제출

---

### 4. 광고주 전용

#### 광고주 대시보드 / 광고주 체험단 상세
- **경로**: `/docs/pages/advertiser/state.md`
- **URL**:
  - 대시보드: `/advertiser/dashboard`
  - 체험단 상세: `/advertiser/campaign/<campaign_id>`
- **상태관리**: ✅ 필요 (탭 전환, 지원자 관리, 선정 로직)
- **주요 기능**:
  - 내 체험단 목록 (탭별: 모집 중, 모집 종료, 선정 완료)
  - 지원자 목록 조회 및 정렬
  - 지원자 선택/해제
  - 모집 조기 종료
  - 인플루언서 선정
  - 지원자 프로필 모달

---

## 상태관리 불필요 페이지

다음 페이지들은 SSR로만 처리되며, 클라이언트 측 상태관리가 불필요합니다:

1. **체험단 생성 페이지** (`/advertiser/campaign/create`)
   - WTForms를 통한 서버 측 폼 처리
   - 이미지 업로드는 Supabase Storage 직접 연동

2. **프로필 수정 페이지** (`/advertiser/profile`, `/influencer/profile`)
   - 사용자 정보 등록과 동일한 구조
   - 필요 시 user-registration 설계 참고

---

## 공통 설계 패턴

### 1. 상태(State) 정의
```javascript
const pageState = {
  // 데이터 상태
  data: null,

  // UI 상태
  isLoading: false,
  error: null,

  // 폼 상태 (폼이 있는 경우)
  formData: {},
  errors: {},
  isSubmitting: false
}
```

### 2. 액션(Actions) 구조
- 데이터 조회 (`fetch*`)
- 상태 업데이트 (`update*`)
- 폼 제출 (`submit*`)
- 유효성 검사 (`validate*`)

### 3. 렌더링(Rendering) 구조
- 데이터 렌더링 (`render*`)
- 에러 렌더링 (`renderError`)
- 로딩 렌더링 (`renderLoading`)

### 4. 에러 처리
- 클라이언트 측 유효성 검사 에러
- 서버 응답 에러
- 네트워크 에러

---

## 기술 스택

### 클라이언트 측
- **JavaScript**: Vanilla JavaScript (ES6+)
- **CSS 프레임워크**: Bootstrap 5.3.2
- **아이콘**: Bootstrap Icons

### 외부 라이브러리
- **Daum 우편번호 API**: 주소 검색 (광고주 정보 등록)
- **Web Share API**: 네이티브 공유 (체험단 상세)
- **Clipboard API**: URL 복사

---

## 파일 구조

```
docs/pages/
├── README.md                           # 본 문서
├── home/
│   └── state.md                        # 홈 페이지 상태관리 설계
├── login/
│   └── state.md                        # 로그인 페이지 상태관리 설계
├── register/
│   └── state.md                        # 회원가입 페이지 상태관리 설계
├── user-registration/
│   └── state.md                        # 사용자 정보 등록 상태관리 설계
├── campaign/
│   └── state.md                        # 체험단 상세/지원 상태관리 설계
└── advertiser/
    └── state.md                        # 광고주 대시보드/관리 상태관리 설계
```

---

## 구현 시 참고사항

### 1. CSRF 보호
모든 POST/PUT/DELETE 요청에는 CSRF 토큰을 포함해야 합니다:
```javascript
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
```

### 2. 접근성 (Accessibility)
- ARIA 속성 적절히 사용
- 키보드 네비게이션 지원
- 스크린 리더 지원

### 3. 성능 최적화
- 디바운싱 (검색, 실시간 검증)
- 캐싱 (API 응답)
- Lazy loading (이미지)

### 4. 에러 처리
- 사용자 친화적인 에러 메시지
- 구체적인 액션 제안 (재시도, 다시 로그인 등)

---

## 관련 문서

- [PRD (Product Requirements Document)](/docs/prd.md)
- [사용자 플로우 (User Flow)](/docs/userflow.md)
- [데이터베이스 설계](/docs/database.md)
- [아키텍처 가이드](/CLAUDE.md)

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| 1.0.0 | 2025-11-14 | 초기 상태관리 설계 문서 작성 | Claude |
