from sentence_transformers import SentenceTransformer, util
import pandas as pd

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_tweets(path='data/public_tweets.csv'):
    df = pd.read_csv(path, encoding='ISO-8859-1', names=['sentiment', 'id', 'date', 'query', 'user', 'text'])
    df.dropna(subset=['text'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df



def recommend_tweets(user_input, df, top_k=5):
    tweets = df['text'].tolist()
    user_vec = model.encode(user_input, convert_to_tensor=True)
    tweet_vecs = model.encode(tweets, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(user_vec, tweet_vecs)[0]
    top_results = scores.topk(top_k)

    # Return list of dicts with tweet text, user, and score
    results = []
    for idx in top_results.indices:
        idx = idx.item()
        results.append({
            "text": df.iloc[idx]['text'],
            "user": df.iloc[idx]['user'],
            "score": float(scores[idx])
        })

    return results


