# 체험단 페이지 상태관리 설계
## (체험단 상세 / 체험단 지원)

## 페이지 개요

### 체험단 상세
- **URL**: `/campaign/<campaign_id>`
- **권한**: 모든 사용자 (비로그인 포함)
- **목적**: 체험단 상세 정보 조회

### 체험단 지원
- **URL**: `/campaign/<campaign_id>/apply`
- **권한**: 인플루언서 (정보 등록 완료)
- **목적**: 체험단 지원

---

## 상태관리 필요 여부
✅ **필요** - 지원 폼, 이미지 확대 모달, 공유 기능

---

## 상태(State) 정의

### 1. 체험단 상세 상태
```javascript
const campaignDetailState = {
  // 체험단 정보
  campaign: null,

  // 로딩 상태
  isLoading: false,

  // 에러 상태
  error: null,

  // 이미지 모달 상태
  imageModal: {
    isOpen: false,
    currentImage: null
  },

  // 사용자 권한 상태
  canApply: false,
  hasApplied: false,
  userRole: null // null | 'advertiser' | 'influencer'
}
```

### 2. 지원 폼 상태
```javascript
const applicationFormState = {
  // 폼 데이터
  applicationMessage: '',

  // 유효성 검사
  errors: {
    applicationMessage: null
  },

  // 제출 상태
  isSubmitting: false,
  serverError: null,
  isSuccess: false
}
```

---

## 액션(Actions)

### 1. 체험단 정보 조회
```javascript
async function fetchCampaignDetail(campaignId) {
  campaignDetailState.isLoading = true;
  campaignDetailState.error = null;

  try {
    const response = await fetch(`/api/campaigns/${campaignId}`);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('존재하지 않는 체험단입니다.');
      }
      throw new Error('체험단 정보를 불러오는데 실패했습니다.');
    }

    const data = await response.json();
    campaignDetailState.campaign = data.campaign;
    campaignDetailState.canApply = data.can_apply;
    campaignDetailState.hasApplied = data.has_applied;
    campaignDetailState.userRole = data.user_role;

    renderCampaignDetail();
    renderActionButton();

  } catch (error) {
    campaignDetailState.error = error.message;
    renderError();
  } finally {
    campaignDetailState.isLoading = false;
  }
}
```

### 2. 이미지 모달 열기/닫기
```javascript
function openImageModal(imageUrl) {
  campaignDetailState.imageModal.isOpen = true;
  campaignDetailState.imageModal.currentImage = imageUrl;
  renderImageModal();
}

function closeImageModal() {
  campaignDetailState.imageModal.isOpen = false;
  campaignDetailState.imageModal.currentImage = null;
  renderImageModal();
}
```

### 3. 공유 기능
```javascript
async function shareCampaign() {
  const campaign = campaignDetailState.campaign;
  const shareData = {
    title: campaign.title,
    text: campaign.description.substring(0, 100) + '...',
    url: window.location.href
  };

  try {
    if (navigator.share) {
      // 네이티브 공유 API 사용 (모바일)
      await navigator.share(shareData);
    } else {
      // URL 복사 (데스크톱)
      await navigator.clipboard.writeText(window.location.href);
      showToast('링크가 클립보드에 복사되었습니다.');
    }
  } catch (error) {
    console.error('공유 실패:', error);
  }
}
```

### 4. 북마크 기능 (Phase 2)
```javascript
async function toggleBookmark(campaignId) {
  try {
    const response = await fetch(`/api/campaigns/${campaignId}/bookmark`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    });

    if (!response.ok) throw new Error('북마크 실패');

    const data = await response.json();
    campaignDetailState.campaign.is_bookmarked = data.is_bookmarked;
    renderBookmarkButton();
    showToast(data.is_bookmarked ? '북마크에 추가되었습니다.' : '북마크가 해제되었습니다.');

  } catch (error) {
    showToast('북마크에 실패했습니다.');
  }
}
```

