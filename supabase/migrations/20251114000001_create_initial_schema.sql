-- =====================================================
-- Migration: 초기 데이터베이스 스키마 생성
-- Description: User, Advertiser, Influencer, Campaign, Application 테이블 생성
-- Date: 2025-11-14
-- =====================================================

-- =====================================================
-- 1. User 테이블 생성
-- Description: Supabase Auth와 연동되는 사용자 인증 정보
-- =====================================================
CREATE TABLE IF NOT EXISTS "user" (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  role VARCHAR(20) CHECK (role IS NULL OR role IN ('advertiser', 'influencer')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE "user" IS '사용자 인증 정보 (Supabase Auth 연동)';
COMMENT ON COLUMN "user".id IS 'Supabase Auth UUID';
COMMENT ON COLUMN "user".email IS '사용자 이메일';
COMMENT ON COLUMN "user".role IS '사용자 역할 (advertiser/influencer)';
COMMENT ON COLUMN "user".created_at IS '계정 생성일';

-- =====================================================
-- 2. Advertiser 테이블 생성
-- Description: 광고주 사업자 정보
-- =====================================================
CREATE TABLE IF NOT EXISTS advertiser (
  id SERIAL PRIMARY KEY,
  user_id UUID UNIQUE NOT NULL REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE,
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

COMMENT ON TABLE advertiser IS '광고주 정보';
COMMENT ON COLUMN advertiser.id IS '광고주 고유 ID';
COMMENT ON COLUMN advertiser.user_id IS 'User 테이블 참조 (1:1)';
COMMENT ON COLUMN advertiser.name IS '이름';
COMMENT ON COLUMN advertiser.birth_date IS '생년월일';
COMMENT ON COLUMN advertiser.phone_number IS '휴대폰번호 (010-XXXX-XXXX)';
COMMENT ON COLUMN advertiser.business_name IS '업체명';
COMMENT ON COLUMN advertiser.address IS '주소';
COMMENT ON COLUMN advertiser.business_phone IS '업장 전화번호';
COMMENT ON COLUMN advertiser.business_number IS '사업자등록번호 (10자리)';
COMMENT ON COLUMN advertiser.representative_name IS '대표자명';
COMMENT ON COLUMN advertiser.created_at IS '등록일';

-- =====================================================
-- 3. Influencer 테이블 생성
-- Description: 인플루언서 SNS 채널 정보
-- =====================================================
CREATE TABLE IF NOT EXISTS influencer (
  id SERIAL PRIMARY KEY,
  user_id UUID UNIQUE NOT NULL REFERENCES "user" (id) ON DELETE CASCADE ON UPDATE CASCADE,
  name VARCHAR(100) NOT NULL,
  birth_date DATE NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  channel_name VARCHAR(100) NOT NULL,
  channel_url TEXT NOT NULL,
  follower_count INTEGER NOT NULL CHECK (follower_count >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE influencer IS '인플루언서 정보';
COMMENT ON COLUMN influencer.id IS '인플루언서 고유 ID';
COMMENT ON COLUMN influencer.user_id IS 'User 테이블 참조 (1:1)';
COMMENT ON COLUMN influencer.name IS '이름';
COMMENT ON COLUMN influencer.birth_date IS '생년월일';
COMMENT ON COLUMN influencer.phone_number IS '휴대폰번호 (010-XXXX-XXXX)';
COMMENT ON COLUMN influencer.channel_name IS 'SNS 채널명';
COMMENT ON COLUMN influencer.channel_url IS '채널 링크 (URL)';
COMMENT ON COLUMN influencer.follower_count IS '팔로워 수 (0 이상)';
COMMENT ON COLUMN influencer.created_at IS '등록일';

-- =====================================================
-- 4. Campaign 테이블 생성
-- Description: 광고주가 생성한 체험단 정보
-- =====================================================
CREATE TABLE IF NOT EXISTS campaign (
  id SERIAL PRIMARY KEY,
  advertiser_id INTEGER NOT NULL REFERENCES advertiser (id) ON DELETE RESTRICT ON UPDATE CASCADE,
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

COMMENT ON TABLE campaign IS '체험단 정보';
COMMENT ON COLUMN campaign.id IS '체험단 고유 ID';
COMMENT ON COLUMN campaign.advertiser_id IS 'Advertiser 테이블 참조';
COMMENT ON COLUMN campaign.title IS '체험단 제목';
COMMENT ON COLUMN campaign.description IS '체험단 설명 (2000자 이하)';
COMMENT ON COLUMN campaign.quota IS '모집 인원 (1 이상)';
COMMENT ON COLUMN campaign.start_date IS '모집 시작일';
COMMENT ON COLUMN campaign.end_date IS '모집 종료일';
COMMENT ON COLUMN campaign.benefits IS '제공 혜택';
COMMENT ON COLUMN campaign.conditions IS '체험 조건';
COMMENT ON COLUMN campaign.image_url IS '대표 이미지 URL (Supabase Storage)';
COMMENT ON COLUMN campaign.status IS '체험단 상태 (RECRUITING/CLOSED/SELECTED)';
COMMENT ON COLUMN campaign.created_at IS '생성일';
COMMENT ON COLUMN campaign.closed_at IS '모집 종료일시';

-- =====================================================
-- 5. Application 테이블 생성
-- Description: 인플루언서의 체험단 지원 정보
-- =====================================================
CREATE TABLE IF NOT EXISTS application (
  id SERIAL PRIMARY KEY,
  campaign_id INTEGER NOT NULL REFERENCES campaign (id) ON DELETE CASCADE ON UPDATE CASCADE,
  influencer_id INTEGER NOT NULL REFERENCES influencer (id) ON DELETE RESTRICT ON UPDATE CASCADE,
  application_reason TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'APPLIED' CHECK (status IN ('APPLIED', 'SELECTED', 'REJECTED')),
  applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_application_campaign_influencer UNIQUE (campaign_id, influencer_id)
);

COMMENT ON TABLE application IS '체험단 지원 정보';
COMMENT ON COLUMN application.id IS '지원 고유 ID';
COMMENT ON COLUMN application.campaign_id IS 'Campaign 테이블 참조';
COMMENT ON COLUMN application.influencer_id IS 'Influencer 테이블 참조';
COMMENT ON COLUMN application.application_reason IS '지원 사유 (선택, 1000자 이하)';
COMMENT ON COLUMN application.status IS '지원 상태 (APPLIED/SELECTED/REJECTED)';
COMMENT ON COLUMN application.applied_at IS '지원일시';

-- =====================================================
-- 스키마 생성 완료
-- =====================================================
