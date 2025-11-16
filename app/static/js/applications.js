/**
 * 인플루언서 지원 내역 조회 페이지 JavaScript
 * 클라이언트 측 필터링 및 정렬 기능
 */

// 상태 관리
const state = {
  applications: [],           // 전체 지원 내역
  filteredApplications: [],   // 필터링된 지원 내역
  statusFilter: 'all',        // 현재 필터 (all, applied, selected, rejected)
  sortOrder: 'desc'           // 정렬 순서 (desc: 최신순, asc: 오래된순)
};

/**
 * 초기화 함수
 */
function init() {
  // Jinja2에서 주입된 데이터 파싱
  const dataElement = document.getElementById('applications-data');
  if (dataElement) {
    try {
      state.applications = JSON.parse(dataElement.textContent);
    } catch (error) {
      console.error('데이터 파싱 오류:', error);
      state.applications = [];
    }
  }

  // 초기 필터링/정렬
  updateFilteredApplications();

  // 이벤트 리스너 등록
  registerEventListeners();
}

/**
 * 필터링 및 정렬 업데이트
 */
function updateFilteredApplications() {
  let filtered = state.applications;

  // 1. 상태 필터링
  if (state.statusFilter !== 'all') {
    const targetStatus = state.statusFilter.toUpperCase();
    filtered = filtered.filter(app => app.status === targetStatus);
  }

  // 2. 정렬 (applied_at 기준)
  const sorted = [...filtered].sort((a, b) => {
    const dateA = new Date(a.applied_at);
    const dateB = new Date(b.applied_at);
    return state.sortOrder === 'desc' ? dateB - dateA : dateA - dateB;
  });

  state.filteredApplications = sorted;
  render();
}

/**
 * 렌더링
 */
function render() {
  renderApplicationList();
  renderFilterButtons();
  renderSortButton();
}

/**
 * 지원 내역 목록 렌더링
 */
function renderApplicationList() {
  const allCards = document.querySelectorAll('.application-card');
  const emptyState = document.getElementById('empty-state');

  // 필터링된 ID 목록 생성
  const filteredIds = new Set(state.filteredApplications.map(app => app.id));

  // 모든 카드 순회하며 표시/숨김 처리
  allCards.forEach(card => {
    const cardId = parseInt(card.dataset.id);
    if (filteredIds.has(cardId)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });

  // 빈 상태 메시지 처리
  if (emptyState) {
    if (state.filteredApplications.length === 0 && allCards.length > 0) {
      // 필터링 결과가 없지만 전체 데이터는 있는 경우
      emptyState.style.display = 'block';
      emptyState.innerHTML = `
        <i class="bi bi-inbox"></i>
        <h4 class="mt-3">해당 상태의 지원 내역이 없습니다</h4>
        <p class="text-muted">다른 필터를 선택해보세요</p>
      `;
    } else if (state.filteredApplications.length === 0 && allCards.length === 0) {
      // 전체 데이터가 없는 경우 (원래 빈 상태)
      emptyState.style.display = 'block';
    } else {
      emptyState.style.display = 'none';
    }
  }
}

/**
 * 필터 버튼 렌더링
 */
function renderFilterButtons() {
  const buttons = document.querySelectorAll('.filter-button');
  buttons.forEach(button => {
    const filter = button.dataset.filter;
    if (filter === state.statusFilter) {
      button.classList.add('btn-primary');
      button.classList.remove('btn-outline-primary');
    } else {
      button.classList.remove('btn-primary');
      button.classList.add('btn-outline-primary');
    }
  });
}

/**
 * 정렬 버튼 렌더링
 */
function renderSortButton() {
  const sortButton = document.getElementById('sort-button');
  if (sortButton) {
    if (state.sortOrder === 'desc') {
      sortButton.innerHTML = '<i class="bi bi-sort-down"></i> 최신순';
    } else {
      sortButton.innerHTML = '<i class="bi bi-sort-up"></i> 오래된순';
    }
  }
}

/**
 * 이벤트 리스너 등록
 */
function registerEventListeners() {
  // 필터 버튼
  document.querySelectorAll('.filter-button').forEach(button => {
    button.addEventListener('click', (e) => {
      const clickedButton = e.currentTarget;
      state.statusFilter = clickedButton.dataset.filter;
      updateFilteredApplications();
    });
  });

  // 정렬 버튼
  const sortButton = document.getElementById('sort-button');
  if (sortButton) {
    sortButton.addEventListener('click', () => {
      state.sortOrder = state.sortOrder === 'desc' ? 'asc' : 'desc';
      updateFilteredApplications();
    });
  }
}

/**
 * DOMContentLoaded 이벤트
 */
document.addEventListener('DOMContentLoaded', init);
