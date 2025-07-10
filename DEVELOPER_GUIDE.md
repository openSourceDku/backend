# DEVELOPER GUIDE

## 1. 프로젝트 개요
- 학원(교육기관) 관리에 필요한 학생, 교사, 관리자, 수업, 비품 등 다양한 정보를 효율적으로 관리하는 Django 기반 백엔드 시스템입니다.

## 2. 폴더/파일 구조
- 주요 디렉토리 및 파일 역할을 간단히 설명합니다.
- 예시:
```
backend/
  ├─ apps/
  │   ├─ accounts/   # 계정/인증 관련
  │   ├─ students/   # 학생 관리
  │   ├─ teachers/   # 교사/수업/공지
  │   ├─ classes/    # 수업/스케줄
  │   ├─ managers/   # 관리자 통합 관리
  │   └─ fixtures/   # 비품 관리
  ├─ manage.py       # Django 관리 명령어
  ├─ requirements.txt# 의존성 목록
  └─ ...
```

## 3. 개발 환경 세팅
- Python 3.x, Django, Django REST Framework 필요
- 의존성 설치:
  ```bash
  pip install -r requirements.txt
  ```
- DB: SQLite3 (기본)
- 환경 변수(.env 등) 설정 방법(필요시)

## 4. 서버 실행 방법
```bash
python manage.py migrate   # DB 마이그레이션
python manage.py runserver # 개발 서버 실행
```

## 5. API 명세
- 모든 엔드포인트는 `/api/`로 시작
- 인증: JWT(SimpleJWT) 기반
- 상세 명세는 `API_명세서.md` 참고

## 6. 코드 컨벤션/커밋 규칙
- 네이밍, 들여쓰기, 주석 등 Python/Django 스타일 권장
- 커밋 메시지: 기능/수정/버그 등 목적 명확히 (예: feat: 학생 등록 기능 추가)
- 브랜치 전략: 기능별 브랜치, 완료 후 main/develop에 merge

## 7. 테스트
- 단위/통합 테스트 코드 작성 권장
- 예시 실행:
  ```bash
  python manage.py test
  ```

## 8. 배포
- 운영/개발 환경 분리(설정 파일, 환경 변수 등)
- 배포 절차(서버 환경에 맞게 추가)

## 9. 기여 가이드
- PR, 이슈, 코드리뷰 등 협업 규칙
- 문서화/주석 적극 활용

---

자세한 API 명세는 `API_명세서.md`를 참고하세요. 