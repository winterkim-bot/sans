import os
import pandas as pd
from datetime import datetime, timedelta
from newsapi import NewsApiClient

def fetch_ai_news():
    # NewsAPI에서 API 키를 발급받아야 합니다 (https://newsapi.org/)
    api_key = os.environ.get('NEWS_API_KEY')
    if not api_key:
        print("NEWS_API_KEY 환경 변수를 설정해주세요")
        print("https://newsapi.org/ 에서 무료 API 키를 발급받을 수 있습니다")
        return None
    
    # NewsAPI 클라이언트 초기화
    newsapi = NewsApiClient(api_key=api_key)
    
    # 어제 날짜 계산
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    
    print(f"{yesterday_str}부터 현재까지의 뉴스를 검색합니다...")
    
    try:
        # 최근 AI 관련 뉴스 가져오기
        ai_news = newsapi.get_everything(
            q='인공지능 OR AI OR 머신러닝 OR 딥러닝',
            language='ko',  # 한국어 기사 검색
            from_param=yesterday_str,
            sort_by='publishedAt',
            page_size=100  # 최대 기사 수
        )
        
        if ai_news['status'] != 'ok':
            print(f"뉴스 가져오기 오류: {ai_news['status']}")
            if 'message' in ai_news:
                print(f"메시지: {ai_news['message']}")
            return None
        
        print(f"{len(ai_news.get('articles', []))}개의 기사를 찾았습니다")
        return ai_news['articles']
    except Exception as e:
        print(f"예외가 발생했습니다: {e}")
        return None

def save_to_excel(articles, filename="ai_news.xlsx"):
    if not articles:
        print("저장할 기사가 없습니다")
        return
    
    print(f"Excel용 {len(articles)}개의 기사를 처리하는 중...")
    
    try:
        # 판다스 DataFrame으로 변환
        df = pd.DataFrame(articles)
        
        # 디버깅용 컬럼명 출력
        print(f"데이터 컬럼: {', '.join(df.columns)}")
        
        # source 컬럼 처리
        if 'source' in df.columns:
            df['출처'] = df['source'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
            df.drop('source', axis=1, inplace=True)
        
        # 컬럼명 한글로 변경
        column_mapping = {
            'title': '제목',
            'author': '작성자',
            'publishedAt': '발행일',
            'description': '설명',
            'content': '내용',
            'url': '링크',
            'urlToImage': '이미지_링크'
        }
        
        # 존재하는 컬럼만 이름 변경
        for eng, kor in column_mapping.items():
            if eng in df.columns:
                df.rename(columns={eng: kor}, inplace=True)
        
        # Excel로 저장
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"{len(articles)}개 기사를 {filename}에 저장했습니다")
        print(f"파일 저장 위치: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Excel 저장 오류: {e}")

def main():
    print("최신 AI 뉴스를 가져오는 중...")
    articles = fetch_ai_news()
    
    if articles:
        # 현재 날짜로 파일명 생성
        today = datetime.now().strftime('%Y%m%d')
        filename = f"ai_news_ko_{today}.xlsx"
        
        save_to_excel(articles, filename)
    else:
        print("기사를 찾을 수 없거나 API 오류가 발생했습니다")

if __name__ == "__main__":
    main() 