import nltk
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from googletrans import Translator
from fastapi.exceptions import HTTPException
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
app = FastAPI()

class SingleReviewRequest(BaseModel):
    review: str

class ManyReviewsRequest(BaseModel):
    reviews: List[str]

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

@app.post("/sentiment-analysis/single")
async def analyze_review(request: SingleReviewRequest):
    try:
        sentiment = await analyze_sentiment(request.review)
        return {"tonality": sentiment}
    except Exception as ex:
        HTTPException(status_code=400, detail=ex)

@app.post("/sentiment-analysis/many")
async def analyze_review(request: ManyReviewsRequest):
    sentiments_list = []
    for review in request.reviews:
        try:
            sentiment = await analyze_sentiment(review)
            sentiments_list.append(sentiment)
        except:
            sentiments_list.append(None)
    return {"tonality": sentiments_list}