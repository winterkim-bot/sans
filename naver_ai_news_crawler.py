import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import random
import os
import urllib.parse

def get_naver_news(keyword, pages=3):
    """
    네이버 뉴스에서 키워드로 검색하여 뉴스 기사 정보를 수집합니다.
    
    Args:
        keyword (str): 검색할 키워드
        pages (int): 수집할 페이지 수 (기본값: 3)
        
    Returns:
        list: 뉴스 기사 정보 리스트
    """
    # 사용자 에이전트 설정 (차단 방지)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    news_list = []
    encoded_keyword = urllib.parse.quote(keyword)
    
    print(f"'{keyword}' 키워드로 네이버 뉴스 검색 시작...")
    
    for page in range(1, pages + 1):
        # 네이버 뉴스 검색 URL
        start_index = (page - 1) * 10 + 1
        url = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={encoded_keyword}&start={start_index}"
        
        print(f"페이지 {page} 크롤링 중...")
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTP 오류 체크
            
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 뉴스 기사 블록 선택 - 네이버 뉴스 검색 결과 HTML 구조 기반
            news_items = soup.select('.list_news .bx')
            
            if not news_items:
                print(f"페이지 {page}에서 뉴스를 찾을 수 없습니다. 다른 CSS 선택자 시도...")
                # 다른 CSS 선택자 시도
                news_items = soup.select("div.group_news > ul.list_news > li")
                
                if not news_items:
                    news_items = soup.select("li.bx")
                    
                if not news_items:
                    print(f"페이지 {page}에서 뉴스를 찾을 수 없습니다.")
                    # 디버깅을 위해 HTML 일부 저장
                    with open(f'debug_page_{page}.html', 'w', encoding='utf-8') as f:
                        f.write(response.text[:10000])  # 처음 10000자만 저장
                    continue
            
            print(f"페이지 {page}에서 {len(news_items)}개의 뉴스 항목 발견")
            
            for item in news_items:
                news_data = {}
                
                # 제목
                title_elem = item.select_one('a.news_tit') or item.select_one('.news_wrap .news_tit') or item.select_one('.news_area .news_tit')
                if title_elem:
                    news_data['제목'] = title_elem.text.strip()
                    news_data['링크'] = title_elem.get('href', '')
                else:
                    continue  # 제목이 없으면 건너뛰기
                
                # 언론사
                press_elem = item.select_one('.press') or item.select_one('.info_group .press')
                news_data['출처'] = press_elem.text.strip() if press_elem else '정보 없음'
                
                # 요약 내용
                summary_elem = item.select_one('.dsc_wrap') or item.select_one('.news_dsc') or item.select_one('.news_info .api_txt_lines')
                news_data['설명'] = summary_elem.text.strip() if summary_elem else '정보 없음'
                
                # 날짜/시간 정보
                date_elem = item.select_one('.info_group .info') or item.select_one('span.info')
                if date_elem:
                    news_data['발행일'] = date_elem.text.strip()
                else:
                    news_data['발행일'] = '정보 없음'
                
                # 이미지 URL 추출
                img_elem = item.select_one('img.thumb') or item.select_one('.dsc_thumb img')
                if img_elem and img_elem.has_attr('src'):
                    news_data['이미지URL'] = img_elem['src']
                else:
                    news_data['이미지URL'] = ''
                
                # 수집한 뉴스 추가
                news_list.append(news_data)
                print(f"  - '{news_data['제목']}' 수집됨")
            
            # 크롤링 딜레이 (서버 부하 방지)
            time.sleep(random.uniform(1.0, 2.0))
            
        except Exception as e:
            print(f"페이지 {page} 크롤링 중 오류 발생: {e}")
            
    print(f"총 {len(news_list)}개의 뉴스 기사를 수집했습니다.")
    return news_list

def save_to_excel(news_data, filename=None):
    """
    수집한 뉴스 데이터를 엑셀 파일로 저장합니다.
    
    Args:
        news_data (list): 뉴스 기사 정보 리스트
        filename (str, optional): 저장할 파일명. 지정하지 않으면 날짜 기반으로 생성됩니다.
    """
    if not news_data:
        print("저장할 뉴스 데이터가 없습니다.")
        return False
    
    # 파일명이 지정되지 않은 경우 현재 날짜 기반으로 생성
    if not filename:
        today = datetime.now().strftime('%Y%m%d')
        filename = f"naver_ai_news_{today}.xlsx"
    
    try:
        # DataFrame 생성
        df = pd.DataFrame(news_data)
        
        # 컬럼 출력 (디버깅용)
        if len(df) > 0:
            print(f"데이터 컬럼: {', '.join(df.columns)}")
            print(f"첫 번째 기사: {df.iloc[0]['제목']}")
        
        # 엑셀 파일로 저장
        df.to_excel(filename, index=False, engine='openpyxl')
        
        print(f"뉴스 데이터가 성공적으로 '{filename}' 파일로 저장되었습니다.")
        print(f"파일 저장 위치: {os.path.abspath(filename)}")
        return True
    except Exception as e:
        print(f"엑셀 파일 저장 중 오류 발생: {e}")
        return False

def main():
    # 검색할 키워드 목록
    keywords = ['인공지능', 'AI']
    
    # 모든 키워드에 대한 뉴스 수집
    all_news = []
    
    for keyword in keywords:
        news_data = get_naver_news(keyword, pages=2)  # 각 키워드당 2페이지씩 수집
        all_news.extend(news_data)
        
        # 중복 제거를 위해 잠시 대기
        time.sleep(1.0)
    
    # 제목 기준으로 중복 제거
    unique_titles = set()
    unique_news = []
    
    for news in all_news:
        if news['제목'] not in unique_titles:
            unique_titles.add(news['제목'])
            unique_news.append(news)
    
    print(f"중복 제거 후 총 {len(unique_news)}개의 뉴스 기사가 남았습니다.")
    
    # 엑셀 파일로 저장
    today = datetime.now().strftime('%Y%m%d')
    success = save_to_excel(unique_news, f"naver_ai_news_{today}.xlsx")
    
    if success:
        print("엑셀 파일이 성공적으로 생성되었습니다.")
    else:
        print("엑셀 파일 생성에 실패했습니다.")

if __name__ == "__main__":
    main() 