### 5. 지원하기
```javascript
async function submitApplication(campaignId) {
  // 유효성 검사
  if (!validateApplicationForm()) return;

  applicationFormState.isSubmitting = true;
  renderSubmitButton();

  try {
    const response = await fetch(`/api/campaigns/${campaignId}/apply`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({
        application_message: applicationFormState.applicationMessage
      })
    });

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 400) {
        applicationFormState.serverError = data.message || '지원 조건을 확인해주세요.';
      } else if (response.status === 409) {
        applicationFormState.serverError = '이미 지원한 체험단입니다.';
      } else {
        applicationFormState.serverError = '지원에 실패했습니다.';
      }
      renderServerError();
      return;
    }

    // 지원 성공
    applicationFormState.isSuccess = true;
    showSuccessMessage();

    // 체험단 상세 페이지로 리다이렉트
    setTimeout(() => {
      window.location.href = `/campaign/${campaignId}`;
    }, 2000);

  } catch (error) {
    applicationFormState.serverError = '네트워크 오류가 발생했습니다.';
    renderServerError();
  } finally {
    applicationFormState.isSubmitting = false;
    renderSubmitButton();
  }
}

function validateApplicationForm() {
  // 지원 메시지는 선택사항이지만, 입력된 경우 길이 검증
  if (applicationFormState.applicationMessage.length > 500) {
    applicationFormState.errors.applicationMessage = '지원 메시지는 최대 500자까지 입력 가능합니다.';
    renderFieldError('applicationMessage');
    return false;
  }

  return true;
}
```

---

## 렌더링(Rendering)

### 1. 체험단 상세 정보 렌더링
```javascript
function renderCampaignDetail() {
  const campaign = campaignDetailState.campaign;
  if (!campaign) return;

  // D-Day 계산
  const dday = calculateDday(campaign.deadline);

  document.getElementById('campaign-detail').innerHTML = `
    <div class="row">
      <div class="col-md-6">
        <img
          src="${campaign.image_url}"
          class="img-fluid rounded cursor-pointer"
          alt="${campaign.title}"
          onclick="openImageModal('${campaign.image_url}')"
        >
      </div>
      <div class="col-md-6">
        <h1 class="mb-3">${campaign.title}</h1>

        <div class="mb-3">
          <span class="badge bg-primary">모집 중</span>
          <span class="badge bg-secondary">D-${dday}</span>
        </div>

        <div class="mb-3">
          <h5>모집 인원</h5>
          <div class="progress">
            <div
              class="progress-bar"
              role="progressbar"
              style="width: ${(campaign.current_applicants / campaign.quota) * 100}%"
              aria-valuenow="${campaign.current_applicants}"
              aria-valuemin="0"
              aria-valuemax="${campaign.quota}"
            >
              ${campaign.current_applicants}/${campaign.quota}명
            </div>
          </div>
        </div>

        <div class="mb-3">
          <h5>모집 마감일</h5>
          <p>${formatDate(campaign.deadline)}</p>
        </div>

        <div class="mb-3">
          <h5>제공 내역</h5>
          <p>${campaign.offer_details}</p>
        </div>

        <div class="mb-3">
          <h5>리뷰 조건</h5>
          <p>${campaign.review_requirements}</p>
        </div>

        <div class="mb-3">
          <h5>광고주 정보</h5>
          <p>${campaign.advertiser.business_name}</p>
        </div>

        ${renderActionButton()}
      </div>
    </div>

    <div class="row mt-5">
      <div class="col-12">
        <h3>상세 설명</h3>
        <div class="campaign-description">
          ${campaign.description}
        </div>
      </div>
    </div>
  `;
}

function calculateDday(deadline) {
  const today = new Date();
  const deadlineDate = new Date(deadline);
  const diff = deadlineDate - today;
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}
```

### 2. 액션 버튼 렌더링
```javascript
function renderActionButton() {
  const { canApply, hasApplied, userRole } = campaignDetailState;

  if (!userRole) {
    // 비로그인
    return `
      <a href="/auth/login?next=${encodeURIComponent(window.location.pathname)}" class="btn btn-primary w-100">
        로그인하여 지원하기
      </a>
    `;
  }

  if (userRole === 'advertiser') {
    // 광고주는 지원 불가
    return `
      <button class="btn btn-secondary w-100" disabled>
        광고주는 지원할 수 없습니다
      </button>
    `;
  }

  if (hasApplied) {
    // 이미 지원함
    return `
      <button class="btn btn-success w-100" disabled>
        <i class="bi bi-check-circle me-2"></i>
        지원 완료
      </button>
    `;
  }

  if (!canApply) {
    // 지원 불가 (인플루언서 정보 미등록 또는 모집 종료)
    return `
      <a href="/influencer/register" class="btn btn-primary w-100">
        인플루언서 정보 등록 후 지원하기
      </a>
    `;
  }

  // 지원 가능
  return `
    <a href="/campaign/${campaignDetailState.campaign.id}/apply" class="btn btn-primary w-100">
      지원하기
    </a>
  `;
}
```

