# 라우트 트랜잭션 처리 통합 테스트 계획

## 1. 개요

### 1.1 테스트 목적
광고주 및 인플루언서 라우트에서 데이터베이스 트랜잭션 처리 로직이 정상적으로 동작하는지 검증합니다.

### 1.2 수정된 기능
- `advertiser_routes.py` - `create_campaign()`: 체험단 생성 트랜잭션 처리
- `advertiser_routes.py` - `register_advertiser()`: 광고주 정보 등록 트랜잭션 처리
- `influencer_routes.py` - `register_influencer()`: 인플루언서 정보 등록 트랜잭션 처리

### 1.3 테스트 유형
**통합 테스트 (Integration Test)**
- Flask Test Client 사용
- 실제 데이터베이스 세션 사용 (SQLite in-memory)
- 라우트 → 서비스 → 리포지토리 전체 플로우 검증

### 1.4 테스트 범위
- HTTP 요청/응답 검증
- 데이터베이스 커밋/롤백 검증
- Flash 메시지 검증
- 폼 검증 에러 처리

---

## 2. 테스트 환경 구성

### 2.1 테스트 픽스처

#### 2.1.1 공통 픽스처
```python
# tests/conftest.py 활용
@pytest.fixture(scope='function')
def app():
    """Flask 앱 픽스처 (함수 범위)"""
    # SQLite in-memory DB 사용
    # 각 테스트마다 DB 초기화

@pytest.fixture
def client(app):
    """Flask 테스트 클라이언트"""
    return app.test_client()
```

#### 2.1.2 테스트용 사용자 픽스처
```python
@pytest.fixture
def advertiser_user(app):
    """광고주 사용자 픽스처 (정보 미등록)"""
    with app.app_context():
        user = UserModel(
            id='advertiser-id',
            email='advertiser@example.com',
            role='advertiser'
        )
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

@pytest.fixture
def influencer_user(app):
    """인플루언서 사용자 픽스처 (정보 미등록)"""
    with app.app_context():
        user = UserModel(
            id='influencer-id',
            email='influencer@example.com',
            role='influencer'
        )
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()

@pytest.fixture
def registered_advertiser(app):
    """광고주 정보 등록된 사용자 픽스처"""
    with app.app_context():
        user = UserModel(
            id='registered-advertiser-id',
            email='registered_advertiser@example.com',
            role='advertiser'
        )
        db.session.add(user)
        db.session.flush()

        advertiser = AdvertiserModel(
            id=1,
            user_id=user.id,
            name='홍길동',
            birth_date=date(1990, 1, 1),
            phone_number='010-1234-5678',
            business_name='테스트 카페',
            address='서울시 강남구',
            business_phone='02-1234-5678',
            business_number='1234567890',
            representative_name='홍길동'
        )
        db.session.add(advertiser)
        db.session.commit()
        yield user
        db.session.delete(advertiser)
        db.session.delete(user)
        db.session.commit()
```

### 2.2 헬퍼 함수
```python
def login_user(client, user_id):
    """테스트용 로그인 헬퍼"""
    with client.session_transaction() as sess:
        sess['user_id'] = user_id

def count_records(model):
    """DB 레코드 개수 조회"""
    return db.session.query(model).count()

def get_flash_messages(response):
    """Flash 메시지 추출"""
    with client.session_transaction() as sess:
        return sess.get('_flashes', [])
```

---

## 3. 테스트 케이스

### 3.1 광고주 정보 등록 (`register_advertiser`)

#### TC-RA-001: 정상 케이스 - 광고주 정보 등록 성공
**목적**: 광고주 정보가 정상적으로 DB에 저장되고 커밋되는지 검증

**Given**:
- 광고주 역할의 미등록 사용자가 로그인
- 유효한 광고주 정보 폼 데이터

**When**:
```python
POST /advertiser/register
form_data = {
    'name': '홍길동',
    'birth_date': '1990-01-01',
    'phone_number': '010-1234-5678',
    'business_name': '테스트 카페',
    'address': '서울시 강남구 테헤란로 123',
    'business_phone': '02-1234-5678',
    'business_number': '123-45-67890',
    'representative_name': '홍길동'
}
```

**Then**:
- HTTP 302 Redirect → `/advertiser/dashboard`
- Flash 메시지: "광고주 정보가 성공적으로 등록되었습니다!" (success)
- `AdvertiserModel` 레코드 1개 추가
- DB에서 조회 시 정보 일치 확인

