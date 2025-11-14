# 홈(Home) 페이지 - 체험단 탐색 상태관리 설계

## 페이지 개요
- **URL**: `/`
- **권한**: 모든 사용자 (비로그인 포함)
- **목적**: 모집 중인 체험단 목록 탐색 및 검색/필터링

---

## 상태관리 필요 여부
✅ **필요** - 클라이언트 측 필터링, 정렬, 검색 기능

---

## 상태(State) 정의

### 1. 필터/검색 상태
```javascript
const filterState = {
  // 검색어
  searchQuery: '',

  // 정렬 기준
  sortBy: 'latest', // 'latest' | 'deadline' | 'popular'

  // 카테고리 필터 (Phase 2)
  category: 'all', // 'all' | 'beauty' | 'food' | 'lifestyle' | ...

  // 현재 페이지
  currentPage: 1,

  // 페이지당 아이템 수
  itemsPerPage: 12
}
```

### 2. 캠페인 목록 상태
```javascript
const campaignListState = {
  // 캠페인 목록
  campaigns: [],

  // 로딩 상태
  isLoading: false,

  // 에러 상태
  error: null,

  // 전체 아이템 수
  totalCount: 0,

  // 전체 페이지 수
  totalPages: 0
}
```

---

## 액션(Actions)

### 1. 검색어 변경
```javascript
function updateSearchQuery(query) {
  filterState.searchQuery = query;
  filterState.currentPage = 1; // 검색 시 첫 페이지로 이동
  fetchCampaigns();
}
```

### 2. 정렬 기준 변경
```javascript
function updateSortBy(sortBy) {
  filterState.sortBy = sortBy;
  filterState.currentPage = 1;
  fetchCampaigns();
}
```

### 3. 페이지 변경
```javascript
function changePage(page) {
  if (page < 1 || page > campaignListState.totalPages) return;
  filterState.currentPage = page;
  fetchCampaigns();
  scrollToTop();
}
```

### 4. 캠페인 목록 조회
```javascript
async function fetchCampaigns() {
  campaignListState.isLoading = true;
  campaignListState.error = null;

  try {
    const params = new URLSearchParams({
      search: filterState.searchQuery,
      sort: filterState.sortBy,
      category: filterState.category,
      page: filterState.currentPage,
      per_page: filterState.itemsPerPage
    });

    const response = await fetch(`/api/campaigns?${params}`);

    if (!response.ok) {
      throw new Error('캠페인 목록을 불러오는데 실패했습니다.');
    }

    const data = await response.json();

    campaignListState.campaigns = data.campaigns;
    campaignListState.totalCount = data.total_count;
    campaignListState.totalPages = data.total_pages;

    renderCampaignList();
    renderPagination();
  } catch (error) {
    campaignListState.error = error.message;
    renderError();
  } finally {
    campaignListState.isLoading = false;
  }
}
```

---

## 렌더링(Rendering)

### 1. 캠페인 목록 렌더링
```javascript
function renderCampaignList() {
  const container = document.getElementById('campaign-list');

  if (campaignListState.isLoading) {
    container.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div></div>';
    return;
  }

  if (campaignListState.error) {
    container.innerHTML = `<div class="alert alert-danger">${campaignListState.error}</div>`;
    return;
  }

  if (campaignListState.campaigns.length === 0) {
    container.innerHTML = '<div class="alert alert-info">검색 결과가 없습니다.</div>';
    return;
  }

  const html = campaignListState.campaigns.map(campaign => `
    <div class="col-md-4 mb-4">
      <div class="card campaign-card">
        <img src="${campaign.image_url}" class="card-img-top" alt="${campaign.title}">
        <div class="card-body">
          <h5 class="card-title">${campaign.title}</h5>
          <p class="card-text">${campaign.description.substring(0, 100)}...</p>
          <div class="d-flex justify-content-between">
            <small>모집: ${campaign.current_applicants}/${campaign.quota}명</small>
            <small class="text-muted">D-${campaign.dday}</small>
          </div>
          <a href="/campaign/${campaign.id}" class="btn btn-primary mt-2">자세히 보기</a>
        </div>
      </div>
    </div>
  `).join('');

  container.innerHTML = html;
}
```

### 2. 페이지네이션 렌더링
```javascript
function renderPagination() {
  const container = document.getElementById('pagination');
  const { currentPage, totalPages } = filterState;

  if (totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  let html = '<nav><ul class="pagination justify-content-center">';

  // 이전 버튼
  html += `
    <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${currentPage - 1}); return false;">이전</a>
    </li>
  `;

  // 페이지 번호
  const startPage = Math.max(1, currentPage - 2);
  const endPage = Math.min(totalPages, currentPage + 2);

  for (let i = startPage; i <= endPage; i++) {
    html += `
      <li class="page-item ${i === currentPage ? 'active' : ''}">
        <a class="page-link" href="#" onclick="changePage(${i}); return false;">${i}</a>
      </li>
    `;
  }

  // 다음 버튼
  html += `
    <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${currentPage + 1}); return false;">다음</a>
    </li>
  `;

  html += '</ul></nav>';
  container.innerHTML = html;
}
```

