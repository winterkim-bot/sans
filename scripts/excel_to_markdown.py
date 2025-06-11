#!/usr/bin/env python3
"""
Excel 파일을 읽어서 Jekyll 블로그 포스트용 Markdown 파일로 변환하는 스크립트
"""

import pandas as pd
import os
from datetime import datetime
import re
import yaml

def clean_filename(title):
    """제목을 파일명으로 사용할 수 있도록 정리"""
    # 특수문자 제거 및 공백을 하이픈으로 변경
    cleaned = re.sub(r'[^\w\s-]', '', title)
    cleaned = re.sub(r'[-\s]+', '-', cleaned)
    return cleaned.lower().strip('-')

def create_post_content(row, date_str):
    """블로그 포스트 내용 생성"""
    # YAML front matter
    front_matter = {
        'layout': 'post',
        'title': str(row.get('제목', row.get('title', 'AI News'))),
        'date': date_str,
        'categories': ['ai', 'news'],
        'tags': ['google', 'crawling', 'ai'],
        'author': 'AI News Crawler'
    }
    
    # 링크가 있다면 추가
    if '링크' in row and pd.notna(row['링크']):
        front_matter['source_url'] = str(row['링크'])
    elif 'url' in row and pd.notna(row['url']):
        front_matter['source_url'] = str(row['url'])
    
    # YAML 헤더 생성
    yaml_header = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    
    # 본문 내용
    content = f"---\n{yaml_header}---\n\n"
    
    # 제목
    content += f"# {front_matter['title']}\n\n"
    
    # 내용 추가
    if '내용' in row and pd.notna(row['내용']):
        content += f"{row['내용']}\n\n"
    elif 'content' in row and pd.notna(row['content']):
        content += f"{row['content']}\n\n"
    elif '요약' in row and pd.notna(row['요약']):
        content += f"{row['요약']}\n\n"
    
    # 원본 링크
    if front_matter.get('source_url'):
        content += f"[원문 보기]({front_matter['source_url']})\n\n"
    
    # 자동 생성 표시
    content += "---\n*이 포스트는 자동으로 생성되었습니다.*\n"
    
    return content

def excel_to_markdown(excel_file, output_dir='_posts'):
    """Excel 파일을 Markdown 포스트로 변환"""
    try:
        # Excel 파일 읽기
        df = pd.read_excel(excel_file)
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 현재 날짜
        current_date = datetime.now()
        date_str = current_date.strftime('%Y-%m-%d')
        
        created_files = []
        
        for index, row in df.iterrows():
            # 제목 추출
            title = str(row.get('제목', row.get('title', f'AI News {index + 1}')))
            
            # 파일명 생성
            clean_title = clean_filename(title)
            filename = f"{date_str}-{clean_title}.md"
            filepath = os.path.join(output_dir, filename)
            
            # 중복 파일명 처리
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                filename = f"{date_str}-{clean_title}-{counter}.md"
                filepath = os.path.join(output_dir, filename)
                counter += 1
            
            # 포스트 내용 생성
            post_content = create_post_content(row, current_date.strftime('%Y-%m-%d %H:%M:%S +0900'))
            
            # 파일 저장
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(post_content)
            
            created_files.append(filepath)
            print(f"Created: {filepath}")
        
        return created_files
        
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return []

if __name__ == "__main__":
    # Excel 파일 경로
    excel_file = "google_ai_news_20250518.xlsx"
    
    if os.path.exists(excel_file):
        print(f"Processing {excel_file}...")
        created_files = excel_to_markdown(excel_file)
        print(f"\nSuccessfully created {len(created_files)} blog posts!")
        
        for file in created_files:
            print(f"  - {file}")
    else:
        print(f"Excel file not found: {excel_file}") 