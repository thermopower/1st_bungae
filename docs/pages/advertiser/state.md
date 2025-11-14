# 광고주 페이지 상태관리 설계
## (광고주 대시보드 / 광고주 체험단 상세)

## 페이지 개요

### 광고주 대시보드
- **URL**: `/advertiser/dashboard`
- **권한**: 광고주 (정보 등록 완료)
- **목적**: 내 체험단 목록 조회 및 관리

### 광고주 체험단 상세
- **URL**: `/advertiser/campaign/<campaign_id>`
- **권한**: 광고주 (본인 체험단만)
- **목적**: 체험단 상세 관리, 지원자 목록, 모집 종료, 인플루언서 선정

---

## 상태관리 필요 여부
✅ **필요** - 탭 전환, 필터링, 모달, 지원자 선정 인터랙션

---

## 상태(State) 정의

### 1. 대시보드 상태
```javascript
const dashboardState = {
  // 현재 탭
  activeTab: 'recruiting', // 'recruiting' | 'closed' | 'selected'

  // 체험단 목록
  campaigns: {
    recruiting: [],
    closed: [],
    selected: []
  },

  // 로딩 상태
  isLoading: false,

  // 에러 상태
  error: null,

  // 체험단 생성 모달
  createModal: {
    isOpen: false
  }
}
```

### 2. 체험단 상세 상태
```javascript
const campaignManageState = {
  // 체험단 정보
  campaign: null,

  // 지원자 목록
  applicants: [],

  // 선택된 지원자 ID 목록
  selectedApplicants: [],

  // 정렬 기준
  sortBy: 'applied_at', // 'applied_at' | 'follower_count'

  // 로딩 상태
  isLoading: false,

  // 에러 상태
  error: null,

  // 모달 상태
  modals: {
    closeRecruiting: false,
    selectInfluencers: false,
    viewProfile: {
      isOpen: false,
      applicant: null
    }
  }
}
```

---

## 액션(Actions)

### 대시보드 액션

#### 1. 탭 전환
```javascript
function switchTab(tabName) {
  dashboardState.activeTab = tabName;

  // 해당 탭의 데이터가 없으면 조회
  if (dashboardState.campaigns[tabName].length === 0) {
    fetchCampaigns(tabName);
  }

  renderTabs();
  renderCampaignList();
}
```

#### 2. 체험단 목록 조회
```javascript
async function fetchCampaigns(status = 'recruiting') {
  dashboardState.isLoading = true;
  dashboardState.error = null;

  try {
    const response = await fetch(`/api/advertiser/campaigns?status=${status}`);

    if (!response.ok) {
      throw new Error('체험단 목록을 불러오는데 실패했습니다.');
    }

    const data = await response.json();
    dashboardState.campaigns[status] = data.campaigns;

    renderCampaignList();

  } catch (error) {
    dashboardState.error = error.message;
    renderError();
  } finally {
    dashboardState.isLoading = false;
  }
}
```

#### 3. 체험단 생성 모달 열기/닫기
```javascript
function openCreateModal() {
  dashboardState.createModal.isOpen = true;
  // 실제로는 /advertiser/campaign/create로 리다이렉트하거나
  // 모달에서 폼을 표시
  window.location.href = '/advertiser/campaign/create';
}

function closeCreateModal() {
  dashboardState.createModal.isOpen = false;
  renderCreateModal();
}
```

### 체험단 관리 액션

#### 1. 체험단 및 지원자 조회
```javascript
async function fetchCampaignWithApplicants(campaignId) {
  campaignManageState.isLoading = true;
  campaignManageState.error = null;

  try {
    const response = await fetch(`/api/advertiser/campaigns/${campaignId}`);

    if (!response.ok) {
      if (response.status === 403) {
        throw new Error('접근 권한이 없습니다.');
      } else if (response.status === 404) {
        throw new Error('존재하지 않는 체험단입니다.');
      }
      throw new Error('체험단 정보를 불러오는데 실패했습니다.');
    }

    const data = await response.json();
    campaignManageState.campaign = data.campaign;
    campaignManageState.applicants = data.applicants;

    renderCampaignInfo();
    renderApplicantList();

  } catch (error) {
    campaignManageState.error = error.message;
    renderError();
  } finally {
    campaignManageState.isLoading = false;
  }
}
```

