# 회원가입(Register) 페이지 상태관리 설계

## 페이지 개요
- **URL**: `/auth/register`
- **권한**: 비로그인 사용자만
- **목적**: 신규 사용자 회원가입

---

## 상태관리 필요 여부
✅ **필요** - 폼 유효성 검사, 비밀번호 확인, 에러 처리, 로딩 상태

---

## 상태(State) 정의

### 1. 폼 상태
```javascript
const formState = {
  // 폼 데이터
  email: '',
  password: '',
  passwordConfirm: '',

  // 유효성 검사 상태
  errors: {
    email: null,
    password: null,
    passwordConfirm: null
  },

  // 비밀번호 강도
  passwordStrength: {
    score: 0, // 0-4
    message: '',
    hasMinLength: false,
    hasNumber: false,
    hasLetter: false
  },

  // 폼 제출 상태
  isSubmitting: false,

  // 서버 에러
  serverError: null,

  // 회원가입 성공 여부
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

  // 비밀번호 강도 체크
  if (field === 'password') {
    checkPasswordStrength(value);
  }

  // 비밀번호 확인 실시간 검증
  if (field === 'passwordConfirm' || field === 'password') {
    validatePasswordConfirm();
  }

  // 서버 에러 제거
  if (formState.serverError) {
    formState.serverError = null;
    renderServerError();
  }
}
```

### 2. 비밀번호 강도 체크
```javascript
function checkPasswordStrength(password) {
  const state = formState.passwordStrength;

  // 최소 길이
  state.hasMinLength = password.length >= 8;

  // 숫자 포함
  state.hasNumber = /\d/.test(password);

  // 문자 포함
  state.hasLetter = /[a-zA-Z]/.test(password);

  // 점수 계산
  let score = 0;
  if (state.hasMinLength) score++;
  if (state.hasNumber) score++;
  if (state.hasLetter) score++;
  if (password.length >= 12) score++;

  state.score = score;

  // 메시지
  if (score === 0 || password.length === 0) {
    state.message = '';
  } else if (score === 1) {
    state.message = '약함';
  } else if (score === 2) {
    state.message = '보통';
  } else if (score === 3) {
    state.message = '강함';
  } else {
    state.message = '매우 강함';
  }

  renderPasswordStrength();
}
```

### 3. 비밀번호 확인 검증
```javascript
function validatePasswordConfirm() {
  if (!formState.passwordConfirm) {
    formState.errors.passwordConfirm = null;
    renderFieldError('passwordConfirm');
    return;
  }

  if (formState.password !== formState.passwordConfirm) {
    formState.errors.passwordConfirm = '비밀번호가 일치하지 않습니다.';
  } else {
    formState.errors.passwordConfirm = null;
  }

  renderFieldError('passwordConfirm');
}
```

### 4. 클라이언트 측 유효성 검사
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
  } else if (!formState.passwordStrength.hasNumber || !formState.passwordStrength.hasLetter) {
    formState.errors.password = '비밀번호는 영문과 숫자를 포함해야 합니다.';
    isValid = false;
  }

  // 비밀번호 확인 검증
  if (!formState.passwordConfirm) {
    formState.errors.passwordConfirm = '비밀번호 확인을 입력해주세요.';
    isValid = false;
  } else if (formState.password !== formState.passwordConfirm) {
    formState.errors.passwordConfirm = '비밀번호가 일치하지 않습니다.';
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

### 5. 폼 제출
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
    const response = await fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({
        email: formState.email,
        password: formState.password,
        password_confirm: formState.passwordConfirm
      })
    });

    const data = await response.json();

    if (!response.ok) {
      // 서버 에러 처리
      if (response.status === 409) {
        formState.errors.email = '이미 사용 중인 이메일입니다.';
        renderFieldError('email');
      } else {
        formState.serverError = data.message || '회원가입에 실패했습니다.';
        renderServerError();
      }
      return;
    }

    // 회원가입 성공
    formState.isSuccess = true;

    // 성공 메시지 표시
    showSuccessMessage();

    // 역할 선택 페이지로 리다이렉트 (2초 후)
    setTimeout(() => {
      const redirectUrl = data.redirect_url || '/role-selection';
      window.location.href = redirectUrl;
    }, 2000);

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
    inputElement.setAttribute('aria-invalid', 'true');
  } else {
    errorElement.textContent = '';
    errorElement.classList.add('d-none');
    inputElement.classList.remove('is-invalid');
    inputElement.setAttribute('aria-invalid', 'false');
  }
}

