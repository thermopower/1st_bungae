/**
 * 로그인 페이지 상태관리 및 이벤트 핸들러
 */

// ===== 상태관리 (State) =====
const formState = {
  email: '',
  password: '',
  errors: {
    email: null,
    password: null
  },
  isSubmitting: false,
  serverError: null,
  isSuccess: false
};

// ===== 유틸리티 함수 =====

/**
 * 이메일 형식 검증
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * CSRF 토큰 가져오기
 * @returns {string}
 */
function getCsrfToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// ===== 액션 (Actions) =====

/**
 * 입력 필드 값 업데이트
 * @param {string} field
 * @param {string} value
 */
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

/**
 * 클라이언트 측 유효성 검사
 * @returns {boolean}
 */
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

// ===== 렌더링 (Rendering) =====

/**
 * 필드 에러 렌더링
 * @param {string} field
 */
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

/**
 * 모든 필드 에러 렌더링
 */
function renderErrors() {
  renderFieldError('email');
  renderFieldError('password');
}

/**
 * 서버 에러 렌더링
 */
function renderServerError() {
  const errorElement = document.getElementById('server-error');

  if (formState.serverError) {
    errorElement.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        ${formState.serverError}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
      </div>
    `;
  } else {
    errorElement.innerHTML = '';
  }
}

/**
 * 제출 버튼 렌더링
 */
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

// ===== 이벤트 핸들러 =====

/**
 * 비밀번호 표시/숨김 토글
 */
function togglePasswordVisibility() {
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
}

// ===== 초기화 =====

/**
 * 페이지 로드 시 초기화
 */
document.addEventListener('DOMContentLoaded', function() {
  // 포커스 설정
  document.getElementById('email').focus();

  // 입력 필드 이벤트 리스너
  document.getElementById('email').addEventListener('input', function(e) {
    updateField('email', e.target.value);
  });

  document.getElementById('password').addEventListener('input', function(e) {
    updateField('password', e.target.value);
  });

  // 비밀번호 표시/숨김 토글
  const toggleButton = document.getElementById('toggle-password');
  if (toggleButton) {
    toggleButton.addEventListener('click', togglePasswordVisibility);
  }

  // URL 파라미터에서 에러 메시지 확인
  const params = new URLSearchParams(window.location.search);
  const errorMsg = params.get('error');
  if (errorMsg) {
    formState.serverError = decodeURIComponent(errorMsg);
    renderServerError();
  }

  // 폼 제출 이벤트
  const form = document.getElementById('login-form');
  form.addEventListener('submit', async function(e) {
    e.preventDefault();

    // 유효성 검사
    if (!validateForm()) {
      announceToScreenReader('입력 내용을 확인해주세요.');
      return;
    }

    // 제출 시작
    formState.isSubmitting = true;
    renderSubmitButton();
    announceToScreenReader('로그인을 진행 중입니다.');

    // 폼 제출 (일반 HTML form submit)
    form.submit();
  });
});

/**
 * 스크린 리더 안내
 */
function announceToScreenReader(message) {
  const srElement = document.getElementById('sr-announcement');
  if (srElement) {
    srElement.textContent = message;
  }
}
