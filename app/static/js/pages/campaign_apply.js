/**
 * 체험단 지원 페이지 JavaScript
 * campaign/apply.html에서 사용
 */

document.addEventListener('DOMContentLoaded', function() {
    // 폼 요소
    const applyForm = document.querySelector('form');
    const submitButton = document.querySelector('button[type="submit"]');
    const applicationReasonTextarea = document.querySelector('#application_reason');

    // 폼 제출 처리
    if (applyForm) {
        applyForm.addEventListener('submit', function(e) {
            // 제출 버튼 비활성화 (중복 제출 방지)
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 지원 중...';
            }

            // 지원 사유 공백 제거
            if (applicationReasonTextarea && applicationReasonTextarea.value) {
                applicationReasonTextarea.value = applicationReasonTextarea.value.trim();
            }

            // 폼 검증은 Flask-WTF에서 처리하므로 여기서는 생략
        });
    }

    // 글자 수 카운터 (선택)
    if (applicationReasonTextarea) {
        const maxLength = 1000;
        const counterDiv = document.createElement('div');
        counterDiv.className = 'form-text text-end';
        counterDiv.innerHTML = `<span id="char-count">0</span> / ${maxLength}자`;
        applicationReasonTextarea.parentNode.appendChild(counterDiv);

        const charCountSpan = document.getElementById('char-count');

        applicationReasonTextarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            charCountSpan.textContent = currentLength;

            // 최대 길이 초과 시 경고 색상
            if (currentLength > maxLength) {
                charCountSpan.classList.add('text-danger');
                charCountSpan.classList.remove('text-muted');
            } else {
                charCountSpan.classList.add('text-muted');
                charCountSpan.classList.remove('text-danger');
            }
        });
    }

    // 확인 다이얼로그 (선택)
    if (applyForm) {
        const originalSubmit = applyForm.onsubmit;
        applyForm.onsubmit = function(e) {
            e.preventDefault();

            if (confirm('정말 이 체험단에 지원하시겠습니까?\n\n지원 후 취소할 수 없습니다.')) {
                if (originalSubmit) {
                    originalSubmit.call(applyForm, e);
                } else {
                    applyForm.submit();
                }
            } else {
                // 취소 시 버튼 다시 활성화
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = '지원하기';
                }
            }
            return false;
        };
    }
});
