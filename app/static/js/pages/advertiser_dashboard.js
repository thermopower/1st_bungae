/**
 * 광고주 대시보드 JavaScript
 * 탭 전환, 정렬 기능
 */

document.addEventListener('DOMContentLoaded', function() {
    // 탭 전환 이벤트 (Bootstrap 5가 자동 처리하지만, 추가 로직이 필요한 경우)
    const tabs = document.querySelectorAll('#campaignTabs button[data-bs-toggle="tab"]');
    tabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            const targetTab = event.target.getAttribute('data-bs-target');
            console.log(`Tab changed to: ${targetTab}`);

            // 탭 변경 시 추가 로직 (예: 정렬, 필터 초기화)
            // resetFilters(targetTab);
        });
    });

    // 정렬 기능 (추후 확장 가능)
    function setupSorting(tabId) {
        const sortButtons = document.querySelectorAll(`${tabId} .sort-button`);
        sortButtons.forEach(button => {
            button.addEventListener('click', function() {
                const sortBy = this.getAttribute('data-sort');
                sortCampaigns(tabId, sortBy);
            });
        });
    }

    function sortCampaigns(tabId, sortBy) {
        const cards = Array.from(document.querySelectorAll(`${tabId} .campaign-card`));
        const container = document.querySelector(`${tabId} .row`);

        if (!container) return;

        // 정렬 로직 (예: 마감일순, 지원자수순 등)
        cards.sort((a, b) => {
            if (sortBy === 'deadline') {
                // 마감일순 정렬
                const dateA = a.querySelector('.deadline-date')?.textContent || '';
                const dateB = b.querySelector('.deadline-date')?.textContent || '';
                return dateA.localeCompare(dateB);
            } else if (sortBy === 'applicants') {
                // 지원자수순 정렬
                const countA = parseInt(a.querySelector('.applicant-count')?.textContent || '0');
                const countB = parseInt(b.querySelector('.applicant-count')?.textContent || '0');
                return countB - countA;
            }
            return 0;
        });

        // DOM 재배치
        container.innerHTML = '';
        cards.forEach(card => {
            container.appendChild(card.parentElement); // col-md-4 유지
        });
    }

    // 초기화
    setupSorting('#recruiting');
    setupSorting('#closed');
    setupSorting('#selected');
});
