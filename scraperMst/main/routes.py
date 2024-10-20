from flask import Blueprint, render_template, current_app

# Create a blueprint named 'main' that will be used for handling routes related to the main section of the app
main = Blueprint('main', __name__)

# Home page route
# This route handles both '/' and '/home' URLs, rendering the 'index.html' template located in the 'home' directory
@main.route('/')
@main.route('/home')
def home():
    return render_template('main/home/index.html',)

# About page route
# This route handles the '/about' URL and renders the 'about.html' template
@main.route('/about')
def about():
    return render_template('main/about.html')
