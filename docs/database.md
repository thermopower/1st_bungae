# 데이터베이스 설계 문서 (Database Design)
# 체험단 매칭 플랫폼 "1st_bungae"

---

## 문서 정보

| 항목 | 내용 |
|------|------|
| **문서명** | 데이터베이스 설계 문서 |
| **프로젝트명** | 1st_bungae |
| **버전** | 1.0.0 |
| **작성일** | 2025-11-14 |
| **DBMS** | PostgreSQL 13+ |
| **ORM** | SQLAlchemy 2.0+ |

---

## 목차

1. [데이터 모델 개요](#1-데이터-모델-개요)
2. [ERD (Entity Relationship Diagram)](#2-erd-entity-relationship-diagram)
3. [테이블 스키마 상세](#3-테이블-스키마-상세)
4. [관계 (Relationships) 정의](#4-관계-relationships-정의)
5. [데이터 플로우 (Data Flow)](#5-데이터-플로우-data-flow)
6. [데이터 무결성 규칙](#6-데이터-무결성-규칙)
7. [인덱스 전략](#7-인덱스-전략)
8. [마이그레이션 전략](#8-마이그레이션-전략)

---

## 1. 데이터 모델 개요

### 1.1 핵심 엔티티

본 플랫폼은 **5개의 핵심 테이블**로 구성됩니다:

1. **User** (사용자): 인증 및 기본 정보
2. **Advertiser** (광고주): 광고주 상세 정보
3. **Influencer** (인플루언서): 인플루언서 상세 정보
4. **Campaign** (체험단): 체험단 정보
5. **Application** (지원): 체험단 지원 정보

### 1.2 설계 원칙

#### 정규화 (Normalization)
- **3차 정규형 (3NF)** 준수
- 중복 데이터 최소화
- 이상 현상 방지

#### 유연성 (Flexibility)
- 역할 기반 테이블 분리 (Advertiser, Influencer)
- 확장 가능한 상태 관리 (status 컬럼)

#### 성능 (Performance)
- 자주 조회되는 컬럼에 인덱스 설정
- JOIN 최적화를 위한 외래 키 설계

---

## 2. ERD (Entity Relationship Diagram)

### 2.1 개념적 ERD

```
                    ┌─────────────────┐
                    │      User       │
                    │                 │
                    │  (인증 정보)      │
                    └────────┬────────┘
                             │
                             │ 1:1
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            │                │                │
     ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼──────┐
     │ Advertiser  │  │ Influencer  │  │            │
     │             │  │             │  │            │
     │ (광고주 정보) │  │(인플루언서   │  │            │
     │             │  │   정보)      │  │            │
     └──────┬──────┘  └──────┬──────┘  │            │
            │                │         │            │
            │ 1:N            │ 1:N     │            │
            │                │         │            │
     ┌──────▼──────┐  ┌──────▼──────┐  │            │
     │  Campaign   │  │Application  │  │            │
     │             │  │             │  │            │
     │ (체험단)     ├─►│  (지원)      │  │            │
     │             │N:1│             │  │            │
     └─────────────┘  └─────────────┘  │            │
                                       │            │
```

### 2.2 논리적 ERD (상세)

```
┌─────────────────────────────┐
│          User               │
├─────────────────────────────┤
│ id (PK, UUID)               │◄──────┐
│ email (UNIQUE)              │       │
│ role (VARCHAR)              │       │ FK
│ created_at (TIMESTAMP)      │       │
└─────────────────────────────┘       │
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        │                             │                             │
┌───────▼──────────────┐   ┌──────────▼─────────┐   ┌──────────────▼──────┐
│    Advertiser        │   │    Influencer      │   │                     │
├──────────────────────┤   ├────────────────────┤   │                     │
│ id (PK, SERIAL)      │   │ id (PK, SERIAL)    │   │                     │
│ user_id (FK, UNIQUE) │   │ user_id (FK, UNIQ) │   │                     │
│ name                 │   │ name               │   │                     │
│ birth_date           │   │ birth_date         │   │                     │
│ phone_number         │   │ phone_number       │   │                     │
│ business_name        │   │ channel_name       │   │                     │
│ address              │   │ channel_url        │   │                     │
│ business_phone       │   │ follower_count     │   │                     │
│ business_number      │   │ created_at         │   │                     │
│ representative_name  │   └────────┬───────────┘   │                     │
│ created_at           │            │               │                     │
└──────┬───────────────┘            │ 1:N           │                     │
       │                            │               │                     │
       │ 1:N                        │               │                     │
       │                            │               │                     │
┌──────▼────────────────────┐       │               │                     │
│       Campaign            │       │               │                     │
├───────────────────────────┤       │               │                     │
│ id (PK, SERIAL)           │       │               │                     │
│ advertiser_id (FK)        │       │               │                     │
│ title                     │       │               │                     │
│ description               │       │               │                     │
│ quota                     │       │               │                     │
│ start_date                │       │               │                     │
│ end_date                  │       │               │                     │
│ benefits                  │       │               │                     │
│ conditions                │       │               │                     │
│ image_url                 │       │               │                     │
│ status                    │       │               │                     │
│ created_at                │       │               │                     │
│ closed_at                 │       │               │                     │
└──────┬────────────────────┘       │               │                     │
       │                            │               │                     │
       │ 1:N                        │               │                     │
       │                            │               │                     │
┌──────▼────────────────────────────▼───────┐       │                     │
│           Application                     │       │                     │
├───────────────────────────────────────────┤       │                     │
│ id (PK, SERIAL)                           │       │                     │
│ campaign_id (FK)                          │       │                     │
│ influencer_id (FK)                        │       │                     │
│ application_reason (TEXT, NULL)           │       │                     │
│ status (VARCHAR)                          │       │                     │
│ applied_at (TIMESTAMP)                    │       │                     │
│ UNIQUE(campaign_id, influencer_id)        │       │                     │
└───────────────────────────────────────────┘       │                     │
```

---

## 3. 테이블 스키마 상세

### 3.1 User (사용자)

**목적**: Supabase Auth와 연동되는 사용자 인증 정보 저장

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | UUID | PK, NOT NULL | - | Supabase Auth UUID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | - | 사용자 이메일 |
| role | VARCHAR(20) | NULL | NULL | 사용자 역할 (advertiser/influencer) |
| created_at | TIMESTAMPTZ | NOT NULL | NOW() | 계정 생성일 |

**인덱스**:
```sql
CREATE UNIQUE INDEX idx_user_email ON "user" (email);
CREATE INDEX idx_user_role ON "user" (role);
```

**비즈니스 규칙**:
- `id`는 Supabase Auth에서 자동 생성된 UUID를 사용
- `role`은 Advertiser 또는 Influencer 정보 등록 시 업데이트
- `email`은 Supabase Auth에서 관리하므로 중복 불가

---

### 3.2 Advertiser (광고주)

**목적**: 광고주 사업자 정보 저장

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | SERIAL | PK | - | 광고주 ID (자동 증가) |
| user_id | UUID | FK(User.id), UNIQUE, NOT NULL | - | User 테이블 참조 |
| name | VARCHAR(100) | NOT NULL | - | 이름 |
| birth_date | DATE | NOT NULL | - | 생년월일 |
| phone_number | VARCHAR(20) | NOT NULL | - | 휴대폰번호 (010-XXXX-XXXX) |
| business_name | VARCHAR(100) | NOT NULL | - | 업체명 |
| address | TEXT | NOT NULL | - | 주소 |
| business_phone | VARCHAR(20) | NOT NULL | - | 업장 전화번호 |
| business_number | VARCHAR(10) | UNIQUE, NOT NULL | - | 사업자등록번호 (10자리) |
| representative_name | VARCHAR(100) | NOT NULL | - | 대표자명 |
| created_at | TIMESTAMPTZ | NOT NULL | NOW() | 등록일 |

**인덱스**:
```sql
CREATE UNIQUE INDEX idx_advertiser_user_id ON advertiser (user_id);
CREATE UNIQUE INDEX idx_advertiser_business_number ON advertiser (business_number);
CREATE INDEX idx_advertiser_phone_number ON advertiser (phone_number);
```

**비즈니스 규칙**:
- `user_id`는 User 테이블과 1:1 관계
- `business_number`는 10자리 숫자로만 구성 (검증은 애플리케이션 레벨)
- `phone_number`는 중복 가능 (대표와 담당자가 다를 수 있음)

---

### 3.3 Influencer (인플루언서)

**목적**: 인플루언서 SNS 채널 정보 저장

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | SERIAL | PK | - | 인플루언서 ID (자동 증가) |
| user_id | UUID | FK(User.id), UNIQUE, NOT NULL | - | User 테이블 참조 |
| name | VARCHAR(100) | NOT NULL | - | 이름 |
| birth_date | DATE | NOT NULL | - | 생년월일 |
| phone_number | VARCHAR(20) | NOT NULL | - | 휴대폰번호 (010-XXXX-XXXX) |
| channel_name | VARCHAR(100) | NOT NULL | - | SNS 채널명 |
| channel_url | TEXT | NOT NULL | - | 채널 링크 (URL) |
| follower_count | INTEGER | NOT NULL, CHECK >= 0 | - | 팔로워 수 |
| created_at | TIMESTAMPTZ | NOT NULL | NOW() | 등록일 |

**인덱스**:
```sql
CREATE UNIQUE INDEX idx_influencer_user_id ON influencer (user_id);
CREATE INDEX idx_influencer_phone_number ON influencer (phone_number);
CREATE INDEX idx_influencer_channel_url ON influencer (channel_url);
```

**비즈니스 규칙**:
- `user_id`는 User 테이블과 1:1 관계
- `follower_count`는 0 이상의 정수 (CHECK 제약조건)
- `channel_url`은 중복 검증 (애플리케이션 레벨)

---

### 3.4 Campaign (체험단)

**목적**: 광고주가 생성한 체험단 정보 저장

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | SERIAL | PK | - | 체험단 ID (자동 증가) |
| advertiser_id | INTEGER | FK(Advertiser.id), NOT NULL | - | 광고주 ID |
| title | VARCHAR(100) | NOT NULL | - | 체험단 제목 |
| description | TEXT | NOT NULL | - | 체험단 설명 (2000자 이하) |
| quota | INTEGER | NOT NULL, CHECK >= 1 | - | 모집 인원 |
| start_date | DATE | NOT NULL | - | 모집 시작일 |
| end_date | DATE | NOT NULL | - | 모집 종료일 |
| benefits | TEXT | NOT NULL | - | 제공 혜택 |
| conditions | TEXT | NOT NULL | - | 체험 조건 |
| image_url | TEXT | NULL | NULL | 대표 이미지 URL (Supabase Storage) |
| status | VARCHAR(20) | NOT NULL | 'RECRUITING' | 체험단 상태 (RECRUITING/CLOSED/SELECTED) |
| created_at | TIMESTAMPTZ | NOT NULL | NOW() | 생성일 |
| closed_at | TIMESTAMPTZ | NULL | NULL | 모집 종료일시 |

**인덱스**:
```sql
CREATE INDEX idx_campaign_advertiser_id ON campaign (advertiser_id);
CREATE INDEX idx_campaign_status ON campaign (status);
CREATE INDEX idx_campaign_end_date ON campaign (end_date);
CREATE INDEX idx_campaign_created_at ON campaign (created_at DESC);
```

**비즈니스 규칙**:
- `advertiser_id`는 Advertiser 테이블과 N:1 관계
- `quota`는 1 이상 (CHECK 제약조건)
- `start_date <= end_date` (애플리케이션 레벨 검증)
- `status` 값: 'RECRUITING' (모집중), 'CLOSED' (모집종료), 'SELECTED' (선정완료)

**상태 전이**:
```
RECRUITING → CLOSED → SELECTED
```

---

### 3.5 Application (체험단 지원)

**목적**: 인플루언서의 체험단 지원 정보 저장

| 컬럼명 | 타입 | 제약조건 | 기본값 | 설명 |
|--------|------|----------|--------|------|
| id | SERIAL | PK | - | 지원 ID (자동 증가) |
| campaign_id | INTEGER | FK(Campaign.id), NOT NULL | - | 체험단 ID |
| influencer_id | INTEGER | FK(Influencer.id), NOT NULL | - | 인플루언서 ID |
| application_reason | TEXT | NULL | NULL | 지원 사유 (선택, 1000자 이하) |
| status | VARCHAR(20) | NOT NULL | 'APPLIED' | 지원 상태 (APPLIED/SELECTED/REJECTED) |
| applied_at | TIMESTAMPTZ | NOT NULL | NOW() | 지원일시 |

**제약조건**:
```sql
ALTER TABLE application ADD CONSTRAINT uq_application_campaign_influencer
  UNIQUE (campaign_id, influencer_id);
```

**인덱스**:
```sql
CREATE UNIQUE INDEX idx_application_campaign_influencer
  ON application (campaign_id, influencer_id);
CREATE INDEX idx_application_influencer_id ON application (influencer_id);
CREATE INDEX idx_application_campaign_id ON application (campaign_id);
CREATE INDEX idx_application_status ON application (status);
CREATE INDEX idx_application_applied_at ON application (applied_at DESC);
```

**비즈니스 규칙**:
- `(campaign_id, influencer_id)` 복합 UNIQUE 제약조건 (중복 지원 방지)
- `status` 값: 'APPLIED' (지원완료), 'SELECTED' (선정됨), 'REJECTED' (탈락)

**상태 전이**:
```
APPLIED → SELECTED (선정 시)
APPLIED → REJECTED (미선정 시)
```

---

## 4. 관계 (Relationships) 정의

### 4.1 User ↔ Advertiser (1:1)

**관계 유형**: One-to-One (선택적)

**외래 키**: `advertiser.user_id → user.id`

**Cascade 규칙**:
```sql
ON DELETE CASCADE  -- User 삭제 시 Advertiser도 삭제
ON UPDATE CASCADE  -- User ID 변경 시 Advertiser도 업데이트
```

**SQLAlchemy 관계 정의**:
```python
# User 엔티티
advertiser = relationship("Advertiser", back_populates="user", uselist=False, cascade="all, delete-orphan")

# Advertiser 엔티티
user = relationship("User", back_populates="advertiser")
```

---

### 4.2 User ↔ Influencer (1:1)

**관계 유형**: One-to-One (선택적)

**외래 키**: `influencer.user_id → user.id`

**Cascade 규칙**:
```sql
ON DELETE CASCADE  -- User 삭제 시 Influencer도 삭제
ON UPDATE CASCADE
```

**SQLAlchemy 관계 정의**:
```python
# User 엔티티
influencer = relationship("Influencer", back_populates="user", uselist=False, cascade="all, delete-orphan")

# Influencer 엔티티
user = relationship("User", back_populates="influencer")
```

---

### 4.3 Advertiser ↔ Campaign (1:N)

**관계 유형**: One-to-Many

**외래 키**: `campaign.advertiser_id → advertiser.id`

**Cascade 규칙**:
```sql
ON DELETE RESTRICT  -- Advertiser 삭제 시 Campaign이 있으면 삭제 불가
ON UPDATE CASCADE
```

**SQLAlchemy 관계 정의**:
```python
# Advertiser 엔티티
campaigns = relationship("Campaign", back_populates="advertiser", cascade="all, delete")

# Campaign 엔티티
advertiser = relationship("Advertiser", back_populates="campaigns")
```

---

### 4.4 Campaign ↔ Application (1:N)

**관계 유형**: One-to-Many

**외래 키**: `application.campaign_id → campaign.id`

**Cascade 규칙**:
```sql
ON DELETE CASCADE  -- Campaign 삭제 시 Application도 삭제
ON UPDATE CASCADE
```

**SQLAlchemy 관계 정의**:
```python
# Campaign 엔티티
applications = relationship("Application", back_populates="campaign", cascade="all, delete-orphan")

# Application 엔티티
campaign = relationship("Campaign", back_populates="applications")
```

---

### 4.5 Influencer ↔ Application (1:N)

**관계 유형**: One-to-Many

**외래 키**: `application.influencer_id → influencer.id`

**Cascade 규칙**:
```sql
ON DELETE RESTRICT  -- Influencer 삭제 시 Application이 있으면 삭제 불가
ON UPDATE CASCADE
```

**SQLAlchemy 관계 정의**:
```python
# Influencer 엔티티
applications = relationship("Application", back_populates="influencer", cascade="all, delete")

# Application 엔티티
influencer = relationship("Influencer", back_populates="applications")
```

---

## 5. 데이터 플로우 (Data Flow)

### 5.1 회원가입 및 역할 등록 플로우

#### 5.1.1 회원가입

```
[사용자] → Supabase Auth (회원가입)
             ↓
         [User 테이블]
             INSERT (id, email, role=NULL, created_at)
             ↓
         [역할 선택 페이지]
```

**SQL**:
```sql
INSERT INTO "user" (id, email, created_at)
VALUES (:supabase_auth_uuid, :email, NOW());
```

---

#### 5.1.2 광고주 정보 등록

```
[광고주 정보 입력]
      ↓
  [트랜잭션 시작]
      ↓
  UPDATE user SET role = 'advertiser'
      ↓
  INSERT INTO advertiser (user_id, name, birth_date, ...)
      ↓
  [트랜잭션 커밋]
```

**SQL**:
```sql
BEGIN;

UPDATE "user" SET role = 'advertiser' WHERE id = :user_id;

INSERT INTO advertiser (
  user_id, name, birth_date, phone_number,
  business_name, address, business_phone,
  business_number, representative_name
) VALUES (
  :user_id, :name, :birth_date, :phone_number,
  :business_name, :address, :business_phone,
  :business_number, :representative_name
);

COMMIT;
```

---

#### 5.1.3 인플루언서 정보 등록

```
[인플루언서 정보 입력]
      ↓
  [트랜잭션 시작]
      ↓
  UPDATE user SET role = 'influencer'
      ↓
  INSERT INTO influencer (user_id, name, channel_name, ...)
      ↓
  [트랜잭션 커밋]
```

**SQL**:
```sql
BEGIN;

UPDATE "user" SET role = 'influencer' WHERE id = :user_id;

INSERT INTO influencer (
  user_id, name, birth_date, phone_number,
  channel_name, channel_url, follower_count
) VALUES (
  :user_id, :name, :birth_date, :phone_number,
  :channel_name, :channel_url, :follower_count
);

COMMIT;
```

---

### 5.2 체험단 생성 플로우

```
[광고주] → 체험단 정보 입력
             ↓
         [이미지 업로드] (Supabase Storage)
             ↓
         INSERT INTO campaign (advertiser_id, title, ...)
             ↓
         [Campaign 테이블]
```

**SQL**:
```sql
INSERT INTO campaign (
  advertiser_id, title, description, quota,
  start_date, end_date, benefits, conditions,
  image_url, status
) VALUES (
  :advertiser_id, :title, :description, :quota,
  :start_date, :end_date, :benefits, :conditions,
  :image_url, 'RECRUITING'
);
```

---

### 5.3 체험단 탐색 플로우

```
[홈 페이지 접속]
      ↓
  SELECT campaign WHERE status = 'RECRUITING'
      ↓
  JOIN advertiser ON campaign.advertiser_id = advertiser.id
      ↓
  [체험단 목록 표시]
```

**SQL**:
```sql
SELECT
  c.id, c.title, c.description, c.quota, c.end_date,
  c.image_url, c.created_at,
  a.business_name,
  COUNT(ap.id) AS application_count
FROM campaign c
INNER JOIN advertiser a ON c.advertiser_id = a.id
LEFT JOIN application ap ON c.id = ap.campaign_id
WHERE c.status = 'RECRUITING'
GROUP BY c.id, a.id
ORDER BY c.created_at DESC
LIMIT 12 OFFSET :offset;
```

---

### 5.4 체험단 지원 플로우

```
[인플루언서] → 체험단 상세 페이지
                  ↓
              [지원하기 버튼 클릭]
                  ↓
              [검증]
                - 인플루언서 정보 등록 여부
                - 모집 중 상태
                - 중복 지원 여부
                  ↓
              INSERT INTO application (campaign_id, influencer_id, ...)
                  ↓
              [Application 테이블]
```

**검증 SQL**:
```sql
-- 중복 지원 검증
SELECT COUNT(*) FROM application
WHERE campaign_id = :campaign_id
  AND influencer_id = :influencer_id;

-- 중복이 없으면 지원 데이터 삽입
INSERT INTO application (
  campaign_id, influencer_id,
  application_reason, status
) VALUES (
  :campaign_id, :influencer_id,
  :application_reason, 'APPLIED'
);
```

---

### 5.5 모집 조기종료 플로우

```
[광고주] → 체험단 관리 페이지
              ↓
          [조기종료 버튼 클릭]
              ↓
          UPDATE campaign
            SET status = 'CLOSED', closed_at = NOW()
            WHERE id = :campaign_id
              ↓
          [Campaign 테이블]
```

**SQL**:
```sql
UPDATE campaign
SET status = 'CLOSED', closed_at = NOW()
WHERE id = :campaign_id
  AND advertiser_id = :advertiser_id
  AND status = 'RECRUITING';
```

---

### 5.6 인플루언서 선정 플로우

```
[광고주] → 지원자 목록 확인
              ↓
          [인플루언서 선택]
              ↓
          [트랜잭션 시작]
              ↓
          UPDATE application SET status = 'SELECTED'
            WHERE id IN (:selected_ids)
              ↓
          UPDATE application SET status = 'REJECTED'
            WHERE campaign_id = :campaign_id
              AND id NOT IN (:selected_ids)
              ↓
          UPDATE campaign SET status = 'SELECTED'
            WHERE id = :campaign_id
              ↓
          [트랜잭션 커밋]
```

**SQL**:
```sql
BEGIN;

-- 선정된 인플루언서 상태 업데이트
UPDATE application
SET status = 'SELECTED'
WHERE id = ANY(:selected_ids)
  AND campaign_id = :campaign_id;

-- 미선정 인플루언서 상태 업데이트
UPDATE application
SET status = 'REJECTED'
WHERE campaign_id = :campaign_id
  AND id <> ALL(:selected_ids)
  AND status = 'APPLIED';

-- 체험단 상태 업데이트
UPDATE campaign
SET status = 'SELECTED'
WHERE id = :campaign_id;

COMMIT;
```

---

### 5.7 지원 내역 조회 플로우 (인플루언서)

```
[인플루언서] → 내 지원내역 페이지
                  ↓
              SELECT application
                WHERE influencer_id = :influencer_id
                  ↓
              JOIN campaign, advertiser
                  ↓
              [지원 내역 목록 표시]
```

**SQL**:
```sql
SELECT
  ap.id, ap.status, ap.applied_at,
  c.title AS campaign_title, c.end_date,
  a.business_name
FROM application ap
INNER JOIN campaign c ON ap.campaign_id = c.id
INNER JOIN advertiser a ON c.advertiser_id = a.id
WHERE ap.influencer_id = :influencer_id
ORDER BY ap.applied_at DESC;
```

---

## 6. 데이터 무결성 규칙

### 6.1 참조 무결성 (Referential Integrity)

#### 외래 키 제약조건

```sql
-- Advertiser → User
ALTER TABLE advertiser
  ADD CONSTRAINT fk_advertiser_user
  FOREIGN KEY (user_id) REFERENCES "user" (id)
  ON DELETE CASCADE ON UPDATE CASCADE;

-- Influencer → User
ALTER TABLE influencer
  ADD CONSTRAINT fk_influencer_user
  FOREIGN KEY (user_id) REFERENCES "user" (id)
  ON DELETE CASCADE ON UPDATE CASCADE;

-- Campaign → Advertiser
ALTER TABLE campaign
  ADD CONSTRAINT fk_campaign_advertiser
  FOREIGN KEY (advertiser_id) REFERENCES advertiser (id)
  ON DELETE RESTRICT ON UPDATE CASCADE;

-- Application → Campaign
ALTER TABLE application
  ADD CONSTRAINT fk_application_campaign
  FOREIGN KEY (campaign_id) REFERENCES campaign (id)
  ON DELETE CASCADE ON UPDATE CASCADE;

-- Application → Influencer
ALTER TABLE application
  ADD CONSTRAINT fk_application_influencer
  FOREIGN KEY (influencer_id) REFERENCES influencer (id)
  ON DELETE RESTRICT ON UPDATE CASCADE;
```

---

### 6.2 도메인 무결성 (Domain Integrity)

#### CHECK 제약조건

```sql
-- Campaign: quota는 1 이상
ALTER TABLE campaign
  ADD CONSTRAINT chk_campaign_quota
  CHECK (quota >= 1);

-- Campaign: start_date <= end_date
ALTER TABLE campaign
  ADD CONSTRAINT chk_campaign_dates
  CHECK (start_date <= end_date);

-- Influencer: follower_count는 0 이상
ALTER TABLE influencer
  ADD CONSTRAINT chk_influencer_follower_count
  CHECK (follower_count >= 0);

-- Campaign: status 값 제한
ALTER TABLE campaign
  ADD CONSTRAINT chk_campaign_status
  CHECK (status IN ('RECRUITING', 'CLOSED', 'SELECTED'));

-- Application: status 값 제한
ALTER TABLE application
  ADD CONSTRAINT chk_application_status
  CHECK (status IN ('APPLIED', 'SELECTED', 'REJECTED'));

-- User: role 값 제한
ALTER TABLE "user"
  ADD CONSTRAINT chk_user_role
  CHECK (role IS NULL OR role IN ('advertiser', 'influencer'));
```

---

### 6.3 엔티티 무결성 (Entity Integrity)

#### UNIQUE 제약조건

```sql
-- User: email은 고유
ALTER TABLE "user" ADD CONSTRAINT uq_user_email UNIQUE (email);

-- Advertiser: user_id는 고유 (1:1 관계)
ALTER TABLE advertiser ADD CONSTRAINT uq_advertiser_user_id UNIQUE (user_id);

-- Advertiser: business_number는 고유
ALTER TABLE advertiser ADD CONSTRAINT uq_advertiser_business_number UNIQUE (business_number);

-- Influencer: user_id는 고유 (1:1 관계)
ALTER TABLE influencer ADD CONSTRAINT uq_influencer_user_id UNIQUE (user_id);

-- Application: (campaign_id, influencer_id) 복합 고유 (중복 지원 방지)
ALTER TABLE application ADD CONSTRAINT uq_application_campaign_influencer
  UNIQUE (campaign_id, influencer_id);
```

---

### 6.4 트랜잭션 격리 수준 (Isolation Level)

**권장 격리 수준**: `READ COMMITTED` (PostgreSQL 기본값)

**동시성 문제 해결**:

#### 중복 지원 방지 (Race Condition)
```sql
-- 비관적 잠금 (Pessimistic Locking)
BEGIN;

SELECT * FROM campaign
WHERE id = :campaign_id
FOR UPDATE;  -- Row-level lock

INSERT INTO application (...) VALUES (...);

COMMIT;
```

#### 모집 인원 초과 방지
```sql
-- 낙관적 잠금 (Optimistic Locking) + 애플리케이션 검증
BEGIN;

SELECT COUNT(*) AS current_applications
FROM application
WHERE campaign_id = :campaign_id
FOR SHARE;  -- Shared lock (읽기 허용, 쓰기 차단)

-- 애플리케이션 레벨에서 quota 검증 후 삽입

INSERT INTO application (...) VALUES (...);

COMMIT;
```

---

## 7. 인덱스 전략

### 7.1 인덱스 목록

#### User 테이블
```sql
CREATE UNIQUE INDEX idx_user_email ON "user" (email);
CREATE INDEX idx_user_role ON "user" (role) WHERE role IS NOT NULL;
```

#### Advertiser 테이블
```sql
CREATE UNIQUE INDEX idx_advertiser_user_id ON advertiser (user_id);
CREATE UNIQUE INDEX idx_advertiser_business_number ON advertiser (business_number);
CREATE INDEX idx_advertiser_phone_number ON advertiser (phone_number);
```

#### Influencer 테이블
```sql
CREATE UNIQUE INDEX idx_influencer_user_id ON influencer (user_id);
CREATE INDEX idx_influencer_phone_number ON influencer (phone_number);
```

#### Campaign 테이블
```sql
CREATE INDEX idx_campaign_advertiser_id ON campaign (advertiser_id);
CREATE INDEX idx_campaign_status ON campaign (status);
CREATE INDEX idx_campaign_end_date ON campaign (end_date);
CREATE INDEX idx_campaign_created_at ON campaign (created_at DESC);
CREATE INDEX idx_campaign_recruiting ON campaign (status) WHERE status = 'RECRUITING';
```

#### Application 테이블
```sql
CREATE UNIQUE INDEX idx_application_campaign_influencer
  ON application (campaign_id, influencer_id);
CREATE INDEX idx_application_influencer_id ON application (influencer_id);
CREATE INDEX idx_application_campaign_id ON application (campaign_id);
CREATE INDEX idx_application_status ON application (status);
CREATE INDEX idx_application_applied_at ON application (applied_at DESC);
```

---

### 7.2 복합 인덱스 전략

#### 체험단 탐색 쿼리 최적화
```sql
-- 모집 중인 체험단을 최신순으로 조회
CREATE INDEX idx_campaign_status_created_at
  ON campaign (status, created_at DESC)
  WHERE status = 'RECRUITING';
```

#### 지원 내역 조회 최적화
```sql
-- 특정 인플루언서의 지원 내역을 최신순으로 조회
CREATE INDEX idx_application_influencer_applied_at
  ON application (influencer_id, applied_at DESC);
```

---

### 7.3 인덱스 유지보수

**정기적인 인덱스 재구축**:
```sql
REINDEX TABLE campaign;
REINDEX TABLE application;
```

**통계 정보 업데이트**:
```sql
ANALYZE campaign;
ANALYZE application;
```

---

## 8. 마이그레이션 전략

### 8.1 마이그레이션 도구

- **도구**: Flask-Migrate (Alembic)
- **마이그레이션 파일 위치**: `/supabase/migrations/`
- **네이밍 규칙**: `YYYYMMDDHHMMSS_description.sql`

---

### 8.2 마이그레이션 순서

#### Phase 1: 초기 스키마 생성

**파일명**: `20251114000001_create_initial_schema.sql`

```sql
-- 1. User 테이블 생성
CREATE TABLE "user" (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(20) CHECK (role IS NULL OR role IN ('advertiser', 'influencer')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Advertiser 테이블 생성
CREATE TABLE advertiser (
  id SERIAL PRIMARY KEY,
  user_id UUID UNIQUE NOT NULL REFERENCES "user" (id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  birth_date DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  business_name VARCHAR(100) NOT NULL,
  address TEXT NOT NULL,
  business_phone VARCHAR(20) NOT NULL,
  business_number VARCHAR(10) UNIQUE NOT NULL,
  representative_name VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Influencer 테이블 생성
CREATE TABLE influencer (
  id SERIAL PRIMARY KEY,
  user_id UUID UNIQUE NOT NULL REFERENCES "user" (id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  birth_date DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  channel_name VARCHAR(100) NOT NULL,
  channel_url TEXT NOT NULL,
  follower_count INTEGER NOT NULL CHECK (follower_count >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Campaign 테이블 생성
CREATE TABLE campaign (
  id SERIAL PRIMARY KEY,
  advertiser_id INTEGER NOT NULL REFERENCES advertiser (id) ON DELETE RESTRICT,
  title VARCHAR(100) NOT NULL,
  description TEXT NOT NULL,
  quota INTEGER NOT NULL CHECK (quota >= 1),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  benefits TEXT NOT NULL,
  conditions TEXT NOT NULL,
  image_url TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'RECRUITING' CHECK (status IN ('RECRUITING', 'CLOSED', 'SELECTED')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  closed_at TIMESTAMPTZ,
  CONSTRAINT chk_campaign_dates CHECK (start_date <= end_date)
);

-- 5. Application 테이블 생성
CREATE TABLE application (
  id SERIAL PRIMARY KEY,
  campaign_id INTEGER NOT NULL REFERENCES campaign (id) ON DELETE CASCADE,
  influencer_id INTEGER NOT NULL REFERENCES influencer (id) ON DELETE RESTRICT,
  application_reason TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'APPLIED' CHECK (status IN ('APPLIED', 'SELECTED', 'REJECTED')),
  applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_application_campaign_influencer UNIQUE (campaign_id, influencer_id)
);
```

---

#### Phase 2: 인덱스 생성

**파일명**: `20251114000002_create_indexes.sql`

```sql
-- User 인덱스
CREATE UNIQUE INDEX idx_user_email ON "user" (email);
CREATE INDEX idx_user_role ON "user" (role) WHERE role IS NOT NULL;

-- Advertiser 인덱스
CREATE UNIQUE INDEX idx_advertiser_user_id ON advertiser (user_id);
CREATE UNIQUE INDEX idx_advertiser_business_number ON advertiser (business_number);
CREATE INDEX idx_advertiser_phone_number ON advertiser (phone_number);

-- Influencer 인덱스
CREATE UNIQUE INDEX idx_influencer_user_id ON influencer (user_id);
CREATE INDEX idx_influencer_phone_number ON influencer (phone_number);

-- Campaign 인덱스
CREATE INDEX idx_campaign_advertiser_id ON campaign (advertiser_id);
CREATE INDEX idx_campaign_status ON campaign (status);
CREATE INDEX idx_campaign_end_date ON campaign (end_date);
CREATE INDEX idx_campaign_created_at ON campaign (created_at DESC);
CREATE INDEX idx_campaign_recruiting ON campaign (status) WHERE status = 'RECRUITING';

-- Application 인덱스
CREATE UNIQUE INDEX idx_application_campaign_influencer ON application (campaign_id, influencer_id);
CREATE INDEX idx_application_influencer_id ON application (influencer_id);
CREATE INDEX idx_application_campaign_id ON application (campaign_id);
CREATE INDEX idx_application_status ON application (status);
CREATE INDEX idx_application_applied_at ON application (applied_at DESC);

-- 복합 인덱스
CREATE INDEX idx_campaign_status_created_at ON campaign (status, created_at DESC) WHERE status = 'RECRUITING';
CREATE INDEX idx_application_influencer_applied_at ON application (influencer_id, applied_at DESC);
```

---

### 8.3 마이그레이션 실행

#### 개발 환경
```bash
# 마이그레이션 파일 적용
flask db upgrade

# 롤백
flask db downgrade
```

#### Supabase 환경
```bash
# Supabase CLI를 통한 마이그레이션
supabase migration up
```

---

### 8.4 데이터 시딩 (Seeding)

**개발/테스트용 샘플 데이터**

**파일명**: `20251114000003_seed_sample_data.sql`

```sql
-- 샘플 User (테스트용 UUID)
INSERT INTO "user" (id, email, role, created_at) VALUES
('11111111-1111-1111-1111-111111111111', 'advertiser1@test.com', 'advertiser', NOW()),
('22222222-2222-2222-2222-222222222222', 'influencer1@test.com', 'influencer', NOW());

-- 샘플 Advertiser
INSERT INTO advertiser (user_id, name, birth_date, phone_number, business_name, address, business_phone, business_number, representative_name) VALUES
('11111111-1111-1111-1111-111111111111', '김광고', '1985-05-15', '010-1234-5678', '테스트 카페', '서울시 강남구 테헤란로 123', '02-1234-5678', '1234567890', '김대표');

-- 샘플 Influencer
INSERT INTO influencer (user_id, name, birth_date, phone_number, channel_name, channel_url, follower_count) VALUES
('22222222-2222-2222-2222-222222222222', '이인플루', '1995-08-20', '010-9876-5432', '테스트 채널', 'https://www.youtube.com/@test', 50000);

-- 샘플 Campaign
INSERT INTO campaign (advertiser_id, title, description, quota, start_date, end_date, benefits, conditions, status) VALUES
(1, '신메뉴 파스타 체험단 모집', '새로 출시한 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다.', 5, '2025-11-15', '2025-11-30', '무료 식사 제공', '인스타그램 피드 1개 + 스토리 2개 업로드', 'RECRUITING');
```

---

## 9. 부록

### 9.1 전체 DDL 스크립트

전체 DDL은 `/supabase/migrations/20251114000001_create_initial_schema.sql` 참조

### 9.2 참고 문서

- `docs/userflow.md`: 사용자 플로우 문서
- `docs/prd.md`: 제품 요구사항 문서
- `CLAUDE.md`: 아키텍처 설계 문서

### 9.3 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|------|------|-----------|--------|
| 1.0.0 | 2025-11-14 | 초기 데이터베이스 설계 문서 작성 | Claude |

---

**문서 끝**
