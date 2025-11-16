# UC-011: 지원 내역 조회 페이지 구현 계획

## 문서 정보

| 항목 | 내용 |
|------|------|
| **UC ID** | UC-011 |
| **UC 이름** | 지원 내역 조회 |
| **페이지 경로** | `/influencer/applications` |
| **작성일** | 2025-11-16 |
| **아키텍처** | 4-Tier Layered Architecture |

---

## 1. 개요

### 1.1 기능 설명

인플루언서가 자신이 지원한 체험단 목록을 조회하고, 상태별(전체/지원완료/선정됨/탈락)로 필터링할 수 있는 페이지입니다.

### 1.2 주요 요구사항

- **권한**: 인플루언서 (정보 등록 완료)
- **정렬**: 지원일시 기준 최신순 (DESC)
- **필터**: 상태별 필터링 (전체/지원완료/선정됨/탈락)
- **렌더링**: 서버 사이드 렌더링 (SSR) + 클라이언트 측 필터링

### 1.3 기술 스택

- **Backend**: Flask + Jinja2 (SSR)
- **Frontend**: Bootstrap 5 + Vanilla JS
- **Architecture**: Layered Architecture (Presentation → Application → Domain → Infrastructure)

---

## 2. 계층별 구현 계획

### 2.1 Presentation Layer (프레젠테이션 계층)

#### 2.1.1 Route 추가

**파일**: `app/presentation/routes/influencer_routes.py`

**추가할 엔드포인트**:
```python
@influencer_bp.route('/applications', methods=['GET'])
@login_required
@influencer_required
def applications():
    """
    인플루언서 지원 내역 조회 페이지

    Returns:
        지원 내역 목록 페이지 (applications.html)
    """
```

**구현 로직**:
1. 현재 로그인한 인플루언서 ID 조회
2. ApplicationService를 통해 지원 내역 조회
3. 상태별 개수 계산 (applied, selected, rejected)
4. 템플릿에 데이터 전달

**에러 처리**:
- 인플루언서 정보 미등록: 정보 등록 페이지로 리다이렉트
- DB 조회 실패: 에러 메시지 표시

---

#### 2.1.2 Template 생성

**파일**: `app/presentation/templates/influencer/applications.html`

**레이아웃 구조**:
```html
{% extends "base.html" %}

{% block content %}
<div class="container my-5">
  <!-- 페이지 헤더 -->
  <h1>내 지원 내역</h1>

  <!-- 상태별 필터 버튼 -->
  <div class="filter-buttons mb-4">
    <button class="btn filter-button" data-filter="all">전체 ({{ total_count }})</button>
    <button class="btn filter-button" data-filter="applied">지원완료 ({{ status_counts.applied }})</button>
    <button class="btn filter-button" data-filter="selected">선정됨 ({{ status_counts.selected }})</button>
    <button class="btn filter-button" data-filter="rejected">탈락 ({{ status_counts.rejected }})</button>
  </div>

  <!-- 정렬 버튼 (옵션) -->
  <div class="sort-controls mb-3">
    <button id="sort-button" class="btn btn-outline-secondary">
      <i class="bi bi-sort-down"></i> 최신순
    </button>
  </div>

  <!-- 지원 내역 목록 -->
  <div id="application-list">
    {% if applications %}
      {% for app in applications %}
        <div class="application-card card mb-3" data-status="{{ app.status | lower }}">
          <div class="card-body">
            <h5 class="card-title">{{ app.campaign.title }}</h5>
            <p class="card-text">
              <span class="badge bg-{{ app.status_badge_color }}">{{ app.status_text }}</span>
            </p>
            <p class="text-muted">
              광고주: {{ app.advertiser.business_name }}<br>
              지원일: {{ app.applied_at.strftime('%Y-%m-%d %H:%M') }}
            </p>
            <a href="{{ url_for('campaign.detail', campaign_id=app.campaign.id) }}" class="btn btn-primary">상세보기</a>
          </div>
        </div>
      {% endfor %}
    {% else %}
      <div class="empty-state text-center my-5">
        <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
        <h4 class="mt-3">아직 지원한 체험단이 없습니다</h4>
        <a href="{{ url_for('main.home') }}" class="btn btn-primary mt-3">체험단 탐색하기</a>
      </div>
    {% endif %}
  </div>
</div>

<!-- 데이터 주입 (Vanilla JS에서 사용) -->
<script id="applications-data" type="application/json">
  {{ applications_json | safe }}
</script>

<script src="{{ url_for('static', filename='js/applications.js') }}"></script>
{% endblock %}
```

