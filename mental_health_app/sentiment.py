from transformers import pipeline

# Use the default sentiment model (works on Streamlit Cloud)
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']
