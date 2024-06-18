from flask import Blueprint, render_template, session
from services.algemeneFuncties import get_image_paths, getRandomImage

home_view = Blueprint('home', __name__, template_folder='templates')

@home_view.route("")
def home():
    session.clear() 
    print("load")

    first_visit = 'visited' not in session
    if first_visit:
        session['visited'] = True

    sources = get_image_paths() if first_visit else []
    return render_template("Home/home.html", imagesources=sources, background_source=getRandomImage("Sfeer"))
