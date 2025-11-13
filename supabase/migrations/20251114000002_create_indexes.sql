-- =====================================================
-- Migration: 인덱스 생성
-- Description: 쿼리 성능 최적화를 위한 인덱스 생성
-- Date: 2025-11-14
-- =====================================================

-- =====================================================
-- 1. User 테이블 인덱스
-- =====================================================

-- 이메일 조회 (로그인 시 사용)
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_email ON "user" (email);

-- 역할별 조회 (역할이 있는 사용자만 인덱싱)
CREATE INDEX IF NOT EXISTS idx_user_role ON "user" (role) WHERE role IS NOT NULL;

-- =====================================================
-- 2. Advertiser 테이블 인덱스
-- =====================================================

-- User와의 조인 최적화 (1:1 관계)
CREATE UNIQUE INDEX IF NOT EXISTS idx_advertiser_user_id ON advertiser (user_id);

-- 사업자등록번호 중복 검증
CREATE UNIQUE INDEX IF NOT EXISTS idx_advertiser_business_number ON advertiser (business_number);

-- 휴대폰번호 검색
CREATE INDEX IF NOT EXISTS idx_advertiser_phone_number ON advertiser (phone_number);

-- =====================================================
-- 3. Influencer 테이블 인덱스
-- =====================================================

-- User와의 조인 최적화 (1:1 관계)
CREATE UNIQUE INDEX IF NOT EXISTS idx_influencer_user_id ON influencer (user_id);

-- 휴대폰번호 검색
CREATE INDEX IF NOT EXISTS idx_influencer_phone_number ON influencer (phone_number);

-- =====================================================
-- 4. Campaign 테이블 인덱스
-- =====================================================

-- Advertiser와의 조인 최적화 (N:1 관계)
CREATE INDEX IF NOT EXISTS idx_campaign_advertiser_id ON campaign (advertiser_id);

-- 상태별 조회 (모집중, 모집종료 등)
CREATE INDEX IF NOT EXISTS idx_campaign_status ON campaign (status);

-- 마감일 기준 정렬 (마감임박순)
CREATE INDEX IF NOT EXISTS idx_campaign_end_date ON campaign (end_date);

-- 최신순 정렬
CREATE INDEX IF NOT EXISTS idx_campaign_created_at ON campaign (created_at DESC);

-- 모집 중인 체험단 조회 최적화 (Partial Index)
CREATE INDEX IF NOT EXISTS idx_campaign_recruiting ON campaign (status) WHERE status = 'RECRUITING';

-- 복합 인덱스: 모집 중인 체험단을 최신순으로 조회
CREATE INDEX IF NOT EXISTS idx_campaign_status_created_at
  ON campaign (status, created_at DESC)
  WHERE status = 'RECRUITING';

-- =====================================================
-- 5. Application 테이블 인덱스
-- =====================================================

-- 중복 지원 방지 (UNIQUE 복합 인덱스)
CREATE UNIQUE INDEX IF NOT EXISTS idx_application_campaign_influencer
  ON application (campaign_id, influencer_id);

-- Influencer와의 조인 최적화 (지원 내역 조회)
CREATE INDEX IF NOT EXISTS idx_application_influencer_id ON application (influencer_id);

-- Campaign과의 조인 최적화 (지원자 목록 조회)
CREATE INDEX IF NOT EXISTS idx_application_campaign_id ON application (campaign_id);

-- 상태별 조회 (선정됨, 탈락 등)
CREATE INDEX IF NOT EXISTS idx_application_status ON application (status);

-- 최신 지원 순 정렬
CREATE INDEX IF NOT EXISTS idx_application_applied_at ON application (applied_at DESC);

-- 복합 인덱스: 특정 인플루언서의 지원 내역을 최신순으로 조회
CREATE INDEX IF NOT EXISTS idx_application_influencer_applied_at
  ON application (influencer_id, applied_at DESC);

-- =====================================================
-- 인덱스 생성 완료
-- =====================================================

-- 통계 정보 업데이트 (쿼리 플래너 최적화)
ANALYZE "user";
ANALYZE advertiser;
ANALYZE influencer;
ANALYZE campaign;
ANALYZE application;