---

## 이벤트 핸들러

### 1. 검색 폼 제출
```javascript
document.getElementById('search-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const query = document.getElementById('search-input').value.trim();
  updateSearchQuery(query);
});
```

### 2. 정렬 선택
```javascript
document.getElementById('sort-select').addEventListener('change', function(e) {
  updateSortBy(e.target.value);
});
```

### 3. 카테고리 필터 (Phase 2)
```javascript
document.querySelectorAll('.category-filter').forEach(button => {
  button.addEventListener('click', function() {
    filterState.category = this.dataset.category;
    filterState.currentPage = 1;
    fetchCampaigns();
  });
});
```

---

## 초기화

### 페이지 로드 시
```javascript
document.addEventListener('DOMContentLoaded', function() {
  // URL 파라미터에서 초기 상태 복원
  const params = new URLSearchParams(window.location.search);
  filterState.searchQuery = params.get('search') || '';
  filterState.sortBy = params.get('sort') || 'latest';
  filterState.currentPage = parseInt(params.get('page')) || 1;

  // 초기 캠페인 목록 조회
  fetchCampaigns();
});
```

---

## URL 동기화

### 상태 변경 시 URL 업데이트
```javascript
function updateURL() {
  const params = new URLSearchParams();

  if (filterState.searchQuery) {
    params.set('search', filterState.searchQuery);
  }

  if (filterState.sortBy !== 'latest') {
    params.set('sort', filterState.sortBy);
  }

  if (filterState.currentPage > 1) {
    params.set('page', filterState.currentPage);
  }

  const newURL = `${window.location.pathname}${params.toString() ? '?' + params.toString() : ''}`;
  history.pushState(null, '', newURL);
}
```

---

## SSR vs CSR 구분

### SSR (서버 사이드 렌더링)
- **초기 페이지 로드**: 서버에서 첫 페이지 렌더링 (SEO 최적화)
- **첫 페이지 데이터**: Jinja2 템플릿으로 캠페인 목록 렌더링

### CSR (클라이언트 사이드 렌더링)
- **필터/정렬/페이지 변경**: AJAX로 데이터 조회 후 클라이언트에서 렌더링
- **부드러운 UX**: 페이지 새로고침 없이 목록 업데이트

---

## 성능 최적화

### 1. 디바운싱 (Debouncing)
```javascript
let searchTimeout;

function updateSearchQuery(query) {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    filterState.searchQuery = query;
    filterState.currentPage = 1;
    fetchCampaigns();
  }, 300); // 300ms 대기
}
```

### 2. 캐싱
```javascript
const cache = new Map();

async function fetchCampaigns() {
  const cacheKey = JSON.stringify({
    search: filterState.searchQuery,
    sort: filterState.sortBy,
    page: filterState.currentPage
  });

  if (cache.has(cacheKey)) {
    const cachedData = cache.get(cacheKey);
    campaignListState.campaigns = cachedData.campaigns;
    campaignListState.totalCount = cachedData.total_count;
    campaignListState.totalPages = cachedData.total_pages;
    renderCampaignList();
    renderPagination();
    return;
  }

  // ... fetch logic ...

  cache.set(cacheKey, data);
}
```

---

## 에러 처리

### 1. 네트워크 에러
```javascript
catch (error) {
  if (error.name === 'NetworkError') {
    campaignListState.error = '네트워크 연결을 확인해주세요.';
  } else {
    campaignListState.error = error.message;
  }
  renderError();
}
```

### 2. 에러 재시도
```javascript
function renderError() {
  const container = document.getElementById('campaign-list');
  container.innerHTML = `
    <div class="alert alert-danger">
      ${campaignListState.error}
      <button class="btn btn-sm btn-outline-danger ms-2" onclick="fetchCampaigns()">다시 시도</button>
    </div>
  `;
}
```

---

## 접근성 (Accessibility)

### 1. ARIA 속성
```html
<div id="campaign-list" role="region" aria-label="체험단 목록" aria-live="polite">
  <!-- 캠페인 목록 -->
</div>
```

### 2. 로딩 상태 알림
```javascript
function renderCampaignList() {
  if (campaignListState.isLoading) {
    container.innerHTML = `
      <div class="text-center" role="status" aria-live="polite">
        <div class="spinner-border" role="status"></div>
        <span class="visually-hidden">로딩 중...</span>
      </div>
    `;
    return;
  }
  // ...
}
```

---

## 테스트 고려사항

### 1. 단위 테스트
- `updateSearchQuery()` 함수 테스트
- `updateSortBy()` 함수 테스트
- `changePage()` 경계값 테스트

### 2. 통합 테스트
- 검색 후 결과 렌더링 확인
- 정렬 변경 후 목록 순서 확인
- 페이지 변경 후 데이터 로드 확인

---

## 향후 확장 가능성

### Phase 2 기능
- **카테고리 필터**: 다중 카테고리 선택
- **북마크 기능**: 관심 체험단 저장
- **실시간 업데이트**: WebSocket으로 새 체험단 알림
- **무한 스크롤**: 페이지네이션 대신 무한 스크롤 옵션
