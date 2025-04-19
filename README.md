# Twitter Data Mining and Recommendation System

This is a Flask-based web application that:

- Loads and displays tweets from a CSV file (1000 tweets).
- Allows generating **personalized tweet recommendations** using **TF-IDF** based on tweet content similarity.
- Displays results with **Bootstrap-style pagination**.
- Includes **loader animation**, and buttons to **Generate** and **Clear Recommendations**.


## Project Structure

twitter-data-app/
  static/
     js/app.js           # JavaScript for AJAX, pagination, event handling
     css/style.css       # Custom styles
templates/
     index.html          # Main frontend interface
data
     public_tweets.csv   # Dataset file (without column names)
app.py                   # Flask backend logic
README.md                # Project documentation
config.py                # Store a secret key.

## Requirements

### Python Version
- Python 3.8 or higher (recommended: Python 3.10+)

### Required Libraries
Install them using pip:
pip install flask pandas scikit-learn
Or use the provided `requirements.txt`:
pip install -r requirements.txt

#### Example `requirements.txt`
Flask==2.3.2
pandas==2.2.1
scikit-learn==1.4.2

## How to Run

### 1.download the project extract it and naviagte to the project directory
     cd twitter-data-app

### 2. Make sure `public_tweets.csv` exists and has 1000 or more tweets.

### 3. Start the Flask App
python app.py
You should see:
 * Running on http://127.0.0.1:5000/

## Features

### Load Tweets
- Loads 1000 tweets from `public_tweets.csv`.
- Displays them in a table format with Bootstrap pagination.

### Generate Recommendations
- Based on **TF-IDF content similarity**.
- Calculates similarity between tweets and generates top matches.
- Results shown in a separate table with pagination.

### Clear Recommendations
- Clears the recommendation table.

### Loader Animation
- "Loading..." shows while data is fetched.

## Testing Tips
- You can replace `public_tweets.csv` with your own tweet data (just keep the format `user,text`).

## Troubleshooting

- **404 for CSS/JS**: Make sure files are in `static/` and paths are `/static/css/style.css` and `/static/js/ app.js`.
- **UnicodeDecodeError**: Use `encoding='ISO-8859-1'` or `errors='replace'` when loading CSV.
- **CORS Issues**: Flask is local only. If deploying externally, enable CORS with `flask-cors`.
