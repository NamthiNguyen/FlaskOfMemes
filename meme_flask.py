# Import necessary libraries
from flask import Flask, render_template  # Flask for web app, render_template to render HTML pages
import requests  # To make HTTP requests to external APIs
import json  # Not strictly needed here since requests.json() handles JSON parsing

# Initialize the Flask application
app = Flask(__name__)

# Function to fetch a meme from the OnlyPepes API
def get_meme():
    url = "https://api.onlypepes.xyz/v1/pepe"  # API endpoint for fetching a Pepe meme

    try:
        response = requests.get(url, timeout=5)  # Send GET request with a 5-second timeout
        response.raise_for_status()  # Raise exception if HTTP error occurs (like 404 or 500)
        data = response.json()  # Parse the JSON response

        # Check if the API returned a successful response
        if data.get("success"):
            meme_url = data.get("url", "")  # Get meme URL from JSON, fallback to empty string
            subreddit = "OnlyPepe"  # Default subreddit since API does not provide one
            return meme_url, subreddit
        else:
            # API returned success=False, provide a placeholder image
            return "https://via.placeholder.com/400x400.png?text=No+Meme", "Error"

    except requests.RequestException as e:
        # Handles network-related errors (e.g., connection issues, timeouts)
        print("Request failed:", e)
        return "https://via.placeholder.com/400x400.png?text=No+Meme", "Error"
    except ValueError as e:
        # Handles JSON parsing errors
        print("JSON parse failed:", e)
        return "https://via.placeholder.com/400x400.png?text=No+Meme", "Error"

# Define the route for the home page
@app.route("/")
def index():
    meme_pic, subreddit = get_meme()  # Call function to get meme
    # Render HTML template and pass meme URL and subreddit
    return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)

# Run the Flask app on localhost, port 5000, with debug mode on
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)