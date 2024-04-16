from flask import Blueprint, render_template, session
import os
from datetime import datetime
from services.algemeneFuncties import write_to_csv, getRandomImage, get_random

wordle_view = Blueprint('wordle', __name__, template_folder='templates')


@wordle_view.route("/")
def wordle_home():
    session["woord"]=""
    background_source=getRandomImage("Spelers", InParentFolder=False)
    return render_template("Games/Wordle/wordle.html", background_source=background_source)


@wordle_view.route("/Play")
def wordle_game():
    background_source=getRandomImage("Spelers")
    woord = get_random(os.getenv('WORDLE_DATA_FILE'), 'woorden')
    session["woord"] = woord
    print(woord)
    return render_template("Games/Wordle/wordle_start.html", background_source=background_source, woord=woord)
    

@wordle_view.route("/Einde/Geraden")
def wordle_end_geraden():
    background_source=getRandomImage("Games/Wordle/Eindscherm/Goed")
    woord = session["woord"]
    write_to_csv("Wordle/Eindscores.csv", [datetime.now(), woord, "Geraden"])
    return render_template("Games/Wordle/wordle_end_geraden.html", background_source="../" + background_source, woord=woord)

@wordle_view.route("/Einde/NGeraden")
def wordle_end_N_geraden():
    background_source=getRandomImage("Games/Wordle/Eindscherm/Slecht")
    woord = session["woord"]
    write_to_csv("Wordle/Eindscores.csv", [datetime.now(), woord, "Niet geraden"])
    return render_template("Games/Wordle/wordle_end_N_geraden.html", background_source="../" + background_source, woord=woord)