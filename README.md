# 🤖 AI News Blog 자동화 시스템

구글에서 크롤링한 AI 뉴스를 자동으로 GitHub Pages 블로그에 업로드하는 시스템입니다.

## 🌐 블로그 주소
[https://winterkim-bot.github.io/sans](https://winterkim-bot.github.io/sans)

## ✨ 주요 기능

- 📊 Excel 파일을 Jekyll 블로그 포스트로 자동 변환
- 🚀 GitHub Pages 자동 배포
- 📧 Gmail을 통한 진행 상황 알림
- ⏰ 스케줄링된 자동 업데이트
- 🔄 GitHub Actions 기반 CI/CD

## 📋 마일스톤

### ✅ Milestone 1: 프로젝트 기반 구조 설정
- GitHub Pages 블로그 설정 (Jekyll)
- 프로젝트 디렉토리 구조 생성
- 기본 블로그 템플릿 설정

### ✅ Milestone 2: 데이터 처리 시스템 구축
- Excel 파일을 읽어서 Markdown으로 변환하는 Python 스크립트
- 뉴스 데이터를 블로그 포스트 형식으로 변환

### ✅ Milestone 3: Gmail 연동 시스템
- Gmail SMTP 설정
- 이메일 발송 기능 구현
- 진행 상황 알림 시스템

### ✅ Milestone 4: 자동화 시스템
- GitHub Actions를 통한 자동 배포
- 크롤링 → 변환 → 업로드 → 이메일 알림 파이프라인

### ✅ Milestone 5: 테스트 및 최적화
- 전체 시스템 테스트
- 에러 핸들링 및 로깅
- 최종 배포

## 🚀 사용법

### 1. 로컬에서 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# Excel 파일을 Markdown으로 변환
cd scripts
python main_automation.py process

# Git에 푸시
python main_automation.py push

# 전체 자동화 실행
python main_automation.py
```

### 2. Gmail 설정

1. `scripts/gmail_notifier.py`를 실행하여 설정 템플릿 생성
2. `email_config.json.template`을 `email_config.json`으로 복사
3. Gmail 앱 비밀번호 설정:
   - Gmail → 설정 → 보안 → 2단계 인증 활성화
   - 앱 비밀번호 생성
   - `email_config.json`에 이메일과 앱 비밀번호 입력

### 3. GitHub Secrets 설정

GitHub 저장소 → Settings → Secrets and variables → Actions에서 다음 설정:

- `GMAIL_EMAIL`: Gmail 주소
- `GMAIL_APP_PASSWORD`: Gmail 앱 비밀번호

## 📁 프로젝트 구조

```
.
├── _config.yml              # Jekyll 설정
├── index.md                 # 블로그 메인 페이지
├── Gemfile                  # Ruby 의존성
├── requirements.txt         # Python 의존성
├── _posts/                  # 블로그 포스트 (자동 생성)
├── scripts/
│   ├── excel_to_markdown.py # Excel → Markdown 변환
│   ├── gmail_notifier.py    # Gmail 알림 시스템
│   └── main_automation.py   # 메인 자동화 스크립트
├── .github/workflows/
│   └── auto-blog-update.yml # GitHub Actions 워크플로우
└── *.xlsx                   # 크롤링된 뉴스 데이터
```

## 🔄 자동화 프로세스

1. **데이터 수집**: Excel 파일에 크롤링된 뉴스 데이터 저장
2. **데이터 변환**: Python 스크립트로 Markdown 포스트 생성
3. **Git 업로드**: 변경사항을 GitHub에 자동 커밋/푸시
4. **블로그 배포**: GitHub Pages에서 Jekyll 빌드 및 배포
5. **알림 발송**: Gmail로 진행 상황 알림

## 📧 알림 시스템

각 마일스톤마다 다음 이메일 주소로 알림 발송:
- 본인 Gmail 계정
- iysin0102@gmail.com

알림 내용:
- 🚀 프로세스 시작
- ⚡ 진행 상황
- ✅ 완료 알림
- ❌ 오류 알림

## 🛠️ 기술 스택

- **Frontend**: Jekyll, GitHub Pages
- **Backend**: Python
- **데이터 처리**: pandas, openpyxl
- **CI/CD**: GitHub Actions
- **알림**: Gmail SMTP
- **버전 관리**: Git, GitHub

## 📝 라이선스

MIT License 