**UI 요소**:
- 상태별 필터 버튼 (전체/지원완료/선정됨/탈락)
- 지원 내역 카드 (체험단명, 광고주명, 지원일시, 상태 배지)
- 빈 상태 메시지 (지원 내역 없을 때)
- 상세보기 버튼 (체험단 상세 페이지로 이동)

**상태 배지 색상**:
- `APPLIED`: `bg-primary` (파란색)
- `SELECTED`: `bg-success` (초록색)
- `REJECTED`: `bg-secondary` (회색)

---

#### 2.1.3 Static JS 추가

**파일**: `app/presentation/static/js/applications.js`

**기능**:
1. 상태별 필터링 (클라이언트 측)
2. 정렬 순서 변경 (최신순 ↔ 오래된순)
3. 필터 버튼 Active 상태 관리

**구현 코드**:
```javascript
// 상태 관리
const state = {
  applications: [],           // 전체 지원 내역
  filteredApplications: [],   // 필터링된 지원 내역
  statusFilter: 'all',        // 현재 필터 (all, applied, selected, rejected)
  sortOrder: 'desc'           // 정렬 순서 (desc: 최신순, asc: 오래된순)
};

// 초기화
function init() {
  // Jinja2에서 주입된 데이터 파싱
  const dataElement = document.getElementById('applications-data');
  if (dataElement) {
    state.applications = JSON.parse(dataElement.textContent);
  }

  // 초기 필터링/정렬
  updateFilteredApplications();

  // 이벤트 리스너 등록
  registerEventListeners();
}

// 필터링 및 정렬
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

// 렌더링
function render() {
  renderApplicationList();
  renderFilterButtons();
  renderSortButton();
}

// 지원 내역 목록 렌더링
function renderApplicationList() {
  const listContainer = document.getElementById('application-list');

  // 모든 카드 숨기기
  const allCards = document.querySelectorAll('.application-card');
  allCards.forEach(card => card.style.display = 'none');

  // 필터링된 카드만 표시
  state.filteredApplications.forEach(app => {
    const card = document.querySelector(`.application-card[data-id="${app.id}"]`);
    if (card) {
      card.style.display = 'block';
    }
  });

  // 빈 상태 메시지 처리
  const emptyState = document.querySelector('.empty-state');
  if (state.filteredApplications.length === 0) {
    if (emptyState) {
      emptyState.style.display = 'block';
    }
  } else {
    if (emptyState) {
      emptyState.style.display = 'none';
    }
  }
}

// 필터 버튼 렌더링
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

// 정렬 버튼 렌더링
function renderSortButton() {
  const sortButton = document.getElementById('sort-button');
  if (sortButton) {
    const icon = sortButton.querySelector('i');
    if (state.sortOrder === 'desc') {
      icon.className = 'bi bi-sort-down';
      sortButton.innerHTML = '<i class="bi bi-sort-down"></i> 최신순';
    } else {
      icon.className = 'bi bi-sort-up';
      sortButton.innerHTML = '<i class="bi bi-sort-up"></i> 오래된순';
    }
  }
}

// 이벤트 리스너 등록
function registerEventListeners() {
  // 필터 버튼
  document.querySelectorAll('.filter-button').forEach(button => {
    button.addEventListener('click', (e) => {
      state.statusFilter = e.target.dataset.filter;
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

// DOMContentLoaded
document.addEventListener('DOMContentLoaded', init);
```

---

### 2.2 Application Layer (애플리케이션 계층)

#### 2.2.1 Service 메서드 추가

**파일**: `app/application/services/application_service.py`

