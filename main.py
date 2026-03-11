from flask import Flask, render_template, request, jsonify
from reddit_scraper import search_reddit_posts
from sentiment import analyze_sentiment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    ticker = request.form.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400
        
    ticker = ticker.upper().strip()
    logger.info(f"Analyzing ticker: {ticker}")
    
    # 1. Fetch posts from reddit
    posts = search_reddit_posts(ticker, limit=10)
    
    if not posts:
        return jsonify({"error": f"No recent posts found for {ticker}. Try another ticker."}), 404
        
    # 2. Analyze sentiment
    try:
        analysis_result = analyze_sentiment(posts)
        if "error" in analysis_result:
             return jsonify({"error": analysis_result["error"]}), 500
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        return jsonify({"error": "Failed to analyze sentiment."}), 500
        
    # 3. Format response
    # Only keep the top 5 most engaged posts for display
    # (Assuming analyze_sentiment sorts them by score)
    top_posts = analysis_result.get("analyzed_posts", [])[:5]
    
    response_data = {
        "ticker": ticker,
        "mood_score": round(analysis_result.get("overall_mood_score", 0), 2),
        "emoji": analysis_result.get("emoji", "😐"),
        "summary": analysis_result.get("summary", {"positive":0,"neutral":0,"negative":0}),
        "top_posts": top_posts,
        "total_posts_analyzed": len(analysis_result.get("analyzed_posts", []))
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