**AAA 패턴**:
```python
def test_register_advertiser_success(client, app, advertiser_user):
    """정상 케이스: 광고주 정보 등록 성공 및 DB 커밋 검증"""
    with app.app_context():
        # Arrange
        login_user(client, advertiser_user.id)
        form_data = {
            'name': '홍길동',
            'birth_date': '1990-01-01',
            'phone_number': '010-1234-5678',
            'business_name': '테스트 카페',
            'address': '서울시 강남구 테헤란로 123',
            'business_phone': '02-1234-5678',
            'business_number': '123-45-67890',
            'representative_name': '홍길동'
        }

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(AdvertiserModel)
        assert before_count == 0

        # Act
        response = client.post(
            '/advertiser/register',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 302
        assert response.location == url_for('advertiser.dashboard')

        # Assert - DB 저장 확인
        after_count = count_records(AdvertiserModel)
        assert after_count == 1

        # Assert - 저장된 데이터 검증
        advertiser = db.session.query(AdvertiserModel).filter_by(
            user_id=advertiser_user.id
        ).first()
        assert advertiser is not None
        assert advertiser.name == '홍길동'
        assert advertiser.business_number == '1234567890'  # 하이픈 제거됨

        # Assert - Flash 메시지
        with client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert len(flashes) == 1
            assert flashes[0][0] == 'success'
            assert '성공적으로 등록되었습니다' in flashes[0][1]
```

---

#### TC-RA-002: 예외 케이스 - 중복 등록 시 롤백
**목적**: 이미 등록된 사용자가 재등록 시도 시 롤백 및 에러 메시지 표시

**Given**:
- 이미 광고주 정보가 등록된 사용자

**When**:
```python
POST /advertiser/register (재등록 시도)
```

**Then**:
- HTTP 200 (폼 재표시)
- Flash 메시지: "이미 광고주 정보가 등록되어 있습니다." (danger)
- DB 레코드 개수 변화 없음 (롤백 확인)

**AAA 패턴**:
```python
def test_register_advertiser_duplicate_rollback(client, app, registered_advertiser):
    """예외 케이스: 중복 등록 시 롤백 검증"""
    with app.app_context():
        # Arrange
        login_user(client, registered_advertiser.id)
        form_data = {
            'name': '김철수',
            'birth_date': '1985-05-05',
            'phone_number': '010-9999-8888',
            'business_name': '새로운 카페',
            'address': '부산시',
            'business_phone': '051-1111-2222',
            'business_number': '999-88-77777',
            'representative_name': '김철수'
        }

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(AdvertiserModel)
        assert before_count == 1

        # Act
        response = client.post(
            '/advertiser/register',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 200  # 폼 재표시

        # Assert - DB 롤백 확인 (레코드 개수 변화 없음)
        after_count = count_records(AdvertiserModel)
        assert after_count == 1

        # Assert - 기존 데이터 유지 확인
        advertiser = db.session.query(AdvertiserModel).filter_by(
            user_id=registered_advertiser.id
        ).first()
        assert advertiser.name == '홍길동'  # 기존 이름 유지

        # Assert - Flash 메시지
        html = response.data.decode('utf-8')
        assert '이미 광고주 정보가 등록되어 있습니다' in html or \
               'AdvertiserAlreadyRegisteredException' in str(response.data)
```

---

#### TC-RA-003: 예외 케이스 - 사업자번호 중복 시 롤백
**목적**: 다른 사용자가 사용 중인 사업자번호로 등록 시도 시 롤백

**Given**:
- 사용자 A: 사업자번호 '1234567890' 등록됨
- 사용자 B: 미등록 상태

**When**:
```python
POST /advertiser/register (사용자 B가 동일 사업자번호로 등록 시도)
```

**Then**:
- HTTP 200 (폼 재표시)
- Flash 메시지: "이미 사용 중인 사업자등록번호입니다." (danger)
- 사용자 B의 `AdvertiserModel` 레코드 생성 안 됨 (롤백)