**추가할 메서드**:
```python
def get_applications_by_influencer(self, influencer_id: int) -> List[Application]:
    """
    인플루언서의 지원 내역 조회

    Args:
        influencer_id: 인플루언서 ID

    Returns:
        Application 엔티티 리스트 (지원일시 기준 최신순)

    Raises:
        InfluencerNotFoundException: 인플루언서가 존재하지 않음
    """
    # 인플루언서 존재 여부 확인
    influencer = self.influencer_repository.find_by_id(influencer_id)
    if influencer is None:
        raise InfluencerNotFoundException("인플루언서 정보를 찾을 수 없습니다")

    # 지원 내역 조회
    applications = self.application_repository.find_by_influencer_id(influencer_id)

    return applications
```

**추가 설명**:
- 인플루언서 존재 여부를 먼저 검증 (비즈니스 규칙)
- Repository를 통해 지원 내역 조회
- 정렬은 Repository에서 처리 (applied_at DESC)

---

### 2.3 Domain Layer (도메인 계층)

#### 2.3.1 Application Entity 확인

**파일**: `app/domain/entities/application.py`

**현재 상태**:
```python
@dataclass
class Application:
    """체험단 지원 도메인 엔티티"""

    id: Optional[int]
    campaign_id: int
    influencer_id: int
    application_reason: Optional[str]
    status: str
    applied_at: datetime

    def is_applied(self) -> bool:
        """지원 완료 상태인지 확인"""
        return self.status == APPLICATION_STATUS_APPLIED

    def is_selected(self) -> bool:
        """선정된 상태인지 확인"""
        return self.status == APPLICATION_STATUS_SELECTED

    def is_rejected(self) -> bool:
        """탈락 상태인지 확인"""
        return self.status == APPLICATION_STATUS_REJECTED
```

**추가 필요 여부**: ❌ 없음 (현재 엔티티로 충분)

---

#### 2.3.2 Business Rules 확인

**파일**: `app/domain/business_rules/application_rules.py`

**현재 상태**: `can_apply()` 메서드만 존재

**추가 필요 여부**: ❌ 없음 (지원 내역 조회는 단순 조회이므로 별도 비즈니스 규칙 불필요)

---

### 2.4 Infrastructure Layer (인프라 계층)

#### 2.4.1 Repository 메서드 추가

**파일**: `app/infrastructure/repositories/application_repository.py`

**추가할 메서드**:
```python
def find_by_influencer_id(self, influencer_id: int) -> List[Application]:
    """
    인플루언서의 지원 내역 조회

    Args:
        influencer_id: 인플루언서 ID

    Returns:
        Application 엔티티 리스트 (지원일시 기준 최신순)
    """
    models = (
        self.session.query(ApplicationModel)
        .filter_by(influencer_id=influencer_id)
        .order_by(ApplicationModel.applied_at.desc())
        .all()
    )
    return [ApplicationMapper.to_entity(model) for model in models]
```

**쿼리 설명**:
- `filter_by(influencer_id=influencer_id)`: 특정 인플루언서의 지원 내역만 조회
- `order_by(ApplicationModel.applied_at.desc())`: 최신순 정렬
- 모든 Application을 리스트로 반환

---

#### 2.4.2 Repository Interface 추가

**파일**: `app/infrastructure/repositories/interfaces/i_application_repository.py`

**추가할 메서드 시그니처**:
```python
from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.application import Application

class IApplicationRepository(ABC):
    # ... 기존 메서드 생략 ...

    @abstractmethod
    def find_by_influencer_id(self, influencer_id: int) -> List[Application]:
        """
        인플루언서의 지원 내역 조회

        Args:
            influencer_id: 인플루언서 ID

        Returns:
            Application 엔티티 리스트
        """
        pass
```

---

#### 2.4.3 Mapper 확인

**파일**: `app/infrastructure/persistence/mappers/application_mapper.py`

**현재 상태**: `to_entity()`, `to_model()` 메서드 존재

**추가 필요 여부**: ❌ 없음 (현재 Mapper로 충분)

---

#### 2.4.4 Model 확인

**파일**: `app/infrastructure/persistence/models/application_model.py`

**현재 상태**: Application 테이블 정의됨

**추가 필요 여부**: ❌ 없음 (현재 모델로 충분)

---

### 2.5 Shared Layer (공통 계층)

#### 2.5.1 Decorator 확인

**파일**: `app/shared/decorators/auth_decorators.py`

**필요한 데코레이터**: `@influencer_required`

**현재 상태**: 이미 존재하는지 확인 필요

