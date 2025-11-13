// 커스텀 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 자동으로 사라지는 알림
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
