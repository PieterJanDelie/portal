from flask import Blueprint, render_template, session
import os
from datetime import datetime
from services.algemeneFuncties import write_to_csv, getRandomImage

rebus_view = Blueprint('rebus', __name__, template_folder='templates')


@rebus_view.route("/")
def rebus_home():
    session["woord"]=""
    background_source=getRandomImage("spelers", InParentFolder=False)
    return render_template("Games/BeginScherm.html", background_source=background_source, game="Rebus", href="Rebus/Play")


@rebus_view.route("/Play")
def rebus_game():
    background_source=getRandomImage("Spelers", InParentFolder=False)
    rebus_source=getRandomImage("Games/Rebus/Rebussen", InParentFolder=False)
    filename = os.path.basename(rebus_source)
    filename_without_extension = os.path.splitext(filename)[0]
    session["woord"] = filename_without_extension
    print(filename_without_extension)
    return render_template("Games/Rebus/rebus_start.html", background_source="../"+background_source, rebus_source="../"+rebus_source, woord=filename_without_extension)
    

@rebus_view.route("/Einde/Geraden")
def rebus_end_geraden():
    background_source="../"+getRandomImage("Games/Rebus/Eindscherm/Goed")
    woord = session["woord"]
    write_to_csv("Rebus/Eindscores.csv", [datetime.now(), woord, "Geraden"])
    return render_template("Games/End.html",game="Rebus", beschrijving="Proficiat u wist de rebus "+ woord + " op te lossen!", background_source=background_source, href="/Rebus")

@rebus_view.route("/Einde/NGeraden")
def rebus_end_N_geraden():
    background_source="../"+getRandomImage("Games/Rebus/Eindscherm/Slecht")
    woord = session["woord"]
    write_to_csv("Rebus/Eindscores.csv", [datetime.now(), woord, "Niet geraden"])
    return render_template("Games/End.html",game="Rebus", beschrijving="Spijtig u wist de rebus "+ woord + " niet op te lossen!", background_source=background_source, href="/Rebus")