### 3. 이미지 모달 렌더링
```javascript
function renderImageModal() {
  const modal = document.getElementById('image-modal');
  const { isOpen, currentImage } = campaignDetailState.imageModal;

  if (isOpen) {
    modal.innerHTML = `
      <div class="modal-backdrop fade show" onclick="closeImageModal()"></div>
      <div class="modal fade show d-block" tabindex="-1">
        <div class="modal-dialog modal-lg modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="btn-close" onclick="closeImageModal()"></button>
            </div>
            <div class="modal-body p-0">
              <img src="${currentImage}" class="img-fluid w-100" alt="캠페인 이미지">
            </div>
          </div>
        </div>
      </div>
    `;
    document.body.style.overflow = 'hidden';
  } else {
    modal.innerHTML = '';
    document.body.style.overflow = '';
  }
}
```

### 4. 지원 폼 렌더링
```javascript
function renderApplicationForm() {
  return `
    <form id="application-form" onsubmit="submitApplication(event)">
      <div class="mb-3">
        <label for="applicationMessage" class="form-label">
          지원 메시지 (선택사항)
        </label>
        <textarea
          id="applicationMessage"
          class="form-control"
          rows="5"
          maxlength="500"
          placeholder="지원 동기나 채널 소개를 입력해주세요."
          oninput="updateApplicationMessage(this.value)"
        >${applicationFormState.applicationMessage}</textarea>
        <div class="form-text">
          ${applicationFormState.applicationMessage.length}/500자
        </div>
        <div id="applicationMessage-error" class="invalid-feedback d-none"></div>
      </div>

      <div id="server-error"></div>
      <div id="success-message"></div>

      <button type="submit" id="submit-button" class="btn btn-primary w-100">
        지원하기
      </button>
    </form>
  `;
}

function updateApplicationMessage(value) {
  applicationFormState.applicationMessage = value;
  document.querySelector('.form-text').textContent = `${value.length}/500자`;

  if (applicationFormState.errors.applicationMessage) {
    applicationFormState.errors.applicationMessage = null;
    renderFieldError('applicationMessage');
  }
}
```

---

## 이벤트 핸들러

### 1. 페이지 로드
```javascript
document.addEventListener('DOMContentLoaded', function() {
  const campaignId = getCampaignIdFromUrl();
  fetchCampaignDetail(campaignId);
});

function getCampaignIdFromUrl() {
  const path = window.location.pathname;
  const match = path.match(/\/campaign\/(\d+)/);
  return match ? match[1] : null;
}
```

### 2. 공유 버튼 클릭
```javascript
document.getElementById('share-button')?.addEventListener('click', shareCampaign);
```

### 3. ESC 키로 모달 닫기
```javascript
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && campaignDetailState.imageModal.isOpen) {
    closeImageModal();
  }
});
```

---

## 접근성

### 1. 이미지 확대 키보드 접근
```html
<img
  src="${campaign.image_url}"
  class="img-fluid rounded cursor-pointer"
  alt="${campaign.title}"
  onclick="openImageModal('${campaign.image_url}')"
  onkeypress="if(event.key==='Enter') openImageModal('${campaign.image_url}')"
  tabindex="0"
  role="button"
>
```

### 2. 모달 포커스 트랩
```javascript
function openImageModal(imageUrl) {
  // ... 모달 열기 로직 ...

  // 포커스를 닫기 버튼으로 이동
  setTimeout(() => {
    document.querySelector('.btn-close')?.focus();
  }, 100);
}
```

---

## 성능 최적화

### 1. 이미지 lazy loading
```html
<img src="${campaign.image_url}" loading="lazy" alt="${campaign.title}">
```

### 2. 캐싱
```javascript
const campaignCache = new Map();

async function fetchCampaignDetail(campaignId) {
  if (campaignCache.has(campaignId)) {
    campaignDetailState.campaign = campaignCache.get(campaignId);
    renderCampaignDetail();
    return;
  }

  // ... fetch 로직 ...

  campaignCache.set(campaignId, data.campaign);
}
```

---

## 향후 확장 가능성

### Phase 2 기능
- **북마크**: 관심 체험단 저장
- **공유**: SNS 공유 기능
- **리뷰 갤러리**: 선정된 인플루언서 리뷰 목록
- **Q&A**: 광고주에게 질문하기
- **실시간 지원자 수 업데이트**: WebSocket
