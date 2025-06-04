import os
import pandas as pd
from datetime import datetime, timedelta
from newsapi import NewsApiClient

def fetch_ai_news():
    # You need to get your API key from https://newsapi.org/
    api_key = os.environ.get('NEWS_API_KEY')
    if not api_key:
        print("Please set your NEWS_API_KEY environment variable")
        print("You can get a free API key at https://newsapi.org/")
        return None
    
    # Initialize NewsAPI client
    newsapi = NewsApiClient(api_key=api_key)
    
    # Get the date for yesterday
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    
    print(f"Searching for news from {yesterday_str} to now...")
    
    try:
        # Fetch AI related news from the last day
        ai_news = newsapi.get_everything(
            q='artificial intelligence OR AI technology OR machine learning',
            language='en',
            from_param=yesterday_str,
            sort_by='publishedAt',
            page_size=100  # Maximum articles per request
        )
        
        if ai_news['status'] != 'ok':
            print(f"Error fetching news: {ai_news['status']}")
            if 'message' in ai_news:
                print(f"Message: {ai_news['message']}")
            return None
        
        print(f"Found {len(ai_news.get('articles', []))} articles")
        return ai_news['articles']
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def save_to_excel(articles, filename="ai_news.xlsx"):
    if not articles:
        print("No articles to save")
        return
    
    print(f"Processing {len(articles)} articles for Excel...")
    
    try:
        # Convert to a pandas DataFrame
        df = pd.DataFrame(articles)
        
        # Print column names for debugging
        print(f"Columns in data: {', '.join(df.columns)}")
        
        # Flatten the source column
        if 'source' in df.columns:
            df['source_name'] = df['source'].apply(lambda x: x.get('name', '') if isinstance(x, dict) else '')
            df.drop('source', axis=1, inplace=True)
        
        # Save to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Saved {len(articles)} articles to {filename}")
        print(f"File saved at: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

def main():
    print("Fetching latest AI news...")
    articles = fetch_ai_news()
    
    if articles:
        # Generate filename with current date
        today = datetime.now().strftime('%Y%m%d')
        filename = f"ai_news_{today}.xlsx"
        
        save_to_excel(articles, filename)
    else:
        print("No articles found or API error occurred")

if __name__ == "__main__":
    main() 