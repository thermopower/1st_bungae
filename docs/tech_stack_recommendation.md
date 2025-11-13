# 기술 스택 권장사항

## 선정 기준

1. **AI가 잘 구현할만한, 인기있는 기술**
2. **믿을만한 기업에 의해 활발히 유지보수되고 있는 기술**
3. **Breaking Change가 잦지않은, 하위호환성이 잘 보장되는 기술**

---

## 최종 선정 기술 스택

### 백엔드 프레임워크

#### Flask 3.0+
- **선정 이유**
  - Python 웹 프레임워크 중 가장 많은 학습 데이터 보유
  - Pallets 프로젝트에서 활발히 관리 (10년+ 이력)
  - 메이저 버전 간 안정적인 마이그레이션 경로 제공
  - 경량화되어 있어 확장성이 좋음
- **유지보수 주체**: Pallets (오픈소스 커뮤니티)
- **하위호환성**: 우수 (Flask 2.x → 3.x 마이그레이션 가이드 완비)

#### Flask 확장 라이브러리

**Flask-SQLAlchemy 3.1.1**
- ORM (데이터베이스 추상화)
- SQLAlchemy 기반으로 안정적
- 점진적 업그레이드 지원

**Flask-Migrate 4.0.7**
- Alembic 기반 데이터베이스 마이그레이션
- 버전 관리 및 롤백 지원

**Flask-Login 0.6.3**
- 세션 기반 사용자 인증
- 간단하고 안정적인 인증 시스템

**Flask-CORS 4.0.1**
- Cross-Origin 요청 처리
- SPA 연동 시 필수

**Flask-WTF 1.2.1**
- 폼 검증 및 CSRF 보호
- WTForms 기반으로 안정적

### 데이터베이스

#### PostgreSQL
- **선정 이유**
  - 30년 이상의 역사를 가진 안정적인 RDBMS
  - Supabase의 기본 데이터베이스
  - 오픈소스로 활발히 유지보수
  - 풍부한 기능과 확장성
- **유지보수 주체**: PostgreSQL Global Development Group
- **하위호환성**: 매우 우수

### 백엔드 서비스 (BaaS)

#### Supabase 2.4.2
- **선정 이유**
  - Firebase의 오픈소스 대안
  - PostgreSQL, Auth, Storage, Realtime 통합 제공
  - 명확한 Python SDK 제공
  - VC 투자를 받은 안정적인 스타트업
  - 활발한 커뮤니티 및 문서화
- **유지보수 주체**: Supabase Inc.
- **하위호환성**: 좋음 (API 변경 시 deprecation 기간 제공)
- **주요 기능**
  - **Supabase Auth**: 이메일/소셜 로그인
  - **PostgreSQL Database**: 관리형 데이터베이스
  - **Storage**: 파일 업로드/다운로드
  - **Realtime**: WebSocket 기반 실시간 구독

### 프론트엔드

#### Jinja2
- **선정 이유**
  - Flask 기본 템플릿 엔진
  - 서버 사이드 렌더링 (SSR)
  - Django 템플릿과 유사한 문법
- **유지보수 주체**: Pallets
- **하위호환성**: 매우 우수

#### Bootstrap 5.3.2
- **선정 이유**
  - 가장 많이 사용되는 CSS 프레임워크
  - AI가 가장 잘 생성하는 UI 프레임워크
  - Twitter 출신, 현재 독립적으로 운영
  - 반응형 디자인 기본 제공
  - 풍부한 컴포넌트
- **유지보수 주체**: Bootstrap Core Team (오픈소스)
- **하위호환성**: 좋음 (4 → 5 마이그레이션 가이드 제공)

#### Vanilla JavaScript
- **선정 이유**
  - 프레임워크 의존성 없음
  - 가장 안정적이고 하위호환성 우수
  - 가벼운 인터랙션에 적합
- **대안**: Alpine.js (필요시)

### 보안

#### python-dotenv 1.0.1
- 환경변수 관리
- 개발/프로덕션 환경 분리