#### 2. 지원자 정렬
```javascript
function sortApplicants(sortBy) {
  campaignManageState.sortBy = sortBy;

  const applicants = [...campaignManageState.applicants];

  applicants.sort((a, b) => {
    if (sortBy === 'applied_at') {
      return new Date(a.applied_at) - new Date(b.applied_at);
    } else if (sortBy === 'follower_count') {
      return b.follower_count - a.follower_count;
    }
    return 0;
  });

  campaignManageState.applicants = applicants;
  renderApplicantList();
}
```

#### 3. 지원자 선택/해제
```javascript
function toggleApplicantSelection(applicantId) {
  const { selectedApplicants } = campaignManageState;
  const index = selectedApplicants.indexOf(applicantId);

  if (index > -1) {
    selectedApplicants.splice(index, 1);
  } else {
    selectedApplicants.push(applicantId);
  }

  renderApplicantList();
  renderSelectButton();
}

function selectAllApplicants() {
  const quota = campaignManageState.campaign.quota;
  const applicantIds = campaignManageState.applicants
    .slice(0, quota)
    .map(a => a.id);

  campaignManageState.selectedApplicants = applicantIds;
  renderApplicantList();
  renderSelectButton();
}

function deselectAllApplicants() {
  campaignManageState.selectedApplicants = [];
  renderApplicantList();
  renderSelectButton();
}
```

#### 4. 모집 조기 종료
```javascript
async function closeRecruitingEarly(campaignId) {
  try {
    const response = await fetch(`/api/advertiser/campaigns/${campaignId}/close`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || '모집 종료에 실패했습니다.');
    }

    // 성공
    showToast('모집이 조기 종료되었습니다.');

    // 상태 업데이트
    campaignManageState.campaign.status = 'closed';
    renderCampaignInfo();
    closeModal('closeRecruiting');

  } catch (error) {
    showToast(error.message, 'error');
  }
}

function showCloseRecruitingModal() {
  campaignManageState.modals.closeRecruiting = true;
  renderCloseRecruitingModal();
}

function confirmCloseRecruiting() {
  const campaignId = campaignManageState.campaign.id;
  closeRecruitingEarly(campaignId);
}
```

#### 5. 인플루언서 선정
```javascript
async function selectInfluencers(campaignId) {
  const { selectedApplicants, campaign } = campaignManageState;

  // 검증
  if (selectedApplicants.length === 0) {
    showToast('선정할 인플루언서를 선택해주세요.', 'warning');
    return;
  }

  if (selectedApplicants.length > campaign.quota) {
    showToast(`모집인원을 초과했습니다. (최대 ${campaign.quota}명)`, 'warning');
    return;
  }

  try {
    const response = await fetch(`/api/advertiser/campaigns/${campaignId}/select`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({
        applicant_ids: selectedApplicants
      })
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || '인플루언서 선정에 실패했습니다.');
    }

    // 성공
    showToast(`${selectedApplicants.length}명의 인플루언서가 선정되었습니다.`);

    // 페이지 새로고침 또는 상태 업데이트
    setTimeout(() => {
      window.location.reload();
    }, 1500);

  } catch (error) {
    showToast(error.message, 'error');
  }
}

function showSelectInfluencersModal() {
  const { selectedApplicants, campaign } = campaignManageState;

  if (selectedApplicants.length === 0) {
    showToast('선정할 인플루언서를 선택해주세요.', 'warning');
    return;
  }

  campaignManageState.modals.selectInfluencers = true;
  renderSelectInfluencersModal();
}

function confirmSelectInfluencers() {
  const campaignId = campaignManageState.campaign.id;
  selectInfluencers(campaignId);
  closeModal('selectInfluencers');
}
```