**AAA 패턴**:
```python
def test_register_advertiser_duplicate_business_number_rollback(client, app, registered_advertiser, advertiser_user):
    """예외 케이스: 사업자번호 중복 시 롤백 검증"""
    with app.app_context():
        # Arrange
        # advertiser_user는 미등록 상태
        login_user(client, advertiser_user.id)
        form_data = {
            'name': '김철수',
            'birth_date': '1985-05-05',
            'phone_number': '010-9999-8888',
            'business_name': '새로운 카페',
            'address': '부산시',
            'business_phone': '051-1111-2222',
            'business_number': '123-45-67890',  # 기존 사용자와 동일 (하이픈 포함)
            'representative_name': '김철수'
        }

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(AdvertiserModel)
        assert before_count == 1

        # Act
        response = client.post(
            '/advertiser/register',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 200

        # Assert - DB 롤백 확인 (레코드 개수 변화 없음)
        after_count = count_records(AdvertiserModel)
        assert after_count == 1

        # Assert - advertiser_user는 등록되지 않음
        advertiser = db.session.query(AdvertiserModel).filter_by(
            user_id=advertiser_user.id
        ).first()
        assert advertiser is None

        # Assert - Flash 메시지
        html = response.data.decode('utf-8')
        assert '사업자등록번호' in html or 'BusinessNumberAlreadyExistsException' in str(response.data)
```

---

#### TC-RA-004: 예외 케이스 - 일반 예외 시 롤백
**목적**: 예상치 못한 예외 발생 시 롤백 및 에러 메시지 표시

**Given**:
- 광고주 역할의 미등록 사용자

**When**:
```python
Mock으로 advertiser_service.register_advertiser()에서 Exception 발생 시뮬레이션
```

**Then**:
- HTTP 200 (폼 재표시)
- Flash 메시지: "광고주 정보 등록 중 오류가 발생했습니다: ..." (danger)
- DB 레코드 생성 안 됨 (롤백)

**AAA 패턴**:
```python
def test_register_advertiser_general_exception_rollback(client, app, advertiser_user, monkeypatch):
    """예외 케이스: 일반 예외 발생 시 롤백 검증"""
    with app.app_context():
        # Arrange
        login_user(client, advertiser_user.id)
        form_data = {
            'name': '홍길동',
            'birth_date': '1990-01-01',
            'phone_number': '010-1234-5678',
            'business_name': '테스트 카페',
            'address': '서울시 강남구 테헤란로 123',
            'business_phone': '02-1234-5678',
            'business_number': '123-45-67890',
            'representative_name': '홍길동'
        }

        # Mock: advertiser_service.register_advertiser()에서 예외 발생
        from app.application.services.advertiser_service import AdvertiserService

        def mock_register_advertiser(*args, **kwargs):
            raise Exception("데이터베이스 연결 오류")

        monkeypatch.setattr(
            AdvertiserService,
            'register_advertiser',
            mock_register_advertiser
        )

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(AdvertiserModel)

        # Act
        response = client.post(
            '/advertiser/register',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 200

        # Assert - DB 롤백 확인
        after_count = count_records(AdvertiserModel)
        assert after_count == before_count

        # Assert - Flash 메시지
        html = response.data.decode('utf-8')
        assert '오류가 발생했습니다' in html
```

---

### 3.2 인플루언서 정보 등록 (`register_influencer`)

#### TC-RI-001: 정상 케이스 - 인플루언서 정보 등록 성공
**목적**: 인플루언서 정보가 정상적으로 DB에 저장되고 커밋되는지 검증

**Given**:
- 인플루언서 역할의 미등록 사용자가 로그인
- 유효한 인플루언서 정보 폼 데이터

**When**:
```python
POST /influencer/register
form_data = {
    'name': '김인플루',
    'birth_date': '1995-03-15',
    'phone_number': '010-9876-5432',
    'channel_type': 'instagram',
    'channel_name': 'test_influencer',
    'channel_url': 'https://instagram.com/test_influencer',
    'follower_count': 10000
}
```

**Then**:
- HTTP 302 Redirect → `/` (홈)
- Flash 메시지: "인플루언서 정보가 성공적으로 등록되었습니다!" (success)
- `InfluencerModel` 레코드 1개 추가
- DB에서 조회 시 정보 일치 확인

