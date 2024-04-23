from flask import Blueprint, render_template, session
from datetime import datetime
from services.algemeneFuncties import write_to_csv, getRandomImage

shotgame_view = Blueprint('shotgame', __name__, template_folder='templates')


@shotgame_view.route("/")
def shotgame_home():
    background_source=getRandomImage("spelers", InParentFolder=False)
    return render_template("Games/BeginScherm.html", background_source=background_source, game="Shotgame", href="Shotgame/Play")


@shotgame_view.route("/Play")
def shotgame_game():
    background_source=getRandomImage("Spelers")
    return render_template("Games/Shotgame/shotgame_start.html", background_source=background_source)

@shotgame_view.route("/Einde/")
def shotgame_end():
    background_source=getRandomImage("Games/Rebus/Eindscherm/Slecht")
    woord = session["woord"]
    write_to_csv("Rebus/Eindscores.csv", [datetime.now(), woord, "Niet geraden"])
    return render_template("Games/End.html",game="Rebus", beschrijving="Spijtig u de rebus "+ woord + " niet op te lossen!", background_source=background_source, href="/Rebus")