**구현 예시** (없을 경우):
```python
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user
from app.infrastructure.repositories.influencer_repository import InfluencerRepository
from app.extensions import db

def influencer_required(f):
    """
    인플루언서 권한 검증 데코레이터

    - 로그인 여부 확인
    - Influencer 테이블에 레코드 존재 여부 확인
    - 미등록 시: 인플루언서 정보 등록 페이지로 리다이렉트
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 로그인 여부는 @login_required에서 검증

        # 인플루언서 정보 등록 여부 확인
        influencer_repo = InfluencerRepository(db.session)
        influencer = influencer_repo.find_by_user_id(current_user.id)

        if influencer is None:
            flash('인플루언서 정보를 먼저 등록해주세요.', 'warning')
            return redirect(url_for('influencer.register_influencer'))

        return f(*args, **kwargs)

    return decorated_function
```

---

## 3. 데이터 흐름

### 3.1 데이터 조회 플로우

```
사용자 요청
  ↓
[Presentation Layer]
  influencer_routes.py: /influencer/applications
  → 현재 인플루언서 ID 조회 (current_user.id → influencer_id)
  ↓
[Application Layer]
  application_service.get_applications_by_influencer(influencer_id)
  → 인플루언서 존재 여부 검증
  ↓
[Infrastructure Layer]
  application_repository.find_by_influencer_id(influencer_id)
  → DB 쿼리: SELECT * FROM application WHERE influencer_id = ? ORDER BY applied_at DESC
  → ApplicationMapper.to_entity(model) 변환
  ↓
[Application Layer]
  → 지원 내역 리스트 반환
  ↓
[Presentation Layer]
  → 상태별 개수 계산 (applied, selected, rejected)
  → 템플릿 렌더링 (applications.html)
  ↓
사용자에게 HTML 반환
```

---

### 3.2 클라이언트 측 필터링 플로우

```
사용자가 "선정됨" 필터 클릭
  ↓
[JavaScript]
  applications.js
  → state.statusFilter = 'selected'
  → updateFilteredApplications()
  → filtered = applications.filter(app => app.status === 'SELECTED')
  → render()
  ↓
DOM 업데이트 (선정된 지원 내역만 표시)
```

---

## 4. DTO 및 데이터 변환

### 4.1 Route → Template 데이터 전달

**Route에서 전달할 데이터**:
```python
{
    'applications': [
        {
            'id': 1,
            'status': 'APPLIED',
            'status_text': '지원완료',
            'status_badge_color': 'primary',
            'applied_at': datetime(2025, 11, 14, 12, 0, 0),
            'campaign': {
                'id': 1,
                'title': '신메뉴 파스타 체험단 모집',
                'end_date': date(2025, 11, 30),
                'status': 'RECRUITING'
            },
            'advertiser': {
                'business_name': '테스트 카페'
            }
        },
        # ...
    ],
    'status_counts': {
        'applied': 3,
        'selected': 1,
        'rejected': 1
    },
    'total_count': 5
}
```

**상태 텍스트 매핑**:
```python
STATUS_TEXT_MAP = {
    'APPLIED': '지원완료',
    'SELECTED': '선정됨',
    'REJECTED': '탈락'
}

STATUS_BADGE_COLOR_MAP = {
    'APPLIED': 'primary',   # 파란색
    'SELECTED': 'success',  # 초록색
    'REJECTED': 'secondary' # 회색
}
```

---

### 4.2 Template → JavaScript 데이터 전달

**Jinja2에서 JSON 주입**:
```html
<script id="applications-data" type="application/json">
  {{ applications_json | safe }}
</script>
```

**applications_json 생성 (Route에서)**:
```python
import json

applications_json = json.dumps([
    {
        'id': app.id,
        'status': app.status,
        'applied_at': app.applied_at.isoformat(),
        'campaign': {
            'id': campaign.id,
            'title': campaign.title
        },
        'advertiser': {
            'business_name': advertiser.business_name
        }
    }
    for app in applications
])
```

---

## 5. 상세 구현 가이드

### 5.1 Route 구현 상세

**파일**: `app/presentation/routes/influencer_routes.py`