**AAA 패턴**:
```python
def test_register_influencer_success(client, app, influencer_user):
    """정상 케이스: 인플루언서 정보 등록 성공 및 DB 커밋 검증"""
    with app.app_context():
        # Arrange
        login_user(client, influencer_user.id)
        form_data = {
            'name': '김인플루',
            'birth_date': '1995-03-15',
            'phone_number': '010-9876-5432',
            'channel_type': 'instagram',
            'channel_name': 'test_influencer',
            'channel_url': 'https://instagram.com/test_influencer',
            'follower_count': 10000
        }

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(InfluencerModel)
        assert before_count == 0

        # Act
        response = client.post(
            '/influencer/register',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 302
        assert response.location == url_for('main.home')

        # Assert - DB 저장 확인
        after_count = count_records(InfluencerModel)
        assert after_count == 1

        # Assert - 저장된 데이터 검증
        influencer = db.session.query(InfluencerModel).filter_by(
            user_id=influencer_user.id
        ).first()
        assert influencer is not None
        assert influencer.name == '김인플루'
        assert influencer.follower_count == 10000

        # Assert - Flash 메시지
        with client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert len(flashes) == 1
            assert flashes[0][0] == 'success'
            assert '성공적으로 등록되었습니다' in flashes[0][1]
```

---

#### TC-RI-002: 예외 케이스 - 중복 등록 시 롤백
**목적**: 이미 등록된 인플루언서가 재등록 시도 시 롤백

**Given**:
- 이미 인플루언서 정보가 등록된 사용자

**When**:
```python
POST /influencer/register (재등록 시도)
```

**Then**:
- HTTP 200 (폼 재표시)
- Flash 메시지: "이미 인플루언서 정보가 등록되어 있습니다." (danger)
- DB 레코드 개수 변화 없음 (롤백 확인)

**AAA 패턴**:
```python
def test_register_influencer_duplicate_rollback(client, app):
    """예외 케이스: 중복 등록 시 롤백 검증"""
    with app.app_context():
        # Arrange - 이미 등록된 인플루언서
        user = UserModel(
            id='registered-influencer-id',
            email='registered_influencer@example.com',
            role='influencer'
        )
        db.session.add(user)
        db.session.flush()

        influencer = InfluencerModel(
            id=1,
            user_id=user.id,
            name='기존 인플루언서',
            birth_date=date(1995, 1, 1),
            phone_number='010-1111-2222',
            channel_name='existing_channel',
            channel_url='https://instagram.com/existing',
            follower_count=5000
        )
        db.session.add(influencer)
        db.session.commit()

        login_user(client, user.id)
        form_data = {
            'name': '새로운 이름',
            'birth_date': '1998-08-08',
            'phone_number': '010-9999-9999',
            'channel_type': 'instagram',
            'channel_name': 'new_channel',
            'channel_url': 'https://instagram.com/new',
            'follower_count': 20000
        }

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(InfluencerModel)
        assert before_count == 1

        # Act
        response = client.post(
            '/influencer/register',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 200

        # Assert - DB 롤백 확인
        after_count = count_records(InfluencerModel)
        assert after_count == 1

        # Assert - 기존 데이터 유지
        influencer = db.session.query(InfluencerModel).filter_by(
            user_id=user.id
        ).first()
        assert influencer.name == '기존 인플루언서'

        # Cleanup
        db.session.delete(influencer)
        db.session.delete(user)
        db.session.commit()
```

---

#### TC-RI-003: 예외 케이스 - 잘못된 값 입력 시 롤백
**목적**: 잘못된 값(예: 음수 팔로워 수) 입력 시 롤백

**Given**:
- 인플루언서 역할의 미등록 사용자

**When**:
```python
POST /influencer/register (팔로워 수 = -100)
```

**Then**:
- HTTP 200 (폼 재표시)
- Flash 메시지 표시 (ValueError 또는 검증 에러)
- DB 레코드 생성 안 됨

**AAA 패턴**:
```python
def test_register_influencer_invalid_value_rollback(client, app, influencer_user, monkeypatch):
    """예외 케이스: 잘못된 값 입력 시 롤백 검증"""
    with app.app_context():
        # Arrange
        login_user(client, influencer_user.id)
        form_data = {
            'name': '김인플루',
            'birth_date': '1995-03-15',
            'phone_number': '010-9876-5432',
            'channel_type': 'instagram',
            'channel_name': 'test_influencer',
            'channel_url': 'https://instagram.com/test_influencer',
            'follower_count': 10000
        }

        # Mock: influencer_service.register_influencer()에서 ValueError 발생
        from app.application.services.influencer_service import InfluencerService

        def mock_register_influencer(*args, **kwargs):
            raise ValueError("팔로워 수는 0 이상이어야 합니다.")

        monkeypatch.setattr(
            InfluencerService,
            'register_influencer',
            mock_register_influencer
        )

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(InfluencerModel)

        # Act
        response = client.post(
            '/influencer/register',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 200

        # Assert - DB 롤백 확인
        after_count = count_records(InfluencerModel)
        assert after_count == before_count

        # Assert - Flash 메시지
        html = response.data.decode('utf-8')
        assert '팔로워' in html or 'ValueError' in str(response.data)
```

