"""Core Flask app routes."""
from flask import render_template
from flask import current_app as app



@app.route('/')
def home():
    return render_template('index.jinja2',
                           title='The Story of a Phish Song Dashboard',
                           template='home-template',
                           body="This is an interactive dashboard that allows you to input any Phish song and choose 7 different graphs to look at the trends of the song.")