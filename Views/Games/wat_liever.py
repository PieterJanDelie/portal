import json
import os
from flask import Blueprint, render_template, request, session
from services.algemeneFuncties import get_random, write_to_csv, getRandomImage
import random

watLiever_view = Blueprint('watLiever', __name__, template_folder='templates')

def getLieverVragen():
    with open('Data/' + os.getenv('WATLIEVER_DATA_FILE'), 'r') as f:
        return json.load(f)["WatLiever"]

@watLiever_view.route("/")
def watLiever_home():
    session['watLieverQuestions'] = getLieverVragen()
    return render_template("Games/WatLiever/watliever.html", background_source=getRandomImage("Games/WatLiever/Startscherm", InParentFolder=False))

@watLiever_view.route("/Start", methods=['GET', 'POST'])
def start_watLiever():
    if request.method == 'GET':
        if not session['watLieverQuestions']:
            return render_template("Games/WatLiever/watliever_end.html", background_source=getRandomImage("Games/WatLiever/Eindscherm", InParentFolder=True))
        watLieverVraag = session['watLieverQuestions'].pop(random.randint(0, len(session['watLieverQuestions']) - 1))
        session["currentWatLiever"] = watLieverVraag
        return render_template("Games/WatLiever/watliever_start.html", background_source=getRandomImage("Games/WatLiever/Startscherm", InParentFolder=True), vraag=watLieverVraag)
    elif request.method == 'POST':
        gekozen_optie = request.form['keuze']
        print("Gekozen optie:", gekozen_optie)
        currentVraag = session["currentWatLiever"]
        return render_template("Games/WatLiever/watliever_tussenscherm.html", background_source=getRandomImage("Games/WatLiever/Startscherm", InParentFolder=True), vraag=currentVraag, procent=50) 