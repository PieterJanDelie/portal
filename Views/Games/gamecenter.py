from flask import Blueprint, render_template
from services.algemeneFuncties import get_image_paths, getRandomImage

game_view = Blueprint('Games', __name__, template_folder='templates')

@game_view.route("")
def GameCenter_Home():
    return render_template("Games/GameCenter.html", imagesources=get_image_paths(),  background_source=getRandomImage("Games/GameCenter/Startscherm"))