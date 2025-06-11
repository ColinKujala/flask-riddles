"""
Random Riddle Flask App

Use https://riddles-api.vercel.app/random to get a random riddle.
Present the riddle text to the user. Let them select a button to make
the answer visible.
"""

import os

import requests
from flask import Flask, render_template


app = Flask(__name__)


def get_riddle():
    """Retrieve a random riddle from page on internet"""
    return requests.get("https://riddles-api.vercel.app/random").json()


@app.route("/")
def home():
    riddle = get_riddle()

    return render_template(
        "home.jinja2",
        riddle=riddle
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
