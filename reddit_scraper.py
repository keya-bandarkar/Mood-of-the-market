import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUBREDDITS = ['wallstreetbets', 'stocks', 'CryptoCurrency', 'investing']

def search_reddit_posts(ticker: str, limit: int = 10) -> list:
    '''
    Searches Reddit for recent posts about a specific ticker across multiple subreddits.
    
    Args:
        ticker (str): The stock or crypto ticker to search for (e.g., TSLA, BTC).
        limit (int): Number of posts to fetch per subreddit.
        
    Returns:
        list: A list of dictionaries containing post data.
    '''
    posts = []
    
    # Use a custom user agent to avoid being blocked by Reddit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MoodOfTheMarketBot/1.0'
    }
    
    for subreddit in SUBREDDITS:
        url = f'https://www.reddit.com/r/{subreddit}/search.json'
        params = {
            'q': ticker,
            'sort': 'new',
            'limit': limit,
            'restrict_sr': 'on' # Only search within this subreddit
        }
        
        try:
            logger.info(f"Fetching posts from r/{subreddit} for ticker {ticker}...")
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                children = data.get('data', {}).get('children', [])
                
                for child in children:
                    post_data = child.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    score = post_data.get('score', 0)
                    url_path = post_data.get('permalink', '')
                    
                    # Only include posts that have some content in title or selftext
                    if title or selftext:
                        posts.append({
                            'subreddit': subreddit,
                            'title': title,
                            'selftext': selftext,
                            'score': score,
                            'url': f"https://www.reddit.com{url_path}"
                        })
            elif response.status_code == 429:
                logger.warning(f"Rate limited on r/{subreddit}. Skipping...")
            else:
                logger.warning(f"Failed to fetch from r/{subreddit}. Status code: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching from r/{subreddit}: {str(e)}")
            
        # Be nice to Reddit's API
        time.sleep(1.5)
        
    logger.info(f"Found {len(posts)} total posts for {ticker}.")
    return posts

if __name__ == '__main__':
    # Test the function
    print("Testing reddit scraper with 'TSLA'")
    posts = search_reddit_posts('TSLA', limit=2)
    for p in posts:
        print(f"[{p['subreddit']}] {p['title'][:50]}...")