#### 6. 지원자 프로필 모달
```javascript
function showApplicantProfile(applicantId) {
  const applicant = campaignManageState.applicants.find(a => a.id === applicantId);

  if (!applicant) return;

  campaignManageState.modals.viewProfile.isOpen = true;
  campaignManageState.modals.viewProfile.applicant = applicant;

  renderApplicantProfileModal();
}

function closeApplicantProfile() {
  campaignManageState.modals.viewProfile.isOpen = false;
  campaignManageState.modals.viewProfile.applicant = null;
  renderApplicantProfileModal();
}
```

---

## 렌더링(Rendering)

### 1. 대시보드 탭 렌더링
```javascript
function renderTabs() {
  const tabsContainer = document.getElementById('campaign-tabs');
  const { activeTab, campaigns } = dashboardState;

  tabsContainer.innerHTML = `
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a
          class="nav-link ${activeTab === 'recruiting' ? 'active' : ''}"
          href="#"
          onclick="switchTab('recruiting'); return false;"
        >
          모집 중 <span class="badge bg-primary">${campaigns.recruiting.length}</span>
        </a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link ${activeTab === 'closed' ? 'active' : ''}"
          href="#"
          onclick="switchTab('closed'); return false;"
        >
          모집 종료 <span class="badge bg-secondary">${campaigns.closed.length}</span>
        </a>
      </li>
      <li class="nav-item">
        <a
          class="nav-link ${activeTab === 'selected' ? 'active' : ''}"
          href="#"
          onclick="switchTab('selected'); return false;"
        >
          선정 완료 <span class="badge bg-success">${campaigns.selected.length}</span>
        </a>
      </li>
    </ul>
  `;
}
```

### 2. 체험단 목록 렌더링
```javascript
function renderCampaignList() {
  const container = document.getElementById('campaign-list');
  const { activeTab, campaigns, isLoading } = dashboardState;

  if (isLoading) {
    container.innerHTML = '<div class="text-center"><div class="spinner-border"></div></div>';
    return;
  }

  const list = campaigns[activeTab];

  if (list.length === 0) {
    container.innerHTML = '<div class="alert alert-info">등록된 체험단이 없습니다.</div>';
    return;
  }

  container.innerHTML = list.map(campaign => `
    <div class="card mb-3">
      <div class="card-body">
        <div class="row">
          <div class="col-md-8">
            <h5 class="card-title">${campaign.title}</h5>
            <p class="card-text text-muted">${campaign.description.substring(0, 100)}...</p>
            <div>
              <span class="badge bg-${getStatusBadgeColor(campaign.status)}">${getStatusText(campaign.status)}</span>
              <small class="text-muted ms-2">
                지원자: ${campaign.current_applicants}/${campaign.quota}명
              </small>
              <small class="text-muted ms-2">
                마감일: ${formatDate(campaign.deadline)}
              </small>
            </div>
          </div>
          <div class="col-md-4 text-end">
            <a href="/advertiser/campaign/${campaign.id}" class="btn btn-outline-primary">
              상세 관리
            </a>
          </div>
        </div>
      </div>
    </div>
  `).join('');
}

function getStatusBadgeColor(status) {
  const colors = {
    'recruiting': 'primary',
    'closed': 'secondary',
    'selected': 'success'
  };
  return colors[status] || 'secondary';
}

function getStatusText(status) {
  const texts = {
    'recruiting': '모집 중',
    'closed': '모집 종료',
    'selected': '선정 완료'
  };
  return texts[status] || status;
}
```

