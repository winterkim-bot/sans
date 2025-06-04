import os
import pandas as pd
from datetime import datetime
import sys

# 테스트를 위한 샘플 뉴스 데이터
sample_articles = [
    {
        'source': {'id': 'techcrunch', 'name': 'TechCrunch'},
        'author': '홍길동',
        'title': '인공지능 기술의 최신 동향: GPT-4의 충격적인 발전',
        'description': '최근 발표된 GPT-4는 이전 모델보다 훨씬 더 정교한 결과를 보여주고 있어 AI 업계에 큰 반향을 일으키고 있다.',
        'url': 'https://example.com/ai-news-1',
        'urlToImage': 'https://example.com/images/ai-1.jpg',
        'publishedAt': '2023-12-01T09:00:00Z',
        'content': 'GPT-4는 이전 모델보다 더 나은 성능을 보여주고 있으며, 특히 복잡한 추론과 문맥 이해에서 큰 발전을 이루었다...'
    },
    {
        'source': {'id': 'wired', 'name': 'Wired'},
        'author': '김철수',
        'title': '머신러닝 모델의 훈련 방법: 효율성 향상을 위한 새로운 접근법',
        'description': '데이터 과학자들이 머신러닝 모델의 훈련 효율성을 크게 높일 수 있는 새로운 방법을 발견했다.',
        'url': 'https://example.com/ai-news-2',
        'urlToImage': 'https://example.com/images/ai-2.jpg',
        'publishedAt': '2023-12-02T10:30:00Z',
        'content': '이 새로운 훈련 방법은 기존 방식보다 50% 더 빠르게 모델을 훈련시키며, 동시에 정확도도 향상시킨다...'
    },
    {
        'source': {'id': 'sciencedaily', 'name': 'Science Daily'},
        'author': '이영희',
        'title': '딥러닝을 활용한 의료 영상 분석의 혁신',
        'description': '연구진이 딥러닝 알고리즘을 사용하여 의료 영상에서 초기 단계의 질병을 감지하는 데 큰 성공을 거두었다.',
        'url': 'https://example.com/ai-news-3',
        'urlToImage': 'https://example.com/images/ai-3.jpg',
        'publishedAt': '2023-12-03T14:15:00Z',
        'content': '이 딥러닝 알고리즘은 방사선 전문의보다 더 높은 정확도로 초기 단계의 종양을 감지할 수 있다고 연구진은 보고했다...'
    }
]

def save_to_excel(articles, language='ko'):
    if not articles:
        print("저장할 기사가 없습니다")
        return False
    
    # 현재 날짜로 파일명 생성
    today = datetime.now().strftime('%Y%m%d')
    filename = f"ai_news_test_{today}.xlsx"
    
    try:
        # 판다스 DataFrame으로 변환
        df = pd.DataFrame(articles)
        
        # 컬럼명 출력
        print(f"데이터 컬럼: {', '.join(df.columns)}")
        
        # source 컬럼 처리
        if 'source' in df.columns:
            col_name = '출처' if language == 'ko' else 'source_name'
            df[col_name] = df['source'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
            df.drop('source', axis=1, inplace=True)
        
        # 한국어일 경우 컬럼명 변경
        if language == 'ko':
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
        print(f"엑셀 파일이 성공적으로 생성되었습니다: {filename}")
        print(f"파일 저장 위치: {os.path.abspath(filename)}")
        return True
    except Exception as e:
        print(f"Excel 저장 오류: {e}")
        return False

def main():
    print("샘플 AI 뉴스로 엑셀 파일 생성 테스트를 진행합니다...")
    
    # 언어 옵션 (기본값: 한국어)
    language = 'en' if len(sys.argv) > 1 and sys.argv[1] == 'en' else 'ko'
    
    if save_to_excel(sample_articles, language):
        print("테스트 성공! Excel 파일 생성이 제대로 작동합니다.")
    else:
        print("테스트 실패! Excel 파일 생성에 문제가 있습니다.")

if __name__ == "__main__":
    main() 