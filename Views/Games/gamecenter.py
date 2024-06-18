from flask import Blueprint, render_template, session
from services.algemeneFuncties import getRandomImage

game_view = Blueprint('Games', __name__, template_folder='templates')

@game_view.route("")
def GameCenter_Home():
    session.clear() 
    return render_template("Games/GameCenter.html", background_source=getRandomImage("Games/GameCenter/Startscherm"))