### 3. 지원자 목록 렌더링
```javascript
function renderApplicantList() {
  const container = document.getElementById('applicant-list');
  const { applicants, selectedApplicants, campaign } = campaignManageState;

  if (applicants.length === 0) {
    container.innerHTML = '<div class="alert alert-info">아직 지원자가 없습니다.</div>';
    return;
  }

  container.innerHTML = `
    <div class="mb-3">
      <button class="btn btn-sm btn-outline-primary" onclick="selectAllApplicants()">
        전체 선택 (최대 ${campaign.quota}명)
      </button>
      <button class="btn btn-sm btn-outline-secondary ms-2" onclick="deselectAllApplicants()">
        선택 해제
      </button>
    </div>

    <div class="table-responsive">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>
              <input
                type="checkbox"
                ${selectedApplicants.length === applicants.length ? 'checked' : ''}
                onchange="selectedApplicants.length > 0 ? deselectAllApplicants() : selectAllApplicants()"
              >
            </th>
            <th>이름</th>
            <th>
              채널명
              <button class="btn btn-sm btn-link" onclick="sortApplicants('follower_count')">
                <i class="bi bi-sort-down"></i>
              </button>
            </th>
            <th>팔로워 수</th>
            <th>
              지원일
              <button class="btn btn-sm btn-link" onclick="sortApplicants('applied_at')">
                <i class="bi bi-sort-down"></i>
              </button>
            </th>
            <th>액션</th>
          </tr>
        </thead>
        <tbody>
          ${applicants.map(applicant => `
            <tr class="${selectedApplicants.includes(applicant.id) ? 'table-primary' : ''}">
              <td>
                <input
                  type="checkbox"
                  ${selectedApplicants.includes(applicant.id) ? 'checked' : ''}
                  onchange="toggleApplicantSelection(${applicant.id})"
                >
              </td>
              <td>${applicant.name}</td>
              <td>
                <a href="${applicant.channel_url}" target="_blank" rel="noopener">
                  ${applicant.channel_name}
                  <i class="bi bi-box-arrow-up-right ms-1"></i>
                </a>
              </td>
              <td>${applicant.follower_count.toLocaleString()}명</td>
              <td>${formatDateTime(applicant.applied_at)}</td>
              <td>
                <button class="btn btn-sm btn-outline-info" onclick="showApplicantProfile(${applicant.id})">
                  프로필 보기
                </button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}
```

### 4. 모달 렌더링
```javascript
function renderSelectInfluencersModal() {
  const modal = document.getElementById('select-modal');
  const { selectInfluencers } = campaignManageState.modals;
  const { selectedApplicants } = campaignManageState;

  if (!selectInfluencers) {
    modal.innerHTML = '';
    return;
  }

  modal.innerHTML = `
    <div class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">인플루언서 선정 확인</h5>
            <button type="button" class="btn-close" onclick="closeModal('selectInfluencers')"></button>
          </div>
          <div class="modal-body">
            <p>선택한 ${selectedApplicants.length}명의 인플루언서를 선정하시겠습니까?</p>
            <p class="text-muted small">
              선정 후에는 취소할 수 없으며, 선정되지 않은 지원자는 자동으로 탈락 처리됩니다.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" onclick="closeModal('selectInfluencers')">
              취소
            </button>
            <button type="button" class="btn btn-primary" onclick="confirmSelectInfluencers()">
              확인
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show"></div>
  `;
}
```

---

## 접근성 및 사용성

### 1. 키보드 네비게이션
- Tab 키로 지원자 체크박스 순회
- Enter 키로 체크박스 토글
- ESC 키로 모달 닫기

### 2. ARIA 라벨
```html
<button
  onclick="showSelectInfluencersModal()"
  aria-label="선택한 인플루언서 선정하기"
  aria-describedby="selected-count"
>
  선정하기 <span id="selected-count">(${selectedApplicants.length}명 선택)</span>
</button>
```

---

## 향후 확장 가능성

### Phase 2 기능
- **엑셀 다운로드**: 지원자 목록 엑셀 다운로드
- **일괄 메시지 발송**: 선정/탈락 알림
- **통계 대시보드**: 체험단별 성과 분석
- **템플릿 관리**: 자주 사용하는 체험단 템플릿 저장
