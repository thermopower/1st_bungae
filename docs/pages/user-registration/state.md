# 사용자 정보 등록 페이지 상태관리 설계
## (광고주 / 인플루언서 정보 등록)

## 페이지 개요

### 광고주 정보 등록
- **URL**: `/advertiser/register`
- **권한**: 로그인 사용자 (광고주 정보 미등록)
- **목적**: 광고주 정보 등록하여 체험단 생성 권한 획득

### 인플루언서 정보 등록
- **URL**: `/influencer/register`
- **권한**: 로그인 사용자 (인플루언서 정보 미등록)
- **목적**: 인플루언서 정보 등록하여 체험단 지원 권한 획득

---

## 상태관리 필요 여부
✅ **필요** - 복잡한 폼 유효성 검사, 다단계 입력, 에러 처리

---

## 상태(State) 정의

### 광고주 폼 상태
```javascript
const advertiserFormState = {
  // 공통 정보
  name: '',
  birthDate: '',
  phoneNumber: '',

  // 광고주 전용 정보
  businessName: '',
  address: {
    zipcode: '',
    basic: '',
    detail: ''
  },
  businessPhone: '',
  businessNumber: '',
  representativeName: '',

  // 유효성 검사 에러
  errors: {
    name: null,
    birthDate: null,
    phoneNumber: null,
    businessName: null,
    address: null,
    businessPhone: null,
    businessNumber: null,
    representativeName: null
  },

  // 제출 상태
  isSubmitting: false,
  serverError: null,
  isSuccess: false
}
```

### 인플루언서 폼 상태
```javascript
const influencerFormState = {
  // 공통 정보
  name: '',
  birthDate: '',
  phoneNumber: '',

  // 인플루언서 전용 정보
  channelName: '',
  channelUrl: '',
  followerCount: '',
  channelType: 'youtube', // 'youtube' | 'instagram' | 'blog' | 'other'

  // 유효성 검사 에러
  errors: {
    name: null,
    birthDate: null,
    phoneNumber: null,
    channelName: null,
    channelUrl: null,
    followerCount: null
  },

  // 제출 상태
  isSubmitting: false,
  serverError: null,
  isSuccess: false
}
```

---

## 액션(Actions)

### 1. 입력 필드 변경
```javascript
function updateField(field, value) {
  if (field.includes('.')) {
    // 중첩 필드 (예: address.zipcode)
    const [parent, child] = field.split('.');
    formState[parent][child] = value;
  } else {
    formState[field] = value;
  }

  // 에러 제거
  clearFieldError(field);

  // 실시간 검증 (선택적)
  if (shouldValidateOnChange(field)) {
    validateField(field);
  }
}
```

### 2. 주소 검색 (광고주)
```javascript
function openAddressSearch() {
  // Daum 우편번호 API 사용
  new daum.Postcode({
    oncomplete: function(data) {
      formState.address.zipcode = data.zonecode;
      formState.address.basic = data.address;

      // UI 업데이트
      document.getElementById('zipcode').value = data.zonecode;
      document.getElementById('basic-address').value = data.address;
      document.getElementById('detail-address').focus();

      // 에러 제거
      clearFieldError('address');
    }
  }).open();
}
```

### 3. 유효성 검사

#### 공통 필드 검증
```javascript
function validateCommonFields() {
  let isValid = true;

  // 이름 검증
  if (!formState.name || formState.name.length < 2) {
    formState.errors.name = '이름은 최소 2자 이상 입력해주세요.';
    isValid = false;
  } else if (!/^[가-힣a-zA-Z\s]+$/.test(formState.name)) {
    formState.errors.name = '이름은 한글 또는 영문만 입력 가능합니다.';
    isValid = false;
  }

  // 생년월일 검증
  if (!formState.birthDate) {
    formState.errors.birthDate = '생년월일을 입력해주세요.';
    isValid = false;
  } else if (!isValidDate(formState.birthDate)) {
    formState.errors.birthDate = '올바른 날짜 형식이 아닙니다. (YYYY-MM-DD)';
    isValid = false;
  } else if (!isAdult(formState.birthDate)) {
    formState.errors.birthDate = '만 19세 이상만 가입 가능합니다.';
    isValid = false;
  }

  // 휴대폰번호 검증
  if (!formState.phoneNumber) {
    formState.errors.phoneNumber = '휴대폰번호를 입력해주세요.';
    isValid = false;
  } else if (!/^010-\d{4}-\d{4}$/.test(formState.phoneNumber)) {
    formState.errors.phoneNumber = '휴대폰번호 형식이 올바르지 않습니다. (010-XXXX-XXXX)';
    isValid = false;
  }

  return isValid;
}

function isValidDate(dateString) {
  const regex = /^\d{4}-\d{2}-\d{2}$/;
  if (!regex.test(dateString)) return false;

  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date);
}

function isAdult(birthDate) {
  const today = new Date();
  const birth = new Date(birthDate);
  const age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    return age - 1 >= 19;
  }
  return age >= 19;
}
```