function renderErrors() {
  renderFieldError('email');
  renderFieldError('password');
  renderFieldError('passwordConfirm');
}
```

### 2. 비밀번호 강도 렌더링
```javascript
function renderPasswordStrength() {
  const container = document.getElementById('password-strength');
  const state = formState.passwordStrength;

  if (!formState.password) {
    container.innerHTML = '';
    return;
  }

  const colors = ['', 'danger', 'warning', 'success', 'success'];
  const color = colors[state.score];

  container.innerHTML = `
    <div class="mt-2">
      <div class="progress" style="height: 5px;">
        <div
          class="progress-bar bg-${color}"
          role="progressbar"
          style="width: ${state.score * 25}%"
          aria-valuenow="${state.score * 25}"
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
      <small class="text-${color}">${state.message}</small>
      <div class="mt-1">
        <small class="${state.hasMinLength ? 'text-success' : 'text-muted'}">
          ${state.hasMinLength ? '✓' : '○'} 최소 8자 이상
        </small><br>
        <small class="${state.hasNumber ? 'text-success' : 'text-muted'}">
          ${state.hasNumber ? '✓' : '○'} 숫자 포함
        </small><br>
        <small class="${state.hasLetter ? 'text-success' : 'text-muted'}">
          ${state.hasLetter ? '✓' : '○'} 영문 포함
        </small>
      </div>
    </div>
  `;
}
```

### 3. 서버 에러 렌더링
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

### 4. 제출 버튼 렌더링
```javascript
function renderSubmitButton() {
  const button = document.getElementById('submit-button');

  if (formState.isSubmitting) {
    button.disabled = true;
    button.innerHTML = `
      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
      회원가입 중...
    `;
  } else {
    button.disabled = false;
    button.innerHTML = '회원가입';
  }
}
```

### 5. 성공 메시지 표시
```javascript
function showSuccessMessage() {
  const container = document.getElementById('success-message');
  container.innerHTML = `
    <div class="alert alert-success" role="alert">
      <i class="bi bi-check-circle me-2"></i>
      회원가입이 완료되었습니다! 잠시 후 역할 선택 페이지로 이동합니다.
    </div>
  `;
}
```

---

## 이벤트 핸들러

### 1. 폼 제출
```javascript
document.getElementById('register-form').addEventListener('submit', submitForm);
```

### 2. 입력 필드 변경
```javascript
document.getElementById('email').addEventListener('input', function(e) {
  updateField('email', e.target.value);
});

document.getElementById('password').addEventListener('input', function(e) {
  updateField('password', e.target.value);
});

document.getElementById('passwordConfirm').addEventListener('input', function(e) {
  updateField('passwordConfirm', e.target.value);
});
```

### 3. 비밀번호 표시/숨김 토글
```javascript
document.querySelectorAll('.toggle-password').forEach(toggle => {
  toggle.addEventListener('click', function() {
    const targetId = this.dataset.target;
    const passwordInput = document.getElementById(targetId);
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
});
```

---

## 초기화

### 페이지 로드 시
```javascript
document.addEventListener('DOMContentLoaded', function() {
  // 이미 로그인된 경우 리다이렉트
  if (isLoggedIn()) {
    window.location.href = '/';
    return;
  }

  // 포커스 설정
  document.getElementById('email').focus();
});

function isLoggedIn() {
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
<form id="register-form" aria-labelledby="register-heading">
  <h1 id="register-heading">회원가입</h1>

  <div class="mb-3">
    <label for="password" class="form-label">비밀번호</label>
    <input
      type="password"
      class="form-control"
      id="password"
      aria-describedby="password-error password-strength"
      aria-invalid="false"
      required
    >
    <div id="password-error" class="invalid-feedback d-none" role="alert"></div>
    <div id="password-strength" aria-live="polite"></div>
  </div>

  <!-- ... -->
</form>
```

### 2. 비밀번호 강도 실시간 알림
```javascript
function renderPasswordStrength() {
  // ... 렌더링 로직 ...

  // 스크린 리더를 위한 알림
  if (state.score >= 3) {
    announceToScreenReader('비밀번호 강도가 충분합니다.');
  }
}

function announceToScreenReader(message) {
  const announcement = document.getElementById('sr-announcement');
  announcement.textContent = message;
  setTimeout(() => {
    announcement.textContent = '';
  }, 1000);
}
```

---

## 보안 고려사항

### 1. CSRF 보호
- 모든 POST 요청에 CSRF 토큰 포함

### 2. 비밀번호 강도 검증
- 클라이언트 측: 실시간 피드백
- 서버 측: 최종 검증

### 3. 이메일 중복 체크
- 클라이언트 측: 실시간 체크 (선택사항, Phase 2)
- 서버 측: 최종 검증 (필수)

---

## 성능 최적화

### 1. 디바운싱
```javascript
let emailCheckTimeout;

async function checkEmailAvailability(email) {
  clearTimeout(emailCheckTimeout);

  emailCheckTimeout = setTimeout(async () => {
    if (!isValidEmail(email)) return;

    try {
      const response = await fetch(`/api/check-email?email=${encodeURIComponent(email)}`);
      const data = await response.json();

      if (!data.available) {
        formState.errors.email = '이미 사용 중인 이메일입니다.';
        renderFieldError('email');
      }
    } catch (error) {
      // 에러 무시 (최종 검증은 서버에서)
    }
  }, 500);
}
```

---

## 테스트 고려사항

### 1. 단위 테스트
- `validateForm()` 함수 테스트
- `checkPasswordStrength()` 함수 테스트
- 다양한 비밀번호 케이스 (짧은 비밀번호, 숫자 없음, 문자 없음 등)

### 2. 통합 테스트
- 올바른 정보로 회원가입 → 성공 리다이렉트
- 중복 이메일로 회원가입 → 에러 메시지
- 비밀번호 불일치 → 에러 메시지

---

## 향후 확장 가능성

### Phase 2 기능
- **이메일 인증**: 회원가입 후 이메일 인증 링크 발송
- **약관 동의**: 서비스 이용약관, 개인정보 처리방침 동의
- **소셜 회원가입**: 카카오, 네이버 OAuth
- **실시간 이메일 중복 체크**: 디바운싱을 활용한 실시간 검증
