-- =====================================================
-- Migration: 샘플 데이터 시딩 (개발/테스트용)
-- Description: 개발 및 테스트를 위한 샘플 데이터 삽입
-- Date: 2025-11-14
-- Warning: 프로덕션 환경에서는 실행하지 마세요!
-- =====================================================

-- =====================================================
-- 1. 샘플 User 데이터
-- =====================================================
INSERT INTO "user" (id, email, role, created_at) VALUES
('11111111-1111-1111-1111-111111111111', 'advertiser1@test.com', 'advertiser', NOW()),
('22222222-2222-2222-2222-222222222222', 'advertiser2@test.com', 'advertiser', NOW()),
('33333333-3333-3333-3333-333333333333', 'influencer1@test.com', 'influencer', NOW()),
('44444444-4444-4444-4444-444444444444', 'influencer2@test.com', 'influencer', NOW()),
('55555555-5555-5555-5555-555555555555', 'influencer3@test.com', 'influencer', NOW())
ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- 2. 샘플 Advertiser 데이터
-- =====================================================
INSERT INTO advertiser (user_id, name, birth_date, phone_number, business_name, address, business_phone, business_number, representative_name, created_at) VALUES
('11111111-1111-1111-1111-111111111111', '김광고', '1985-05-15', '010-1234-5678', '테스트 카페', '서울시 강남구 테헤란로 123', '02-1234-5678', '1234567890', '김대표', NOW()),
('22222222-2222-2222-2222-222222222222', '이사장', '1980-03-20', '010-2345-6789', '맛있는 레스토랑', '서울시 서초구 서초대로 456', '02-2345-6789', '2345678901', '이대표', NOW())
ON CONFLICT (user_id) DO NOTHING;

-- =====================================================
-- 3. 샘플 Influencer 데이터
-- =====================================================
INSERT INTO influencer (user_id, name, birth_date, phone_number, channel_name, channel_url, follower_count, created_at) VALUES
('33333333-3333-3333-3333-333333333333', '이인플루', '1995-08-20', '010-9876-5432', '테스트 유튜브 채널', 'https://www.youtube.com/@testchannel1', 50000, NOW()),
('44444444-4444-4444-4444-444444444444', '박리뷰어', '1998-11-10', '010-8765-4321', '맛집 인스타그램', 'https://www.instagram.com/testaccount2', 30000, NOW()),
('55555555-5555-5555-5555-555555555555', '최크리에이터', '1993-06-05', '010-7654-3210', '라이프 블로그', 'https://blog.naver.com/testblog3', 15000, NOW())
ON CONFLICT (user_id) DO NOTHING;

-- =====================================================
-- 4. 샘플 Campaign 데이터
-- =====================================================
INSERT INTO campaign (advertiser_id, title, description, quota, start_date, end_date, benefits, conditions, image_url, status, created_at) VALUES
(1, '신메뉴 파스타 체험단 모집', '새로 출시한 크림 파스타 메뉴를 체험하고 리뷰해주실 인플루언서를 모집합니다. 분위기 좋은 강남 카페에서 맛있는 파스타를 즐기세요!', 5, '2025-11-15', '2025-11-30', '크림 파스타 1인분 + 음료 1잔 무료 제공', '인스타그램 피드 1개 + 스토리 2개 업로드 필수. 해시태그 #테스트카페 #신메뉴파스타 포함', NULL, 'RECRUITING', NOW()),
(1, '크리스마스 디저트 체험단', '크리스마스 시즌 한정 디저트를 미리 체험하고 홍보해주실 분을 찾습니다. 특별한 디저트와 함께 따뜻한 겨울을 보내세요!', 3, '2025-11-20', '2025-12-05', '크리스마스 디저트 세트 무료 제공', '유튜브 쇼츠 또는 인스타그램 릴스 1개 업로드', NULL, 'RECRUITING', NOW()),
(2, '신규 오픈 레스토랑 홍보', '서초에 새로 오픈한 이탈리안 레스토랑입니다. 정성스럽게 준비한 코스 요리를 체험해보세요!', 10, '2025-11-10', '2025-11-25', '2인 코스 요리 무료 제공 (약 10만원 상당)', '블로그 리뷰 1개 + 인스타그램 피드 1개 필수. 최소 사진 5장 이상', NULL, 'RECRUITING', NOW()),
(2, '[마감] 여름 시즌 음료 체험단', '여름 한정 시그니처 음료 체험단 모집 (이미 마감되었습니다)', 8, '2025-08-01', '2025-08-15', '시그니처 음료 2잔 무료', '인스타그램 스토리 3개 업로드', NULL, 'CLOSED', NOW() - INTERVAL '3 months')
ON CONFLICT DO NOTHING;

-- =====================================================
-- 5. 샘플 Application 데이터
-- =====================================================
INSERT INTO application (campaign_id, influencer_id, application_reason, status, applied_at) VALUES
(1, 1, '파스타를 정말 좋아합니다! 제 채널 구독자들도 맛집 콘텐츠를 많이 좋아해주셔서 좋은 홍보가 될 것 같습니다.', 'APPLIED', NOW() - INTERVAL '2 days'),
(1, 2, '강남 지역 맛집 인플루언서로 활동하고 있습니다. 팔로워 분들께 추천드리고 싶어요!', 'APPLIED', NOW() - INTERVAL '1 day'),
(2, 1, '크리스마스 콘텐츠를 준비 중이어서 딱 맞는 것 같습니다. 분위기 있게 촬영하겠습니다!', 'APPLIED', NOW() - INTERVAL '3 hours'),
(3, 3, '블로그 리뷰 전문으로 활동하고 있습니다. 상세한 리뷰 작성 가능합니다.', 'APPLIED', NOW() - INTERVAL '5 hours'),
(4, 1, '여름 음료 체험에 지원했던 내역입니다.', 'SELECTED', NOW() - INTERVAL '3 months'),
(4, 2, '여름 음료 체험에 지원했던 내역입니다.', 'REJECTED', NOW() - INTERVAL '3 months')
ON CONFLICT (campaign_id, influencer_id) DO NOTHING;

-- =====================================================
-- 샘플 데이터 시딩 완료
-- =====================================================

-- 시퀀스 값 업데이트 (다음 삽입 시 ID 충돌 방지)
SELECT setval('advertiser_id_seq', (SELECT MAX(id) FROM advertiser));
SELECT setval('influencer_id_seq', (SELECT MAX(id) FROM influencer));
SELECT setval('campaign_id_seq', (SELECT MAX(id) FROM campaign));
SELECT setval('application_id_seq', (SELECT MAX(id) FROM application));
