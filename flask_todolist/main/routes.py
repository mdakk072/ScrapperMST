from flask import Blueprint, render_template,current_app
from flask_todolist.main.utils import load_background_images

main = Blueprint('main', __name__)

# Home page route
@main.route('/')
@main.route('/home')
def home():
    background_images = load_background_images(current_app.static_folder)
    return render_template('home.html', background_images=background_images)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')