```python
@influencer_bp.route('/applications', methods=['GET'])
@login_required
@influencer_required
def applications():
    """
    인플루언서 지원 내역 조회 페이지

    Returns:
        지원 내역 목록 페이지 (applications.html)
    """
    from app.extensions import db
    from app.infrastructure.repositories.application_repository import ApplicationRepository
    from app.infrastructure.repositories.campaign_repository import CampaignRepository
    from app.infrastructure.repositories.influencer_repository import InfluencerRepository
    from app.infrastructure.repositories.advertiser_repository import AdvertiserRepository
    from app.application.services.application_service import ApplicationService
    from app.domain.exceptions.influencer_exceptions import InfluencerNotFoundException
    import json

    try:
        # 1. Repository 및 Service 생성 (DI)
        application_repo = ApplicationRepository(db.session)
        campaign_repo = CampaignRepository(db.session)
        influencer_repo = InfluencerRepository(db.session)

        application_service = ApplicationService(
            application_repo,
            campaign_repo,
            influencer_repo
        )

        # 2. 현재 인플루언서 ID 조회
        influencer = influencer_repo.find_by_user_id(current_user.id)
        if influencer is None:
            flash('인플루언서 정보를 먼저 등록해주세요.', 'warning')
            return redirect(url_for('influencer.register_influencer'))

        # 3. 지원 내역 조회
        applications = application_service.get_applications_by_influencer(influencer.id)

        # 4. 각 지원 내역에 Campaign 및 Advertiser 정보 추가
        advertiser_repo = AdvertiserRepository(db.session)

        enriched_applications = []
        for app in applications:
            campaign = campaign_repo.find_by_id(app.campaign_id)
            if campaign:
                advertiser = advertiser_repo.find_by_id(campaign.advertiser_id)

                enriched_applications.append({
                    'id': app.id,
                    'status': app.status,
                    'status_text': STATUS_TEXT_MAP.get(app.status, app.status),
                    'status_badge_color': STATUS_BADGE_COLOR_MAP.get(app.status, 'secondary'),
                    'applied_at': app.applied_at,
                    'campaign': {
                        'id': campaign.id,
                        'title': campaign.title,
                        'end_date': campaign.end_date,
                        'status': campaign.status
                    },
                    'advertiser': {
                        'business_name': advertiser.business_name if advertiser else '알 수 없음'
                    }
                })

        # 5. 상태별 개수 계산
        status_counts = {
            'applied': sum(1 for app in applications if app.is_applied()),
            'selected': sum(1 for app in applications if app.is_selected()),
            'rejected': sum(1 for app in applications if app.is_rejected())
        }

        # 6. JavaScript용 JSON 생성
        applications_json = json.dumps([
            {
                'id': app['id'],
                'status': app['status'],
                'applied_at': app['applied_at'].isoformat(),
            }
            for app in enriched_applications
        ])

        return render_template(
            'influencer/applications.html',
            applications=enriched_applications,
            status_counts=status_counts,
            total_count=len(applications),
            applications_json=applications_json
        )

    except InfluencerNotFoundException as e:
        flash(str(e), 'danger')
        return redirect(url_for('influencer.register_influencer'))
    except Exception as e:
        flash(f'지원 내역을 불러오는 중 오류가 발생했습니다: {str(e)}', 'danger')
        return redirect(url_for('main.home'))


# 상수 정의
STATUS_TEXT_MAP = {
    'APPLIED': '지원완료',
    'SELECTED': '선정됨',
    'REJECTED': '탈락'
}

STATUS_BADGE_COLOR_MAP = {
    'APPLIED': 'primary',
    'SELECTED': 'success',
    'REJECTED': 'secondary'
}
```

---

### 5.2 Template 구현 상세

**파일**: `app/presentation/templates/influencer/applications.html`

