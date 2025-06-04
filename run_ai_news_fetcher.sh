#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
cd "$(dirname "$0")"

# API 키가 설정되어 있는지 확인
if [ -z "$NEWS_API_KEY" ]; then
    echo "NEWS_API_KEY 환경 변수가 설정되어 있지 않습니다."
    echo "다음 명령어로 API 키를 설정해주세요:"
    echo "export NEWS_API_KEY='your_api_key_here'"
    exit 1
fi

# 언어 선택 (기본값: 영어)
LANG_OPTION=${1:-"en"}

if [ "$LANG_OPTION" = "ko" ]; then
    echo "한국어 AI 뉴스를 가져옵니다..."
    python ai_news_fetcher_ko.py
else
    echo "영어 AI 뉴스를 가져옵니다..."
    python ai_news_fetcher.py
fi

echo "완료!" 