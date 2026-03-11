from sentiment import analyze_sentiment

def test_long_input():
    long_text = "This is a very long text " * 200 # Creates a text well over 512 tokens
    
    mock_posts = [
        {"title": "Long Post 1", "selftext": long_text, "score": 100},
        {"title": "Short Post", "selftext": "TSLA is good", "score": 50}
    ]
    
    print("Testing analyze_sentiment with very long inputs...")
    result = analyze_sentiment(mock_posts)
    
    if "error" in result:
        print(f"FAILED: {result['error']}")
    else:
        print("SUCCESS: Model processed long inputs without crashing.")
        print(f"Scores -> {result['summary']}")
        print(f"Overall Mood -> {result['overall_mood_score']} {result['emoji']}")

if __name__ == "__main__":
    test_long_input()