```html
{% extends "base.html" %}

{% block title %}내 지원 내역 - 1st_bungae{% endblock %}

{% block content %}
<div class="container my-5">
  <!-- 페이지 헤더 -->
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h1>내 지원 내역</h1>
    <a href="{{ url_for('main.home') }}" class="btn btn-outline-primary">
      <i class="bi bi-house"></i> 홈으로
    </a>
  </div>

  <!-- 상태별 필터 버튼 -->
  <div class="filter-buttons mb-4">
    <div class="btn-group" role="group" aria-label="상태 필터">
      <button type="button" class="btn btn-outline-primary filter-button active" data-filter="all">
        전체 <span class="badge bg-secondary">{{ total_count }}</span>
      </button>
      <button type="button" class="btn btn-outline-primary filter-button" data-filter="applied">
        지원완료 <span class="badge bg-primary">{{ status_counts.applied }}</span>
      </button>
      <button type="button" class="btn btn-outline-primary filter-button" data-filter="selected">
        선정됨 <span class="badge bg-success">{{ status_counts.selected }}</span>
      </button>
      <button type="button" class="btn btn-outline-primary filter-button" data-filter="rejected">
        탈락 <span class="badge bg-secondary">{{ status_counts.rejected }}</span>
      </button>
    </div>
  </div>

  <!-- 정렬 버튼 -->
  <div class="sort-controls mb-3 d-flex justify-content-end">
    <button id="sort-button" class="btn btn-outline-secondary btn-sm">
      <i class="bi bi-sort-down"></i> 최신순
    </button>
  </div>

  <!-- 지원 내역 목록 -->
  <div id="application-list">
    {% if applications %}
      {% for app in applications %}
        <div class="application-card card mb-3" data-status="{{ app.status | lower }}" data-id="{{ app.id }}">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h5 class="card-title">{{ app.campaign.title }}</h5>
                <p class="card-text mb-2">
                  <span class="badge bg-{{ app.status_badge_color }}">{{ app.status_text }}</span>
                </p>
                <p class="text-muted small mb-0">
                  <i class="bi bi-building"></i> {{ app.advertiser.business_name }}<br>
                  <i class="bi bi-calendar"></i> 지원일: {{ app.applied_at.strftime('%Y-%m-%d %H:%M') }}
                </p>
              </div>
              <div>
                <a href="{{ url_for('campaign.detail', campaign_id=app.campaign.id) }}"
                   class="btn btn-primary btn-sm">
                  상세보기 <i class="bi bi-arrow-right"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      {% endfor %}
    {% else %}
      <div class="empty-state text-center my-5">
        <i class="bi bi-inbox" style="font-size: 3rem; color: #ccc;"></i>
        <h4 class="mt-3">아직 지원한 체험단이 없습니다</h4>
        <p class="text-muted">관심 있는 체험단에 지원해보세요!</p>
        <a href="{{ url_for('main.home') }}" class="btn btn-primary mt-3">
          <i class="bi bi-search"></i> 체험단 탐색하기
        </a>
      </div>
    {% endif %}
  </div>
</div>

<!-- 데이터 주입 (Vanilla JS에서 사용) -->
<script id="applications-data" type="application/json">
  {{ applications_json | safe }}
</script>

<script src="{{ url_for('static', filename='js/applications.js') }}"></script>
{% endblock %}
```

---

### 5.3 JavaScript 구현 상세

**파일**: `app/presentation/static/js/applications.js`

(위에 작성한 JavaScript 코드 참조)

---

## 6. 에러 처리

### 6.1 Route 레벨 에러 처리

| 에러 상황 | 예외 타입 | 처리 방법 |
|----------|----------|----------|
| 인플루언서 정보 미등록 | `InfluencerNotFoundException` | 인플루언서 정보 등록 페이지로 리다이렉트 |
| DB 조회 실패 | `Exception` | 에러 메시지 표시 후 홈으로 리다이렉트 |

---

### 6.2 Service 레벨 에러 처리

| 에러 상황 | 예외 타입 | 발생 조건 |
|----------|----------|----------|
| 인플루언서 미존재 | `InfluencerNotFoundException` | `influencer_repository.find_by_id()` 결과가 None |

---

## 7. 테스트 시나리오

### 7.1 정상 조회 (지원 내역 있음)

**Given**: 인플루언서가 3개 체험단에 지원
**When**: `/influencer/applications` 페이지 접속
**Then**: 3개의 지원 내역이 최신순으로 표시됨

---

### 7.2 지원 내역 없음

**Given**: 지원한 체험단이 없는 인플루언서
**When**: `/influencer/applications` 페이지 접속
**Then**: "아직 지원한 체험단이 없습니다" 메시지 및 "체험단 탐색하기" 버튼 표시

---

### 7.3 상태별 필터 (선정됨만)

