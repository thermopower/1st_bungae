# 로그인(Login) 페이지 상태관리 설계

## 페이지 개요
- **URL**: `/auth/login`
- **권한**: 비로그인 사용자만
- **목적**: 사용자 로그인

---

## 상태관리 필요 여부
✅ **필요** - 폼 유효성 검사, 에러 처리, 로딩 상태

---

## 상태(State) 정의

### 1. 폼 상태
```javascript
const formState = {
  // 폼 데이터
  email: '',
  password: '',

  // 유효성 검사 상태
  errors: {
    email: null,
    password: null
  },

  // 폼 제출 상태
  isSubmitting: false,

  // 서버 에러
  serverError: null,

  // 로그인 성공 여부
  isSuccess: false
}
```

---

## 액션(Actions)

### 1. 입력 필드 변경
```javascript
function updateField(field, value) {
  formState[field] = value;

  // 입력 시 해당 필드 에러 제거
  if (formState.errors[field]) {
    formState.errors[field] = null;
    renderFieldError(field);
  }

  // 서버 에러도 제거
  if (formState.serverError) {
    formState.serverError = null;
    renderServerError();
  }
}
```

### 2. 클라이언트 측 유효성 검사
```javascript
function validateForm() {
  let isValid = true;

  // 이메일 검증
  if (!formState.email) {
    formState.errors.email = '이메일을 입력해주세요.';
    isValid = false;
  } else if (!isValidEmail(formState.email)) {
    formState.errors.email = '올바른 이메일 형식이 아닙니다.';
    isValid = false;
  }

  // 비밀번호 검증
  if (!formState.password) {
    formState.errors.password = '비밀번호를 입력해주세요.';
    isValid = false;
  } else if (formState.password.length < 8) {
    formState.errors.password = '비밀번호는 최소 8자 이상이어야 합니다.';
    isValid = false;
  }

  renderErrors();
  return isValid;
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### 3. 폼 제출
```javascript
async function submitForm(e) {
  e.preventDefault();

  // 유효성 검사
  if (!validateForm()) {
    return;
  }

  formState.isSubmitting = true;
  formState.serverError = null;
  renderSubmitButton();

  try {
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({
        email: formState.email,
        password: formState.password
      })
    });

    const data = await response.json();

    if (!response.ok) {
      // 서버 에러 처리
      if (response.status === 401) {
        formState.serverError = '이메일 또는 비밀번호가 일치하지 않습니다.';
      } else if (response.status === 403) {
        formState.serverError = '계정이 정지되었습니다. 관리자에게 문의하세요.';
      } else {
        formState.serverError = data.message || '로그인에 실패했습니다.';
      }
      renderServerError();
      return;
    }

    // 로그인 성공
    formState.isSuccess = true;

    // 리다이렉트 (서버에서 제공한 URL 또는 기본 URL)
    const redirectUrl = data.redirect_url || '/';
    window.location.href = redirectUrl;

  } catch (error) {
    formState.serverError = '네트워크 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
    renderServerError();
  } finally {
    formState.isSubmitting = false;
    renderSubmitButton();
  }
}
```

---

## 렌더링(Rendering)

### 1. 필드 에러 렌더링
```javascript
function renderFieldError(field) {
  const errorElement = document.getElementById(`${field}-error`);
  const inputElement = document.getElementById(field);

  if (formState.errors[field]) {
    errorElement.textContent = formState.errors[field];
    errorElement.classList.remove('d-none');
    inputElement.classList.add('is-invalid');
  } else {
    errorElement.textContent = '';
    errorElement.classList.add('d-none');
    inputElement.classList.remove('is-invalid');
  }
}

