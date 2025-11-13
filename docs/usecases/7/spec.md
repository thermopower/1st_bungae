# UC-007: 인플루언서 선정

## 1. 유스케이스 정보

| 항목 | 내용 |
|------|------|
| **유스케이스 ID** | UC-007 |
| **유스케이스 이름** | 인플루언서 선정 |
| **액터** | 광고주 (본인 체험단, 모집 종료 후) |
| **우선순위** | 높음 |
| **관련 기능** | 체험단 관리 |

## 2. 사전조건 (Preconditions)

- 사용자가 로그인 상태
- User.role이 'advertiser'
- 광고주가 생성한 체험단 존재
- Campaign.status가 'CLOSED'
- 지원자가 1명 이상 존재

## 3. 사후조건 (Postconditions)

### 성공 시
- 선정된 Application의 status가 'SELECTED'로 업데이트
- 미선정된 Application의 status가 'REJECTED'로 업데이트
- Campaign.status가 'SELECTED'로 업데이트
- 체험단 관리 페이지로 리다이렉트

### 실패 시
- 에러 메시지 표시
- 인플루언서 선정 페이지 유지

## 4. 주요 플로우 (Main Flow)

1. 광고주가 체험단 관리 페이지에서 "인플루언서 선정" 버튼 클릭
2. 인플루언서 선정 페이지(`/advertiser/campaign/<campaign_id>/select`)로 이동
3. **시스템**: 지원자 목록 조회
   - Application 테이블에서 campaign_id로 조회
   - JOIN Influencer, User 테이블 (인플루언서 정보, 사용자 정보)
   - 정렬: applied_at ASC (선착순)
4. **시스템**: 각 지원자 정보 표시
   - 인플루언서 이름
   - SNS 채널명, 채널링크
   - 팔로워 수
   - 지원 사유
   - 지원 일시
   - 선정 체크박스
5. 광고주가 선정할 인플루언서 체크박스 선택 (최대 모집인원만큼)
6. "선정하기" 버튼 클릭
7. **시스템**: 로그인 여부 검증
8. **시스템**: 광고주 권한 검증
9. **시스템**: 체험단 소유권 검증
10. **시스템**: 모집 종료 여부 검증
    - Campaign.status = 'RECRUITING': "모집을 먼저 종료해주세요" + 플로우 중단
11. **시스템**: 선정 완료 여부 검증
    - Campaign.status = 'SELECTED': "이미 인플루언서 선정이 완료되었습니다" + 플로우 중단
12. **시스템**: 선정 인원 검증
    - 선택 없음: "선정할 인플루언서를 선택해주세요" + 플로우 중단
    - 모집인원 초과: "모집인원을 초과했습니다 (최대 {quota}명)" + 플로우 중단
13. **시스템**: 선정된 Application ID 검증
    - 각 Application ID가 해당 Campaign의 지원자인지 확인
14. **시스템**: 트랜잭션 시작
15. **시스템**: Application 업데이트
    - 선정된 Application: status = 'SELECTED'
    - 미선정된 Application: status = 'REJECTED'
16. **시스템**: Campaign 업데이트
    - status = 'SELECTED'
17. **시스템**: 트랜잭션 커밋
18. **시스템**: 체험단 관리 페이지(`/advertiser/campaign/<campaign_id>`)로 리다이렉트
19. **시스템**: "인플루언서 선정이 완료되었습니다" 메시지 표시

## 5. 대체 플로우 (Alternative Flows)

### 5.1 미로그인 상태
- **시점**: 7단계 (로그인 검증)
- **조건**: 세션에 user_id 없음
- **처리**:
  - 로그인 페이지로 리다이렉트

### 5.2 광고주 권한 없음
- **시점**: 8단계 (광고주 권한 검증)
- **조건**: Advertiser 테이블에 user_id로 레코드 없음
- **처리**:
  - 403 Forbidden 페이지 표시

### 5.3 체험단 소유권 없음
- **시점**: 9단계 (소유권 검증)
- **조건**: Campaign.advertiser_id ≠ 현재 Advertiser ID
- **처리**:
  - 403 Forbidden 페이지 표시

### 5.4 모집 중인 체험단
- **시점**: 10단계 (모집 종료 여부 검증)
- **조건**: Campaign.status = 'RECRUITING'
- **처리**:
  - "모집을 먼저 종료해주세요" 메시지 표시
  - 플로우 중단

### 5.5 이미 선정 완료
- **시점**: 11단계 (선정 완료 여부 검증)
- **조건**: Campaign.status = 'SELECTED'
- **처리**:
  - "이미 인플루언서 선정이 완료되었습니다" 메시지 표시
  - 플로우 중단

### 5.6 선정 인원 초과
- **시점**: 12단계 (선정 인원 검증)
- **조건**: 선택된 인플루언서 수 > quota
- **처리**:
  - "모집인원을 초과했습니다 (최대 {quota}명)" 메시지 표시
  - 플로우 중단

### 5.7 선정 없음
- **시점**: 12단계 (선정 인원 검증)
- **조건**: 선택된 인플루언서 수 = 0
- **처리**:
  - "선정할 인플루언서를 선택해주세요" 메시지 표시
  - 플로우 중단

### 5.8 지원자 없음
- **시점**: 3단계 (지원자 목록 조회)
- **조건**: Application 레코드 없음
- **처리**:
  - "지원자가 없습니다" 메시지 표시
  - 선정 불가

## 6. 예외 플로우 (Exception Flows)

### 6.1 트랜잭션 롤백
- **조건**: Application 또는 Campaign 업데이트 실패
- **처리**:
  - 트랜잭션 롤백
  - "일시적인 오류가 발생했습니다. 다시 시도해주세요" 메시지 표시
  - 플로우 중단