---

### 3.3 체험단 생성 (`create_campaign`)

#### TC-CC-001: 정상 케이스 - 체험단 생성 성공
**목적**: 체험단이 정상적으로 DB에 저장되고 커밋되는지 검증

**Given**:
- 광고주 정보가 등록된 사용자가 로그인
- 유효한 체험단 생성 폼 데이터

**When**:
```python
POST /advertiser/campaign/create
form_data = {
    'title': '신메뉴 파스타 체험단 모집',
    'description': '새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
    'quota': 5,
    'start_date': '2025-11-16',
    'end_date': '2025-12-01',
    'benefits': '무료 식사 제공',
    'conditions': '인스타그램 피드 1개 + 스토리 2개 업로드'
}
```

**Then**:
- HTTP 302 Redirect → `/advertiser/dashboard`
- Flash 메시지: "체험단이 성공적으로 생성되었습니다!" (success)
- `CampaignModel` 레코드 1개 추가
- DB에서 조회 시 정보 일치 확인
- 체험단 상태: 'RECRUITING'

**AAA 패턴**:
```python
def test_create_campaign_success(client, app, registered_advertiser):
    """정상 케이스: 체험단 생성 성공 및 DB 커밋 검증"""
    with app.app_context():
        # Arrange
        login_user(client, registered_advertiser.id)
        form_data = {
            'title': '신메뉴 파스타 체험단 모집',
            'description': '새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
            'quota': 5,
            'start_date': '2025-11-16',
            'end_date': '2025-12-01',
            'benefits': '무료 식사 제공',
            'conditions': '인스타그램 피드 1개 + 스토리 2개 업로드'
        }

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(CampaignModel)
        assert before_count == 0

        # Act
        response = client.post(
            '/advertiser/campaign/create',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 302
        assert response.location == url_for('advertiser.dashboard')

        # Assert - DB 저장 확인
        after_count = count_records(CampaignModel)
        assert after_count == 1

        # Assert - 저장된 데이터 검증
        campaign = db.session.query(CampaignModel).filter_by(
            title='신메뉴 파스타 체험단 모집'
        ).first()
        assert campaign is not None
        assert campaign.quota == 5
        assert campaign.status == 'RECRUITING'
        assert campaign.advertiser_id == 1

        # Assert - Flash 메시지
        with client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert len(flashes) == 1
            assert flashes[0][0] == 'success'
            assert '성공적으로 생성되었습니다' in flashes[0][1]
```

---

#### TC-CC-002: 폼 검증 실패 - 필수 필드 누락
**목적**: 폼 검증 실패 시 Flash 메시지 표시 및 DB 저장 안 됨 확인

**Given**:
- 광고주 정보가 등록된 사용자가 로그인
- 필수 필드 누락된 폼 데이터 (title 없음)

**When**:
```python
POST /advertiser/campaign/create
form_data = {
    'description': '설명',
    'quota': 5,
    'start_date': '2025-11-16',
    'end_date': '2025-12-01',
    'benefits': '혜택',
    'conditions': '조건'
    # title 누락
}
```

**Then**:
- HTTP 200 (폼 재표시)
- Flash 메시지: "title: This field is required." (danger)
- `CampaignModel` 레코드 생성 안 됨

**AAA 패턴**:
```python
def test_create_campaign_form_validation_failure(client, app, registered_advertiser):
    """폼 검증 실패: 필수 필드 누락 시 Flash 메시지 및 DB 저장 안 됨"""
    with app.app_context():
        # Arrange
        login_user(client, registered_advertiser.id)
        form_data = {
            'description': '설명',
            'quota': 5,
            'start_date': '2025-11-16',
            'end_date': '2025-12-01',
            'benefits': '혜택',
            'conditions': '조건'
            # title 누락
        }

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(CampaignModel)

        # Act
        response = client.post(
            '/advertiser/campaign/create',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 200

        # Assert - DB 저장 안 됨
        after_count = count_records(CampaignModel)
        assert after_count == before_count

        # Assert - Flash 메시지 (폼 에러)
        html = response.data.decode('utf-8')
        assert 'title' in html.lower() or 'This field is required' in html
```

