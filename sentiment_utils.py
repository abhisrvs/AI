from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def filter_by_sentiment(tweet_score_list, desired_sentiment="positive"):
    return [(tweet, score) for tweet, score in tweet_score_list
            if analyze_sentiment(tweet) == desired_sentiment]
