from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sbert_recommender import load_tweets, recommend_tweets
from trending_utils import load_public_tweets, extract_trending_topics
import os
import config
from functools import wraps


app = Flask(__name__)
app.secret_key = config.secret_key
usrname = app.USERNAME = config.USERNAME
password = app.PASSWORD = config.PASSWORD
TWEETS_PER_PAGE = 20

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        if uname == usrname and pwd == password:
            session["user"] = uname
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Load data
csv_file = os.path.join(os.path.dirname(__file__), 'data', 'public_tweets.csv')
columns = ['sentiment', 'id', 'date', 'query', 'user', 'text']
df = pd.read_csv(csv_file, encoding='ISO-8859-1', names=columns, nrows=5000)
df.reset_index(inplace=True)
df.rename(columns={'index': 'tweet_id'}, inplace=True)

@app.route('/get_tweets')
@login_required
def get_tweets():
    page = int(request.args.get('page', 1))
    start = (page - 1) * TWEETS_PER_PAGE
    end = start + TWEETS_PER_PAGE
    tweets_slice = df.iloc[start:end]
    tweets = tweets_slice.to_dict(orient='records')
    total_pages = (len(df) + TWEETS_PER_PAGE - 1) // TWEETS_PER_PAGE
    return jsonify({"tweets": tweets, "total_pages": total_pages, "current": page,"totalItems":len(df),"itemsPerPage":TWEETS_PER_PAGE})

@app.route('/generate_recommendations')
@login_required
def generate_recommendations():
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['text'])
    similarity = cosine_similarity(tfidf_matrix)

    user_index = 0
    sim_scores = list(enumerate(similarity[user_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    recommended = [df.iloc[i].to_dict() for i, _ in sim_scores]
    session['recommendations'] = recommended
    return jsonify({"recommendations": recommended})

@app.route('/clear_recommendations')
@login_required
def clear_recommendations():
    session.pop('recommendations', None)
    return jsonify({"status": "cleared"})

@app.route('/get_recommendations')
@login_required
def get_recommendations():
    recs = session.get('recommendations', [])
    return jsonify({"recommendations": recs})

@app.route('/trending')
@login_required
def trending():
    tweets = load_public_tweets()
    topics = extract_trending_topics(tweets, top_n=10)
    return render_template('trending.html', topics=topics)

@app.route('/recommend_topic/<topic>',methods=['GET'])
@login_required
def recommend_topic(topic):
    #tweets = load_public_tweets()
    recommendations = recommend_tweets(topic, df, top_k=10)
    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)
