from flask import Blueprint, render_template, session
import os
from datetime import datetime
from services.gameFuncties import write_to_csv, getRandomImage

wordle_view = Blueprint('wordle', __name__, template_folder='templates')


@wordle_view.route("/")
def wordle_home():
    session["woord"]=""
    background_source=getRandomImage("wordle/spelers", InParentFolder=False)
    return render_template("Wordle/wordle.html", background_source=background_source)


@wordle_view.route("/Play")
def wordle_game():
    background_source=getRandomImage("wordle/spelers")
    woord = get_random(os.getenv('WORDLE_DATA_FILE'), 'woorden')
    session["woord"] = woord
    print(woord)
    return render_template("Wordle/wordle_start.html", background_source=background_source, woord=woord)
    

@wordle_view.route("/Einde/Geraden")
def wordle_end_geraden():
    background_source=getRandomImage("wordle/eindscherm/goed")
    woord = session["woord"]
    write_to_csv("Wordle/Eindscores.csv", [datetime.now(), woord, "Geraden"])
    return render_template("Wordle/wordle_end_geraden.html", background_source="../" + background_source, woord=woord)

@wordle_view.route("/Einde/NGeraden")
def wordle_end_N_geraden():
    background_source=getRandomImage("wordle/eindscherm/slecht")
    woord = session["woord"]
    write_to_csv("Wordle/Eindscores.csv", [datetime.now(), woord, "Niet geraden"])
    return render_template("Wordle/wordle_end_N_geraden.html", background_source="../" + background_source, woord=woord)