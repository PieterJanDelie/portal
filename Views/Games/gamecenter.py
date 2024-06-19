from flask import Blueprint, render_template
from services.algemeneFuncties import getRandomImage

game_view = Blueprint('Games', __name__, template_folder='templates')

@game_view.route("")
def GameCenter_Home():
    return render_template("Games/GameCenter.html", background_source=getRandomImage("Games/GameCenter/Startscherm"))