---

#### TC-CC-003: 예외 케이스 - 일반 예외 시 롤백
**목적**: 예상치 못한 예외 발생 시 롤백 및 에러 메시지 표시

**Given**:
- 광고주 정보가 등록된 사용자가 로그인
- 유효한 폼 데이터

**When**:
```python
Mock으로 campaign_service.create_campaign()에서 Exception 발생 시뮬레이션
```

**Then**:
- HTTP 200 (폼 재표시)
- Flash 메시지: "체험단 생성 중 오류가 발생했습니다: ..." (danger)
- DB 레코드 생성 안 됨 (롤백)

**AAA 패턴**:
```python
def test_create_campaign_general_exception_rollback(client, app, registered_advertiser, monkeypatch):
    """예외 케이스: 일반 예외 발생 시 롤백 검증"""
    with app.app_context():
        # Arrange
        login_user(client, registered_advertiser.id)
        form_data = {
            'title': '신메뉴 파스타 체험단 모집',
            'description': '새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.',
            'quota': 5,
            'start_date': '2025-11-16',
            'end_date': '2025-12-01',
            'benefits': '무료 식사 제공',
            'conditions': '인스타그램 피드 1개 + 스토리 2개 업로드'
        }

        # Mock: campaign_service.create_campaign()에서 예외 발생
        from app.application.services.campaign_service import CampaignService

        def mock_create_campaign(*args, **kwargs):
            raise Exception("데이터베이스 연결 오류")

        monkeypatch.setattr(
            CampaignService,
            'create_campaign',
            mock_create_campaign
        )

        # DB 레코드 개수 확인 (Before)
        before_count = count_records(CampaignModel)

        # Act
        response = client.post(
            '/advertiser/campaign/create',
            data=form_data,
            follow_redirects=False
        )

        # Assert - HTTP 응답
        assert response.status_code == 200

        # Assert - DB 롤백 확인
        after_count = count_records(CampaignModel)
        assert after_count == before_count

        # Assert - Flash 메시지
        html = response.data.decode('utf-8')
        assert '오류가 발생했습니다' in html
```

---

## 4. 테스트 파일 구조

### 4.1 파일 위치
```
tests/
├── integration/
│   └── routes/
│       ├── __init__.py
│       ├── test_advertiser_routes_transaction.py  # 광고주 라우트 트랜잭션 테스트
│       └── test_influencer_routes_transaction.py  # 인플루언서 라우트 트랜잭션 테스트
```

### 4.2 테스트 클래스 구조

#### test_advertiser_routes_transaction.py
```python
"""
광고주 라우트 트랜잭션 처리 통합 테스트
"""

import pytest
from datetime import date
from flask import url_for
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.models.advertiser_model import AdvertiserModel
from app.infrastructure.persistence.models.campaign_model import CampaignModel
from app.extensions import db


class TestAdvertiserRegisterTransaction:
    """광고주 정보 등록 트랜잭션 테스트"""

    # TC-RA-001, TC-RA-002, TC-RA-003, TC-RA-004


class TestCampaignCreateTransaction:
    """체험단 생성 트랜잭션 테스트"""

    # TC-CC-001, TC-CC-002, TC-CC-003
```

#### test_influencer_routes_transaction.py
```python
"""
인플루언서 라우트 트랜잭션 처리 통합 테스트
"""

import pytest
from datetime import date
from flask import url_for
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.models.influencer_model import InfluencerModel
from app.extensions import db


class TestInfluencerRegisterTransaction:
    """인플루언서 정보 등록 트랜잭션 테스트"""

    # TC-RI-001, TC-RI-002, TC-RI-003
```

---

## 5. 테스트 실행

### 5.1 전체 통합 테스트 실행
```bash
pytest tests/integration/routes/ -v
```

### 5.2 특정 테스트 파일 실행
```bash
pytest tests/integration/routes/test_advertiser_routes_transaction.py -v
pytest tests/integration/routes/test_influencer_routes_transaction.py -v
```

