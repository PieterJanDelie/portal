from flask import Blueprint, render_template
from services.gameFuncties import get_image_paths

home_view = Blueprint('home', __name__, template_folder='templates')

@home_view.route("")
def home():
    return render_template("Home/home.html", imagesources=get_image_paths())