/**
 * 광고주 정보 등록 페이지 스크립트
 * 전화번호 및 사업자등록번호 자동 포맷팅
 */

document.addEventListener('DOMContentLoaded', function() {
    // 휴대폰번호 자동 포맷팅
    const phoneNumberInput = document.getElementById('phoneNumber');
    if (phoneNumberInput) {
        phoneNumberInput.addEventListener('input', function(e) {
            formatPhoneNumber(e.target);
        });
    }

    // 사업자등록번호 자동 포맷팅
    const businessNumberInput = document.getElementById('businessNumber');
    if (businessNumberInput) {
        businessNumberInput.addEventListener('input', function(e) {
            formatBusinessNumber(e.target);
        });
    }
});

/**
 * 휴대폰번호 자동 포맷팅 (010-XXXX-XXXX)
 * @param {HTMLInputElement} input - 입력 필드
 */
function formatPhoneNumber(input) {
    // 숫자만 추출
    const value = input.value.replace(/\D/g, '');

    let formatted = '';
    if (value.length <= 3) {
        formatted = value;
    } else if (value.length <= 7) {
        formatted = value.slice(0, 3) + '-' + value.slice(3);
    } else {
        formatted = value.slice(0, 3) + '-' + value.slice(3, 7) + '-' + value.slice(7, 11);
    }

    input.value = formatted;
}

/**
 * 사업자등록번호 자동 포맷팅 (XXX-XX-XXXXX)
 * @param {HTMLInputElement} input - 입력 필드
 */
function formatBusinessNumber(input) {
    // 숫자만 추출
    const value = input.value.replace(/\D/g, '');

    let formatted = '';
    if (value.length <= 3) {
        formatted = value;
    } else if (value.length <= 5) {
        formatted = value.slice(0, 3) + '-' + value.slice(3);
    } else {
        formatted = value.slice(0, 3) + '-' + value.slice(3, 5) + '-' + value.slice(5, 10);
    }

    input.value = formatted;
}