### 5.3 특정 테스트 케이스 실행
```bash
pytest tests/integration/routes/test_advertiser_routes_transaction.py::TestAdvertiserRegisterTransaction::test_register_advertiser_success -v
```

### 5.4 커버리지 확인
```bash
pytest tests/integration/routes/ --cov=app.presentation.routes --cov-report=html
```

---

## 6. 검증 항목 체크리스트

### 6.1 HTTP 응답 검증
- [ ] 정상 케이스: HTTP 302 Redirect
- [ ] 예외 케이스: HTTP 200 (폼 재표시)
- [ ] Redirect 경로 정확성

### 6.2 데이터베이스 검증
- [ ] 정상 케이스: 레코드 생성 확인
- [ ] 예외 케이스: 레코드 생성 안 됨 (롤백)
- [ ] 저장된 데이터 정확성
- [ ] 트랜잭션 커밋/롤백 확인

### 6.3 Flash 메시지 검증
- [ ] 정상 케이스: success 메시지
- [ ] 예외 케이스: danger 메시지
- [ ] 메시지 내용 정확성

### 6.4 폼 검증
- [ ] 필수 필드 검증
- [ ] 폼 에러 메시지 표시
- [ ] 검증 실패 시 DB 저장 안 됨

---

## 7. 예상 이슈 및 대응

### 7.1 세션 관리
**이슈**: Flask Test Client에서 세션 유지 안 됨
**대응**: `with client.session_transaction() as sess:` 사용

### 7.2 DB 트랜잭션 격리
**이슈**: 테스트 간 DB 상태 공유
**대응**: 각 테스트마다 `@pytest.fixture(scope='function')` 사용

### 7.3 Mock 적용 범위
**이슈**: monkeypatch 적용 시점
**대응**: 테스트 함수 내부에서 monkeypatch 적용

### 7.4 Flash 메시지 추출
**이슈**: response.data에서 Flash 메시지 추출 어려움
**대응**: `session_transaction()` 사용하여 `_flashes` 직접 조회

---

## 8. TDD 원칙 준수

### 8.1 Red-Green-Refactor
1. **Red**: 테스트 작성 후 실행 → 실패 확인
2. **Green**: 최소 코드 작성 → 테스트 통과
3. **Refactor**: 코드 개선 → 테스트 유지

### 8.2 AAA 패턴
- **Arrange**: 테스트 데이터 및 환경 준비
- **Act**: 라우트 호출
- **Assert**: 결과 검증 (HTTP, DB, Flash)

### 8.3 FIRST 원칙
- **Fast**: 각 테스트 < 100ms
- **Independent**: 테스트 간 독립성 (픽스처 사용)
- **Repeatable**: 동일 결과 보장 (in-memory DB)
- **Self-validating**: assert로 명확한 검증
- **Timely**: 기능 구현 직후 테스트 작성

---

## 9. 참고 문서
- `docs/rules/tdd.md`: TDD 프로세스 가이드라인
- `tests/conftest.py`: 테스트 환경 설정
- `tests/e2e/routes/test_campaign_routes.py`: 기존 E2E 테스트 참고
- `tests/integration/services/test_application_service.py`: 서비스 통합 테스트 참고

---

## 10. 테스트 구현 순서

### Phase 1: 광고주 정보 등록 (우선순위: 높음)
1. TC-RA-001: 정상 케이스
2. TC-RA-002: 중복 등록 롤백
3. TC-RA-003: 사업자번호 중복 롤백
4. TC-RA-004: 일반 예외 롤백

### Phase 2: 인플루언서 정보 등록 (우선순위: 높음)
1. TC-RI-001: 정상 케이스
2. TC-RI-002: 중복 등록 롤백
3. TC-RI-003: 잘못된 값 롤백

### Phase 3: 체험단 생성 (우선순위: 중간)
1. TC-CC-001: 정상 케이스
2. TC-CC-002: 폼 검증 실패
3. TC-CC-003: 일반 예외 롤백

---

## 11. 성공 기준

### 11.1 테스트 통과율
- 전체 테스트 케이스 100% 통과

### 11.2 커버리지
- 라우트 트랜잭션 로직 커버리지 90% 이상

### 11.3 실행 시간
- 전체 통합 테스트 < 5초

### 11.4 문서화
- 각 테스트 케이스 docstring 명확히 작성
- AAA 패턴 주석 포함