#### 광고주 필드 검증
```javascript
function validateAdvertiserFields() {
  let isValid = validateCommonFields();

  // 업체명 검증
  if (!formState.businessName || formState.businessName.length < 2) {
    formState.errors.businessName = '업체명을 입력해주세요.';
    isValid = false;
  }

  // 주소 검증
  if (!formState.address.zipcode || !formState.address.basic || !formState.address.detail) {
    formState.errors.address = '주소를 모두 입력해주세요.';
    isValid = false;
  }

  // 업장 전화번호 검증
  if (!formState.businessPhone) {
    formState.errors.businessPhone = '업장 전화번호를 입력해주세요.';
    isValid = false;
  } else if (!/^\d{2,3}-\d{3,4}-\d{4}$/.test(formState.businessPhone)) {
    formState.errors.businessPhone = '전화번호 형식이 올바르지 않습니다.';
    isValid = false;
  }

  // 사업자등록번호 검증
  if (!formState.businessNumber) {
    formState.errors.businessNumber = '사업자등록번호를 입력해주세요.';
    isValid = false;
  } else if (!/^\d{3}-\d{2}-\d{5}$/.test(formState.businessNumber)) {
    formState.errors.businessNumber = '사업자등록번호 형식이 올바르지 않습니다. (XXX-XX-XXXXX)';
    isValid = false;
  }

  // 대표자명 검증
  if (!formState.representativeName || formState.representativeName.length < 2) {
    formState.errors.representativeName = '대표자명을 입력해주세요.';
    isValid = false;
  }

  renderErrors();
  return isValid;
}
```

#### 인플루언서 필드 검증
```javascript
function validateInfluencerFields() {
  let isValid = validateCommonFields();

  // 채널명 검증
  if (!formState.channelName || formState.channelName.length < 2) {
    formState.errors.channelName = '채널명을 입력해주세요.';
    isValid = false;
  }

  // 채널 URL 검증
  if (!formState.channelUrl) {
    formState.errors.channelUrl = '채널 링크를 입력해주세요.';
    isValid = false;
  } else if (!isValidUrl(formState.channelUrl)) {
    formState.errors.channelUrl = '올바른 URL 형식이 아닙니다. (http:// 또는 https://)';
    isValid = false;
  }

  // 팔로워 수 검증
  if (!formState.followerCount) {
    formState.errors.followerCount = '팔로워 수를 입력해주세요.';
    isValid = false;
  } else if (!/^\d+$/.test(formState.followerCount) || parseInt(formState.followerCount) < 0) {
    formState.errors.followerCount = '팔로워 수는 0 이상의 숫자여야 합니다.';
    isValid = false;
  }

  renderErrors();
  return isValid;
}

function isValidUrl(url) {
  try {
    new URL(url);
    return url.startsWith('http://') || url.startsWith('https://');
  } catch {
    return false;
  }
}
```

