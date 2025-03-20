import nltk
from googletrans import Translator
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

async def analyze_sentiment(text: str):
    try:
        translator = Translator()
        translated_text = await translator.translate(text, src='ru', dest='en')
        translated_text = translated_text.text
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(translated_text)

        if scores['compound'] >= 0.05:
            return "Positive"
        elif scores['compound'] <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    except:
        raise Exception("Error during sentiment analysis")