#### email-validator 2.1.1
- 이메일 형식 검증

#### WTForms 3.1.2
- 폼 검증 및 보안

### WSGI 서버

#### Gunicorn 22.0.0
- **선정 이유**
  - Python WSGI HTTP 서버 표준
  - 프로덕션 환경에서 검증됨
  - Render, Heroku 등에서 권장
- **유지보수 주체**: Benoît Chesneau 및 커뮤니티
- **하위호환성**: 매우 우수

### 배포 및 인프라

#### Render
- **선정 이유**
  - Heroku의 대안으로 주목받는 플랫폼
  - Flask 애플리케이션 자동 감지
  - GitHub 자동 배포
  - 무료 티어 제공 (월 750시간)
  - PostgreSQL 데이터베이스 포함
  - 간단한 환경변수 관리
- **유지보수 주체**: Render Inc. (Y Combinator 출신)
- **장점**
  - Heroku보다 저렴
  - 설정이 간단함
  - 자동 SSL 인증서
  - 로그 및 모니터링 제공

#### Docker (선택사항)
- 컨테이너화 (향후 확장 시)
- 로컬 개발 환경 일관성

### 유틸리티

#### python-dateutil 2.9.0
- 날짜/시간 처리

#### psycopg2-binary 2.9.9
- PostgreSQL 어댑터

---

## 배포 아키텍처

```
GitHub Repository
    ↓ (Push)
Render Web Service
    ↓ (자동 배포)
Flask Application (Gunicorn)
    ↓ (API 연결)
Supabase
    ├── PostgreSQL Database
    ├── Auth (이메일 인증)
    └── Storage (파일 업로드)
```

---

## 개발 도구 (권장)

### 코드 품질

- **pytest**: 테스트 프레임워크
- **black**: 코드 포매터
- **pylint/flake8**: 린터
- **mypy**: 타입 체커 (선택사항)

### 버전 관리

- **Git**: 소스 관리
- **GitHub**: 원격 저장소 및 CI/CD

---

## 비용 분석

### 무료 티어 범위

**Render (무료)**
- 월 750시간 서비스 실행
- 15분 비활성화 시 sleep 모드
- 커스텀 도메인 지원

**Supabase (무료)**
- 500MB 데이터베이스
- 1GB 파일 스토리지
- 50,000 월간 활성 사용자
- 2GB 데이터 전송

### 유료 전환 시 예상 비용

**Render**
- Starter: $7/month (Sleep 없음)
- Standard: $25/month (고성능)

**Supabase**
- Pro: $25/month (8GB DB, 100GB Storage)

**총 예상 비용**: 약 $10~50/month (트래픽에 따라 변동)

---

## 대안 기술 (고려했으나 선정하지 않은 이유)

### Django
- ❌ Flask보다 무겁고 복잡함
- ❌ 소규모 프로젝트에 과도한 기능

### FastAPI
- ❌ 비동기 학습 곡선
- ❌ Flask보다 생태계가 작음

### Next.js + Vercel
- ❌ 기존 요구사항이 Flask 기반
- ❌ SSR보다 전통적인 MPA 구조가 요구사항에 적합

### AWS/GCP/Azure
- ❌ 설정이 복잡함
- ❌ 비용 관리 어려움
- ❌ 초기 프로젝트에 과도함

---

## 결론

선정된 기술 스택은 다음 기준을 모두 충족합니다:

✅ **AI 구현 용이성**: Flask와 Bootstrap은 가장 많은 학습 데이터 보유
✅ **유지보수성**: 모든 기술이 안정적인 조직/커뮤니티에서 관리
✅ **하위호환성**: Breaking Change가 적고 마이그레이션 경로가 명확
✅ **배포 편의성**: Render + Supabase로 간단한 배포
✅ **비용 효율성**: 무료 티어로 시작 가능

이 스택은 빠른 개발과 안정적인 운영을 동시에 달성할 수 있는 최적의 조합입니다.