### 6.2 동시 선정 요청
- **조건**: 다른 세션에서 동일 체험단을 동시에 선정
- **처리**:
  - 트랜잭션 격리 수준 설정 (SERIALIZABLE 또는 SELECT FOR UPDATE)
  - 재시도 로직
  - "이미 처리되었습니다" 메시지 표시

## 7. 비즈니스 규칙 (Business Rules)

### BR-001: 모집 종료 후에만 선정 가능
- Campaign.status가 'CLOSED'일 때만 선정 가능
- 'RECRUITING' 상태에서는 선정 불가

### BR-002: 선정 완료 후 재선정 불가 (Phase 1)
- Campaign.status가 'SELECTED'이면 재선정 불가
- Phase 2에서 재선정 기능 추가 검토

### BR-003: 모집 인원 이내 선정
- 선정 인원 ≤ quota
- 애플리케이션 레벨에서 검증

### BR-004: 트랜잭션 원자성
- Application 업데이트와 Campaign 업데이트는 트랜잭션으로 묶어 원자성 보장
- 하나라도 실패 시 전체 롤백

### BR-005: 선정/미선정 상태 일괄 처리
- 선정된 Application: SELECTED
- 미선정된 Application: REJECTED
- 동시에 처리

## 8. UI/UX 요구사항

### 지원자 목록
- 각 지원자별로 카드 형식 표시
- 체크박스로 선정/미선정 선택
- 선정 가능 인원 표시 (예: "5명 중 3명 선정")

### 버튼
- "선정하기" 버튼 (Primary)
  - 조건: Campaign.status = 'CLOSED'일 때만 표시
- "취소" 버튼 (Secondary) → 체험단 관리 페이지로 이동

### 메시지
- 성공: "인플루언서 선정이 완료되었습니다"
- 에러:
  - "모집을 먼저 종료해주세요"
  - "이미 인플루언서 선정이 완료되었습니다"
  - "모집인원을 초과했습니다 (최대 {quota}명)"
  - "선정할 인플루언서를 선택해주세요"
  - "지원자가 없습니다"

## 9. 데이터 모델

### 입력 데이터
```json
{
  "campaign_id": 1,
  "selected_application_ids": [1, 3, 5]
}
```

### 출력 데이터 (성공 시)
```json
{
  "campaign_id": 1,
  "campaign_status": "SELECTED",
  "selected_count": 3,
  "rejected_count": 2
}
```

## 10. 시퀀스 다이어그램

```
광고주 -> 체험단 관리 페이지: "인플루언서 선정" 클릭
체험단 관리 페이지 -> 선정 페이지: 이동
선정 페이지 -> DB (Application): 지원자 목록 조회 (JOIN Influencer, User)
DB (Application) --> 선정 페이지: 지원자 정보 반환
선정 페이지 -> 광고주: 지원자 목록 표시
광고주 -> 선정 페이지: 인플루언서 선택 및 "선정하기" 클릭
선정 페이지 -> AuthService: 로그인 검증
AuthService --> 선정 페이지: 검증 성공
선정 페이지 -> DB (Campaign): 소유권, 상태 검증
DB (Campaign) --> 선정 페이지: 검증 성공
선정 페이지 -> 선정 페이지: 선정 인원 검증
선정 페이지 -> DB: 트랜잭션 시작
선정 페이지 -> DB (Application): 선정된 Application 업데이트 (status=SELECTED)
DB (Application) --> 선정 페이지: 업데이트 완료
선정 페이지 -> DB (Application): 미선정된 Application 업데이트 (status=REJECTED)
DB (Application) --> 선정 페이지: 업데이트 완료
선정 페이지 -> DB (Campaign): Campaign 업데이트 (status=SELECTED)
DB (Campaign) --> 선정 페이지: 업데이트 완료
선정 페이지 -> DB: 트랜잭션 커밋
DB --> 선정 페이지: 커밋 완료
선정 페이지 -> 광고주: 체험단 관리 페이지로 리다이렉트
```

## 11. 테스트 시나리오

### 11.1 정상 선정 (정원 이내)
- **Given**: 모집 종료된 체험단 (지원자 5명, quota 3명)
- **When**: 3명 선택 후 "선정하기" 클릭
- **Then**: 3명 SELECTED, 2명 REJECTED, Campaign.status = 'SELECTED'

### 11.2 모집인원 초과
- **Given**: 모집 종료된 체험단 (quota 3명)
- **When**: 4명 선택 후 "선정하기" 클릭
- **Then**: "모집인원을 초과했습니다 (최대 3명)" 에러 메시지

### 11.3 선정 없음
- **Given**: 모집 종료된 체험단
- **When**: 아무도 선택하지 않고 "선정하기" 클릭
- **Then**: "선정할 인플루언서를 선택해주세요" 에러 메시지

### 11.4 모집 중인 체험단
- **Given**: 모집 중인 체험단 (status = 'RECRUITING')
- **When**: 인플루언서 선정 시도
- **Then**: "모집을 먼저 종료해주세요" 에러 메시지

### 11.5 이미 선정 완료
- **Given**: 이미 선정이 완료된 체험단 (status = 'SELECTED')
- **When**: 인플루언서 선정 시도
- **Then**: "이미 인플루언서 선정이 완료되었습니다" 에러 메시지

### 11.6 지원자 없음
- **Given**: 모집 종료되었으나 지원자가 없는 체험단
- **When**: 선정 페이지 접근
- **Then**: "지원자가 없습니다" 메시지 표시

## 12. 참고 문서

- `docs/userflow.md`: 인플루언서 선정 플로우 (6.4)
- `docs/prd.md`: 인플루언서 선정 기능 요구사항 (6.3.6)
- `docs/database.md`: Application 테이블 스키마 (3.5)
