from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download the lexicon once (cached afterward)
nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        return "POSITIVE", compound
    elif compound <= -0.05:
        return "NEGATIVE", compound
    else:
        return "NEUTRAL", compound
