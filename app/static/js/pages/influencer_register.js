/**
 * 인플루언서 정보 등록 페이지 클라이언트 측 로직
 */

document.addEventListener('DOMContentLoaded', function() {
    // 전화번호 자동 포맷팅 (010-XXXX-XXXX)
    const phoneNumberInput = document.getElementById('phoneNumber');
    if (phoneNumberInput) {
        phoneNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // 숫자만 추출
            let formatted = '';

            if (value.length <= 3) {
                formatted = value;
            } else if (value.length <= 7) {
                formatted = value.slice(0, 3) + '-' + value.slice(3);
            } else {
                formatted = value.slice(0, 3) + '-' + value.slice(3, 7) + '-' + value.slice(7, 11);
            }

            e.target.value = formatted;
        });
    }

    // 팔로워 수 숫자만 입력 허용
    const followerCountInput = document.getElementById('followerCount');
    if (followerCountInput) {
        followerCountInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, ''); // 숫자만 허용
        });

        // 팔로워 수 포맷팅 (1,000 형태)
        followerCountInput.addEventListener('blur', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value) {
                e.target.value = parseInt(value).toLocaleString();
            }
        });

        followerCountInput.addEventListener('focus', function(e) {
            e.target.value = e.target.value.replace(/,/g, ''); // 포커스 시 콤마 제거
        });
    }

    // 채널 URL 검증
    const channelUrlInput = document.getElementById('channelUrl');
    if (channelUrlInput) {
        channelUrlInput.addEventListener('blur', function(e) {
            const url = e.target.value.trim();
            if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
                // http:// 또는 https://로 시작하지 않으면 자동으로 https:// 추가
                e.target.value = 'https://' + url;
            }
        });
    }

    // 폼 제출 시 팔로워 수 콤마 제거
    const form = document.getElementById('influencerRegisterForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (followerCountInput) {
                followerCountInput.value = followerCountInput.value.replace(/,/g, '');
            }
        });
    }
});
