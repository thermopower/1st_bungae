# 배포 가이드 (Render)

## 사전 준비

### 1. GitHub 저장소 설정
현재 프로젝트를 GitHub에 푸시해야 합니다.

```bash
# 원격 저장소가 없다면 추가
git remote add origin https://github.com/your-username/1st_bungae.git

# 최신 코드 푸시
git push -u origin main
```

### 2. Supabase 설정
Supabase Dashboard에서 다음 정보를 확인하세요:

1. **Database URL** (Session Pooler)
   - Dashboard > Settings > Database > Connection Pooling
   - Mode: **Session** 선택 (Port: 5432)
   - 형식: `postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres`

2. **Supabase URL**
   - Dashboard > Settings > API
   - Project URL

3. **Supabase Keys**
   - Dashboard > Settings > API
   - `anon` `public` key
   - `service_role` `secret` key

---

## Render 배포 단계

### 1. Render 계정 생성
https://render.com 에서 계정을 만드세요 (GitHub 계정으로 가입 권장).

### 2. 새 Web Service 생성

1. Render Dashboard에서 **"New +"** 버튼 클릭
2. **"Web Service"** 선택
3. GitHub 저장소 연결
   - "Connect a repository" 클릭
   - GitHub 계정 연동
   - `1st_bungae` 저장소 선택

### 3. 서비스 설정

#### 기본 설정
- **Name**: `bungae-platform` (또는 원하는 이름)
- **Region**: `Singapore` (한국과 가까운 지역)
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt && python manage.py upgrade
  ```
- **Start Command**:
  ```bash
  gunicorn app:app
  ```

#### 환경 변수 설정
"Environment" 탭에서 다음 환경 변수들을 추가하세요:

| Key | Value | 설명 |
|-----|-------|------|
| `PYTHON_VERSION` | `3.11.0` | Python 버전 |
| `FLASK_APP` | `app.py` | Flask 앱 엔트리포인트 |
| `FLASK_ENV` | `production` | 프로덕션 환경 |
| `SECRET_KEY` | (자동 생성) | Flask secret key |
| `DATABASE_URL` | `postgresql://postgres...` | Supabase Session Pooler URL |
| `SUPABASE_URL` | `https://xxx.supabase.co` | Supabase 프로젝트 URL |
| `SUPABASE_KEY` | `eyJ...` | Supabase anon public key |
| `SUPABASE_SERVICE_KEY` | `eyJ...` | Supabase service role key |

**중요**: `SECRET_KEY`는 "Generate" 버튼을 눌러 자동 생성하세요.

### 4. 배포 시작

"Create Web Service" 버튼을 클릭하면 자동으로 배포가 시작됩니다.

배포 과정:
1. ✅ GitHub에서 코드 가져오기
2. ✅ `pip install -r requirements.txt` 실행
3. ✅ `python manage.py upgrade` (마이그레이션 적용)
4. ✅ `gunicorn app:app` (서버 시작)

---

## 배포 후 확인

### 1. 서비스 상태 확인
- Render Dashboard에서 "Live" 상태 확인
- Logs에서 에러가 없는지 확인

### 2. 웹사이트 접속
- Render가 제공하는 URL로 접속 (예: `https://bungae-platform.onrender.com`)
- 모든 페이지가 정상 작동하는지 확인

### 3. 데이터베이스 확인
- Supabase Dashboard에서 테이블이 제대로 생성되었는지 확인

---

## 업데이트 배포

코드를 수정한 후:

```bash
# 1. 커밋
git add .
git commit -m "feat: 새로운 기능 추가"

# 2. GitHub에 푸시
git push origin main
```

Render는 자동으로 새 코드를 감지하고 재배포합니다!

---

## 문제 해결

### 배포 실패 시

1. **Logs 확인**
   - Render Dashboard > Logs 탭
   - 에러 메시지 확인

2. **환경 변수 확인**
   - 모든 환경 변수가 올바르게 설정되었는지 확인
   - `DATABASE_URL`이 Session Pooler URL인지 확인

3. **마이그레이션 문제**
   ```bash
   # 로컬에서 마이그레이션 테스트
   python manage.py upgrade
   ```

### 데이터베이스 연결 실패

1. Supabase Session Pooler URL이 맞는지 확인
2. Supabase에서 IPv4 Add-on 필요 여부 확인
3. 방화벽 설정 확인

---

## 참고 링크

- [Render Documentation](https://render.com/docs)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Supabase Database Connection](https://supabase.com/docs/guides/database/connecting-to-postgres)

---

## 추가 최적화 (선택사항)

### 1. 커스텀 도메인 설정
- Render Dashboard > Settings > Custom Domain

### 2. HTTPS 자동 적용
- Render는 자동으로 Let's Encrypt SSL 인증서 제공

### 3. 자동 배포 비활성화
- Settings > Auto-Deploy 끄기 (수동 배포 원할 때)

### 4. 환경별 설정
- `.env.production` 파일 추가 (프로덕션 전용 설정)