### 4. 폼 제출
```javascript
async function submitForm(e) {
  e.preventDefault();

  // 유효성 검사
  const isValid = isAdvertiser ? validateAdvertiserFields() : validateInfluencerFields();
  if (!isValid) return;

  formState.isSubmitting = true;
  renderSubmitButton();

  try {
    const endpoint = isAdvertiser ? '/advertiser/register' : '/influencer/register';
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify(formState)
    });

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 409) {
        // 중복 에러 처리
        if (data.field === 'business_number') {
          formState.errors.businessNumber = '이미 등록된 사업자등록번호입니다.';
          renderFieldError('businessNumber');
        } else if (data.field === 'phone_number') {
          formState.errors.phoneNumber = '이미 사용 중인 휴대폰번호입니다.';
          renderFieldError('phoneNumber');
        } else if (data.field === 'channel_url') {
          formState.errors.channelUrl = '이미 등록된 채널 링크입니다.';
          renderFieldError('channelUrl');
        }
      } else {
        formState.serverError = data.message || '정보 등록에 실패했습니다.';
        renderServerError();
      }
      return;
    }

    // 등록 성공
    formState.isSuccess = true;
    showSuccessMessage();

    // 리다이렉트
    setTimeout(() => {
      window.location.href = data.redirect_url || (isAdvertiser ? '/advertiser/dashboard' : '/');
    }, 2000);

  } catch (error) {
    formState.serverError = '네트워크 오류가 발생했습니다.';
    renderServerError();
  } finally {
    formState.isSubmitting = false;
    renderSubmitButton();
  }
}
```

---

## 렌더링 및 UI 헬퍼

### 1. 전화번호 자동 포맷팅
```javascript
function formatPhoneNumber(input) {
  const value = input.value.replace(/\D/g, '');

  let formatted = '';
  if (value.length <= 3) {
    formatted = value;
  } else if (value.length <= 7) {
    formatted = value.slice(0, 3) + '-' + value.slice(3);
  } else {
    formatted = value.slice(0, 3) + '-' + value.slice(3, 7) + '-' + value.slice(7, 11);
  }

  input.value = formatted;
  formState.phoneNumber = formatted;
}

document.getElementById('phoneNumber').addEventListener('input', function() {
  formatPhoneNumber(this);
});
```

### 2. 사업자등록번호 자동 포맷팅 (광고주)
```javascript
function formatBusinessNumber(input) {
  const value = input.value.replace(/\D/g, '');

  let formatted = '';
  if (value.length <= 3) {
    formatted = value;
  } else if (value.length <= 5) {
    formatted = value.slice(0, 3) + '-' + value.slice(3);
  } else {
    formatted = value.slice(0, 3) + '-' + value.slice(3, 5) + '-' + value.slice(5, 10);
  }

  input.value = formatted;
  formState.businessNumber = formatted;
}
```

### 3. 숫자만 입력 허용 (팔로워 수)
```javascript
document.getElementById('followerCount').addEventListener('input', function() {
  this.value = this.value.replace(/\D/g, '');
  formState.followerCount = this.value;
});
```

---

## 접근성 및 사용성

### 1. 필수 필드 표시
```html
<label for="name" class="form-label">
  이름 <span class="text-danger" aria-label="필수">*</span>
</label>
```

### 2. Placeholder 가이드
```html
<input
  type="text"
  id="phoneNumber"
  placeholder="010-1234-5678"
  aria-describedby="phoneNumber-help"
>
<small id="phoneNumber-help" class="form-text text-muted">
  하이픈(-)을 포함하여 입력해주세요.
</small>
```

### 3. 툴팁 안내
```html
<label for="businessNumber" class="form-label">
  사업자등록번호
  <i class="bi bi-question-circle" data-bs-toggle="tooltip" title="사업자등록증에 표시된 10자리 번호입니다."></i>
</label>
```

---

## 테스트 고려사항

### 1. 경계값 테스트
- 이름 1자 (에러)
- 이름 2자 (성공)
- 만 18세 (에러)
- 만 19세 (성공)
- 팔로워 수 -1 (에러)
- 팔로워 수 0 (성공)

### 2. 형식 검증 테스트
- 잘못된 이메일 형식
- 잘못된 전화번호 형식
- 잘못된 URL 형식
- 잘못된 날짜 형식

---

## 향후 확장 가능성

### Phase 2 기능
- **프로필 사진 업로드**: Supabase Storage 연동
- **사업자등록번호 진위확인**: 국세청 API 연동
- **채널 인증**: YouTube API, Instagram API 연동하여 팔로워 수 자동 조회
- **다중 채널 등록**: 여러 SNS 채널 등록 가능