**Given**: 지원 내역 5개 (선정 2개, 탈락 3개)
**When**: "선정됨" 필터 클릭
**Then**: 선정된 2개 지원 내역만 표시

---

### 7.4 인플루언서 권한 없음

**Given**: 인플루언서 정보가 등록되지 않은 사용자
**When**: `/influencer/applications` 접근
**Then**: "인플루언서 정보를 먼저 등록해주세요" 메시지, 정보 등록 페이지로 리다이렉트

---

### 7.5 정렬 순서 변경

**Given**: 지원 내역 5개
**When**: 정렬 버튼 클릭
**Then**: 오래된순으로 재정렬됨 (아이콘 변경)

---

## 8. UI/UX 고려사항

### 8.1 반응형 디자인

- **모바일**: 카드 레이아웃 (1열)
- **태블릿**: 카드 레이아웃 (2열)
- **데스크톱**: 카드 레이아웃 (2-3열)

---

### 8.2 접근성 (Accessibility)

- ARIA 속성 추가 (`role`, `aria-label`)
- 키보드 네비게이션 지원 (Tab, Enter)
- 색상 대비 (WCAG AA 준수)

---

### 8.3 로딩 상태

Phase 1에서는 SSR이므로 서버에서 전체 데이터를 렌더링하여 로딩 스피너 불필요.
Phase 2에서 API 기반으로 전환 시 로딩 스피너 추가.

---

## 9. 성능 최적화

### 9.1 DB 쿼리 최적화

- 인덱스 활용: `application.influencer_id`에 인덱스 생성
- 페이지네이션 (Phase 2): 지원 내역이 많을 경우 페이지네이션 추가

---

### 9.2 클라이언트 측 최적화

- 필터링/정렬은 클라이언트에서 처리 (서버 요청 최소화)
- 이벤트 위임 (Event Delegation) 사용

---

## 10. 향후 확장 가능성 (Phase 2)

### 10.1 실시간 업데이트

- Supabase Realtime으로 선정 상태 변경 시 자동 갱신

---

### 10.2 페이지네이션

- 지원 내역이 많을 경우 (100개 이상) 페이지네이션 추가

---

### 10.3 검색 기능

- 체험단 제목으로 검색

---

### 10.4 날짜 범위 필터

- 지원 기간으로 필터링 (예: 최근 1개월)

---

## 11. 파일 체크리스트

### 11.1 수정할 파일

- [x] `app/presentation/routes/influencer_routes.py` - `/applications` 엔드포인트 추가
- [x] `app/application/services/application_service.py` - `get_applications_by_influencer()` 메서드 추가
- [x] `app/infrastructure/repositories/application_repository.py` - `find_by_influencer_id()` 메서드 추가
- [x] `app/infrastructure/repositories/interfaces/i_application_repository.py` - 인터페이스 메서드 추가

---

### 11.2 새로 생성할 파일

- [x] `app/presentation/templates/influencer/applications.html` - 지원 내역 페이지 템플릿
- [x] `app/presentation/static/js/applications.js` - 클라이언트 측 필터링/정렬 로직

---

### 11.3 확인이 필요한 파일

- [ ] `app/shared/decorators/auth_decorators.py` - `@influencer_required` 데코레이터 존재 여부 확인

---

## 12. 구현 순서

### Step 1: Infrastructure Layer
1. `i_application_repository.py`에 `find_by_influencer_id()` 인터페이스 추가
2. `application_repository.py`에 `find_by_influencer_id()` 구현

### Step 2: Application Layer
3. `application_service.py`에 `get_applications_by_influencer()` 메서드 추가

### Step 3: Presentation Layer
4. `influencer_routes.py`에 `/applications` 엔드포인트 추가
5. `applications.html` 템플릿 생성
6. `applications.js` JavaScript 생성

### Step 4: 테스트 및 검증
7. 단위 테스트 작성 (Repository, Service)
8. 통합 테스트 작성 (Route)
9. E2E 테스트 (브라우저)

---

## 13. 참고 문서

- `docs/usecases/11/spec.md`: UC-011 유스케이스 스펙
- `docs/pages/applications/state.md`: 상태관리 설계
- `docs/prd.md`: PRD 문서
- `docs/database.md`: 데이터베이스 스키마
- `CLAUDE.md`: 프로젝트 아키텍처

---

**문서 끝**
