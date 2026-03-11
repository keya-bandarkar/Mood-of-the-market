from transformers import pipeline
import logging
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the pipeline once when the module loads
# We use device=-1 to run on CPU, change to device=0 if you have a GPU
try:
    logger.info("Loading ProsusAI/finbert sentiment model... (this may take a moment)")
    device = 0 if torch.cuda.is_available() else -1
    sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=device)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load the model: {e}")
    sentiment_pipeline = None

def get_emoji_for_score(score: float) -> str:
    """Returns an emoji based on the aggregate score."""
    if score >= 0.2:
        return '🚀'
    elif score <= -0.2:
        return '💀'
    else:
        return '😐'

def analyze_sentiment(posts: list) -> dict:
    """
    Analyzes the sentiment of a list of reddit posts using FinBERT.
    
    Args:
        posts (list): List of dictionaries containing 'title' and 'selftext'.
        
    Returns:
        dict: A dictionary containing:
            - analyzed_posts: The original posts with 'sentiment_label' and 'sentiment_score' added.
            - summary: dict with 'positive', 'negative', 'neutral' counts.
            - overall_mood_score: A float from -1 to 1.
            - emoji: A representative emoji.
    """
    if not sentiment_pipeline:
        logger.error("Sentiment pipeline is not initialized.")
        return {"error": "Model failed to load"}

    if not posts:
        return {
            "analyzed_posts": [],
            "summary": {"positive": 0, "negative": 0, "neutral": 0},
            "overall_mood_score": 0.0,
            "emoji": "😐"
        }

    # Prepare texts by combining title and selftext
    texts = []
    for p in posts:
        # Avoid passing massive bodies of text to finbert, truncate if necessary
        content = f"{p.get('title', '')} {p.get('selftext', '')}"
        # Crude truncation to ~500 tokens. FinBERT's max length is usually 512.
        texts.append(content[:1500])

    try:
        results = sentiment_pipeline(texts, truncation=True, max_length=512)
    except Exception as e:
        logger.error(f"Error during sentiment inference: {e}")
        return {"error": str(e)}

    # Map finbert classes to our own and aggregate
    summary_counts = {"positive": 0, "negative": 0, "neutral": 0}
    total_score = 0.0
    valid_posts = 0

    for idx, (post, result) in enumerate(zip(posts, results)):
        label = result['label']  # 'positive', 'negative', 'neutral'
        confidence = result['score']
        
        post['sentiment_label'] = label
        post['sentiment_confidence'] = confidence
        
        summary_counts[label] += 1
        
        # Calculate a weighted score for this post based on upvotes (score) + confidence
        # Simple mapping: positive=1, negative=-1, neutral=0
        val = 0
        if label == "positive":
            val = 1
        elif label == "negative":
            val = -1
            
        total_score += val * confidence
        valid_posts += 1

    overall_score = 0.0
    if valid_posts > 0:
        overall_score = total_score / valid_posts

    # Ensure it's bounded
    overall_score = max(-1.0, min(1.0, overall_score))

    # Sort the analyzed posts by sentiment confidence to get the most polar ones
    # (Optional, but useful for the "Top 5 posts" requirement)
    analyzed_posts = sorted(posts, key=lambda x: x.get('score', 0), reverse=True)

    return {
        "analyzed_posts": analyzed_posts,
        "summary": summary_counts,
        "overall_mood_score": overall_score,
        "emoji": get_emoji_for_score(overall_score)
    }

if __name__ == "__main__":
    # Test
    test_posts = [
        {"title": "TSLA is going to the moon! Best stock ever", "selftext": "Earnings were incredible.", "score": 100},
        {"title": "I lost all my money on TSLA puts", "selftext": "Terrible company.", "score": 50},
        {"title": "TSLA earnings report released today", "selftext": "Revenue was exactly as expected.", "score": 10}
    ]
    res = analyze_sentiment(test_posts)
    print(res)
