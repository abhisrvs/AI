import pandas as pd
import os
import re
from collections import Counter

def load_public_tweets():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'public_tweets.csv')
    columns = ['sentiment', 'id', 'date', 'query', 'user', 'text']
    df = pd.read_csv(file_path, encoding='ISO-8859-1', names=columns, nrows=5000)
    return df['text'].dropna().tolist()

def extract_trending_topics(tweets, top_n=10):
    all_words = []
    for tweet in tweets:
        tweet = re.sub(r"http\S+|@\S+|#|\W+", " ", tweet.lower())
        words = tweet.split()
        all_words.extend(words)

    stop_words = set([
        'the', 'and', 'for', 'you', 'that', 'with', 'this', 'just', 'have',
        'are', 'but', 'was', 'not', 'your', 'out', 'get', 'has', 'all',
        'about', 'can', 'what', 'from', 'they', 'will', 'one', 'like', 'now'
    ])
    filtered_words = [word for word in all_words if word not in stop_words and len(word) > 3]

    topic_counts = Counter(filtered_words).most_common(top_n)
    return topic_counts
