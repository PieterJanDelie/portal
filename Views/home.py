from flask import Blueprint, render_template
from services.algemeneFuncties import get_image_paths, getRandomImage

home_view = Blueprint('home', __name__, template_folder='templates')

@home_view.route("")
def home():
    return render_template("Home/home.html", imagesources=get_image_paths(),  background_source=getRandomImage("Sfeer"))