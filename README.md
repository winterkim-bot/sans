# AI 뉴스 자동 수집 프로그램

이 프로그램은 AI 관련 뉴스를 자동으로 수집하여 Excel 파일로 저장해 주는 도구입니다.

## 기능

- AI 관련 뉴스 기사를 자동으로 수집
- 수집된 뉴스를 Excel 파일로 저장
- 다양한 정보 포함: 제목, 링크, 출처, 설명, 발행일 등
- 여러 검색 키워드 지원 (인공지능, AI, 머신러닝 등)
- 영어 및 한국어 뉴스 지원

## 설치 방법

1. 필요한 라이브러리 설치:

```bash
pip install -r requirements.txt
```

## 사용 방법

### NewsAPI를 사용한 뉴스 수집

1. [NewsAPI](https://newsapi.org)에서 API 키를 얻으세요.
2. 환경 변수로 API 키를 설정하세요:

```bash
export NEWS_API_KEY="your_api_key_here"
```

3. 스크립트 실행:

```bash
# 영어 뉴스 수집
python ai_news_fetcher.py

# 한국어 뉴스 수집
python ai_news_fetcher_ko.py

# 또는 쉘 스크립트 실행
bash run_ai_news_fetcher.sh
```

### 구글 뉴스 크롤링

API 키 없이도 구글 뉴스에서 AI 관련 기사를 크롤링할 수 있습니다:

```bash
python google_ai_news_crawler.py
```

이 스크립트는 '인공지능'과 'AI' 키워드로 구글 뉴스를 검색하고 결과를 Excel 파일로 저장합니다.

## Excel 파일 내용

생성된 Excel 파일은 다음 정보를 포함합니다:

- 제목: 뉴스 기사 제목
- 링크: 원본 기사 URL
- 출처: 뉴스 소스/언론사
- 설명: 기사 요약 내용
- 발행일: 기사 발행 일자
- 이미지URL: 기사 관련 이미지 URL (해당하는 경우)

## 문제 해결

- NewsAPI 사용 시 API 키가 올바르게 설정되었는지 확인하세요.
- 인터넷 연결이 안정적인지 확인하세요.
- 크롤링 동작이 원활하지 않을 경우, 해당 웹사이트의 HTML 구조가 변경되었을 수 있습니다.

## 참고 사항

* 생성된 Excel 파일은 현재 디렉토리에 저장됩니다.
* 파일명에는 현재 날짜가 포함됩니다 (예: `ai_news_20230101.xlsx`, `google_ai_news_20230101.xlsx`).
* 웹 크롤링은 해당 웹사이트의 이용약관을 준수해야 합니다. 