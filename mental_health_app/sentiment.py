from transformers import pipeline

# Load MentalRoBERTa for sentiment analysis
sentiment_analyzer = pipeline("text-classification", model="mental/mental-roberta-base")

def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']
