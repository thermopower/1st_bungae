/**
 * 회원가입 페이지 상태관리
 */

// 폼 상태
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
        score: 0,
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
};

/**
 * 입력 필드 변경
 */
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

/**
 * 비밀번호 강도 체크
 */
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

/**
 * 비밀번호 확인 검증
 */
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

/**
 * 클라이언트 측 유효성 검사
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

/**
 * 필드 에러 렌더링
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

function renderErrors() {
    renderFieldError('email');
    renderFieldError('password');
    renderFieldError('passwordConfirm');
}

/**
 * 비밀번호 강도 렌더링
 */
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

/**
 * 서버 에러 렌더링
 */
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

/**
 * 제출 버튼 렌더링
 */
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

/**
 * 성공 메시지 표시
 */
function showSuccessMessage() {
    const container = document.getElementById('success-message');
    container.innerHTML = `
        <div class="alert alert-success" role="alert">
            <i class="bi bi-check-circle me-2"></i>
            회원가입이 완료되었습니다! 잠시 후 로그인 페이지로 이동합니다.
        </div>
    `;
}

/**
 * 이벤트 핸들러 초기화
 */
document.addEventListener('DOMContentLoaded', function() {
    // 이미 로그인된 경우 리다이렉트
    if (isLoggedIn()) {
        window.location.href = '/';
        return;
    }

    // 포커스 설정
    document.getElementById('email').focus();

    // 입력 필드 이벤트 리스너
    document.getElementById('email').addEventListener('input', function(e) {
        updateField('email', e.target.value);
    });

    document.getElementById('password').addEventListener('input', function(e) {
        updateField('password', e.target.value);
    });

    document.getElementById('passwordConfirm').addEventListener('input', function(e) {
        updateField('passwordConfirm', e.target.value);
    });

    // 비밀번호 표시/숨김 토글
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
});

function isLoggedIn() {
    return document.cookie.includes('session=');
}
