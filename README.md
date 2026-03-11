# Mood of the Market 🚀

A real-time sentiment analysis web application that tracks the mood around specific stocks and cryptocurrencies on Reddit.

## Features
- **Real-time Reddit Scraping:** Fetches the latest conversational data from popular subreddits like `r/wallstreetbets`, `r/stocks`, `r/CryptoCurrency`, and `r/investing` using Reddit's public JSON API.
- **Advanced Sentiment Analysis:** Uses HuggingFace's `ProsusAI/finbert` to perform high-accuracy sentiment classification on financial texts, giving each post a bullish, bearish, or neutral rating.
- **Dynamic Visualization:** Interactive Plotly donut chart rendering the overall sentiment distribution.
- **Premium UI:** A sleek, glassmorphic dark-mode interface built with Vanilla CSS and responsive design principles.

## Tech Stack
- **Backend:** Python, Flask, Requests
- **Machine Learning:** HuggingFace `transformers`, PyTorch (for FinBERT)
- **Frontend:** HTML, Vanilla CSS, Plotly.js

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/keya-bandarkar/Mood-of-the-market.git
cd Mood-of-the-market
```

### 2. Install dependencies
Make sure you have Python 3.8+ installed. It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python main.py
```

### 4. Use the app
Open your web browser and navigate to `http://localhost:5000`. Enter a stock ticker (e.g., TSLA, AAPL, BTC) and hit "Analyze Mood"!

## How it works
1. **Scraping**: The backend sends a request to Reddit's `/search.json` endpoint to find recent posts matching the ticker.
2. **Analysis**: The selftext (and title) of each post is fed into the FinBERT pipeline. Posts are truncated to 512 tokens to adhere to model limitations.
3. **Scoring**: A weighted algorithm determines an overall "Mood Score" between `-1.0` (Bearish) and `+1.0` (Bullish).
4. **Presentation**: The frontend dynamically renders the distribution and top 5 conversational posts for context.

## License
[MIT License](LICENSE)