function renderErrors() {
  renderFieldError('email');
  renderFieldError('password');
}
```

### 2. 서버 에러 렌더링
```javascript
function renderServerError() {
  const errorElement = document.getElementById('server-error');

  if (formState.serverError) {
    errorElement.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        ${formState.serverError}
        <button type="button" class="btn-close" onclick="dismissServerError()"></button>
      </div>
    `;
  } else {
    errorElement.innerHTML = '';
  }
}

function dismissServerError() {
  formState.serverError = null;
  renderServerError();
}
```

### 3. 제출 버튼 렌더링
```javascript
function renderSubmitButton() {
  const button = document.getElementById('submit-button');

  if (formState.isSubmitting) {
    button.disabled = true;
    button.innerHTML = `
      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
      로그인 중...
    `;
  } else {
    button.disabled = false;
    button.innerHTML = '로그인';
  }
}
```

---

## 이벤트 핸들러

### 1. 폼 제출
```javascript
document.getElementById('login-form').addEventListener('submit', submitForm);
```

### 2. 입력 필드 변경
```javascript
document.getElementById('email').addEventListener('input', function(e) {
  updateField('email', e.target.value);
});

document.getElementById('password').addEventListener('input', function(e) {
  updateField('password', e.target.value);
});
```

### 3. 비밀번호 표시/숨김 토글
```javascript
document.getElementById('toggle-password').addEventListener('click', function() {
  const passwordInput = document.getElementById('password');
  const icon = this.querySelector('i');

  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    icon.classList.remove('bi-eye');
    icon.classList.add('bi-eye-slash');
  } else {
    passwordInput.type = 'password';
    icon.classList.remove('bi-eye-slash');
    icon.classList.add('bi-eye');
  }
});
```

---

## 초기화

### 페이지 로드 시
```javascript
document.addEventListener('DOMContentLoaded', function() {
  // 이미 로그인된 경우 리다이렉트 (서버에서 처리하지만 클라이언트에서도 체크)
  if (isLoggedIn()) {
    window.location.href = '/';
    return;
  }

  // 포커스 설정
  document.getElementById('email').focus();

  // URL 파라미터에서 에러 메시지 확인 (예: 로그인 필요 페이지에서 리다이렉트)
  const params = new URLSearchParams(window.location.search);
  const errorMsg = params.get('error');
  if (errorMsg) {
    formState.serverError = decodeURIComponent(errorMsg);
    renderServerError();
  }
});

function isLoggedIn() {
  // 쿠키 또는 세션 스토리지에서 로그인 상태 확인
  return document.cookie.includes('session=');
}
```

---

## CSRF 토큰 처리

```javascript
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
```

---

## 접근성 (Accessibility)

### 1. ARIA 속성
```html
<form id="login-form" aria-labelledby="login-heading">
  <h1 id="login-heading">로그인</h1>

  <div class="mb-3">
    <label for="email" class="form-label">이메일</label>
    <input
      type="email"
      class="form-control"
      id="email"
      aria-describedby="email-error"
      aria-invalid="false"
      required
    >
    <div id="email-error" class="invalid-feedback d-none" role="alert"></div>
  </div>

  <!-- ... -->
</form>
```

### 2. 에러 알림
```javascript
function renderFieldError(field) {
  const errorElement = document.getElementById(`${field}-error`);
  const inputElement = document.getElementById(field);

  if (formState.errors[field]) {
    errorElement.textContent = formState.errors[field];
    errorElement.classList.remove('d-none');
    inputElement.classList.add('is-invalid');
    inputElement.setAttribute('aria-invalid', 'true');
  } else {
    errorElement.textContent = '';
    errorElement.classList.add('d-none');
    inputElement.classList.remove('is-invalid');
    inputElement.setAttribute('aria-invalid', 'false');
  }
}
```

---

## 보안 고려사항

### 1. CSRF 보호
- 모든 POST 요청에 CSRF 토큰 포함
- Flask-WTF를 통한 CSRF 검증

### 2. 비밀번호 노출 방지
- `type="password"` 사용
- 비밀번호 자동완성 허용 (`autocomplete="current-password"`)

### 3. 에러 메시지
- 구체적인 에러 (이메일 없음, 비밀번호 틀림)를 구분하지 않음
- "이메일 또는 비밀번호가 일치하지 않습니다"로 통일 (보안)

---

## 성능 최적화

### 1. 클라이언트 측 유효성 검사
- 서버 요청 전 클라이언트에서 검증하여 불필요한 요청 방지

### 2. 디바운싱 (선택사항)
- 실시간 이메일 형식 검증 시 디바운싱 적용

---

## 테스트 고려사항

### 1. 단위 테스트
- `validateForm()` 함수 테스트
- `isValidEmail()` 함수 테스트
- 다양한 입력 케이스 (빈 값, 잘못된 형식 등)

### 2. 통합 테스트
- 올바른 로그인 정보로 제출 → 성공 리다이렉트
- 잘못된 로그인 정보로 제출 → 에러 메시지 표시
- 네트워크 에러 시나리오

---

## SSR vs CSR

### SSR (서버 사이드 렌더링)
- **초기 페이지 로드**: 서버에서 로그인 폼 렌더링
- **서버 측 검증**: Flask-WTF로 서버 측 유효성 검사

### CSR (클라이언트 사이드 렌더링)
- **클라이언트 측 검증**: 폼 제출 전 즉시 피드백
- **AJAX 로그인**: 페이지 새로고침 없이 로그인 처리 (선택사항)

---

## 향후 확장 가능성

### Phase 2 기능
- **소셜 로그인**: 카카오, 네이버 OAuth
- **이메일 찾기/비밀번호 재설정**: 별도 플로우
- **2FA (Two-Factor Authentication)**: 추가 보안 단계
- **로그인 기록**: 최근 로그인 기록 표시
