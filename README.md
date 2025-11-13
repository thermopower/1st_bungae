# 번개 체험단 플랫폼

체험단 매칭 플랫폼 - 광고주와 인플루언서를 연결하는 서비스

## 기술 스택

### 백엔드
- **Flask 3.0+**: Python 웹 프레임워크
- **Flask-SQLAlchemy**: ORM
- **Flask-Login**: 사용자 인증
- **Supabase**: 백엔드 서비스 (Auth, Database)
- **PostgreSQL**: 데이터베이스

### 프론트엔드
- **Jinja2**: 템플릿 엔진
- **Bootstrap 5**: UI 프레임워크
- **Vanilla JavaScript**: 클라이언트 로직

### 배포
- **Render**: 애플리케이션 호스팅
- **Gunicorn**: WSGI HTTP 서버

## 프로젝트 구조

```
1st_bungae/
├── app/
│   ├── models/          # 데이터베이스 모델
│   ├── routes/          # 라우트 (컨트롤러)
│   ├── templates/       # Jinja2 템플릿
│   ├── static/          # 정적 파일 (CSS, JS)
│   ├── utils/           # 유틸리티 함수
│   ├── config.py        # 설정
│   └── extensions.py    # Flask 확장
├── docs/                # 문서
├── supabase/            # Supabase 마이그레이션
├── app.py               # 애플리케이션 진입점
├── requirements.txt     # Python 의존성
├── render.yaml          # Render 배포 설정
└── .env.example         # 환경변수 예시

```

## 로컬 개발 환경 설정

### 1. 저장소 클론

```bash
git clone <repository-url>
cd 1st_bungae
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. 환경변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 값을 입력합니다.

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

### 5. 데이터베이스 초기화

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. 애플리케이션 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## Render 배포

### 1. Supabase 프로젝트 생성

1. [Supabase](https://supabase.com)에서 새 프로젝트 생성
2. Project Settings > API에서 다음 정보 확인:
   - Project URL (SUPABASE_URL)
   - anon public key (SUPABASE_KEY)
   - service_role key (SUPABASE_SERVICE_KEY)

### 2. Render에 배포

1. [Render](https://render.com)에서 새 Web Service 생성
2. GitHub 저장소 연결
3. 다음 설정 입력:
   - **Name**: bungae-platform
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. 환경변수 추가:
   - `SUPABASE_URL`: Supabase Project URL
   - `SUPABASE_KEY`: Supabase anon key
   - `SUPABASE_SERVICE_KEY`: Supabase service role key
   - `SECRET_KEY`: (Render가 자동 생성)

5. **Create Web Service** 클릭

## 주요 기능

- ✅ 회원가입 / 로그인 (Supabase Auth)
- ✅ 광고주 / 인플루언서 프로필 등록
- ✅ 체험단 캠페인 탐색
- ✅ 체험단 지원
- ✅ 광고주 대시보드
- ✅ 캠페인 관리 (조기 종료, 인플루언서 선정)

## 개발 상태

현재 기본 구조가 완성되었으며, 다음 작업이 필요합니다:

- [ ] Supabase Auth 연동 완료
- [ ] 폼 검증 추가
- [ ] 추가 템플릿 작성
- [ ] 테스트 코드 작성
- [ ] 배포 및 테스트

## 라이선스

MIT License
