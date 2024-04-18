import json
import os
from flask import Blueprint, render_template, request, session
from services.algemeneFuncties import write_to_csv, getRandomImage
import random
from datetime import datetime

watLiever_view = Blueprint('watLiever', __name__, template_folder='templates')

def getLieverVragen():
    with open('Data/' + os.getenv('WATLIEVER_DATA_FILE'), 'r') as f:
        return json.load(f)["WatLiever"]

def updateJsonData(data, chosen_option):
    for vraag in data["WatLiever"]:
        if vraag["optie1"] == chosen_option:
            vraag["numOptie1"] += 1
        elif vraag["optie2"] == chosen_option:
            vraag["numOptie2"] += 1
    return data

@watLiever_view.route("/")
def watLiever_home():
    session['watLieverQuestions'] = getLieverVragen()
    return render_template("Games/WatLiever/watliever.html", background_source=getRandomImage("Games/WatLiever/Startscherm", InParentFolder=False))

@watLiever_view.route("/Start", methods=['GET', 'POST'])
def start_watLiever():
    if request.method == 'GET':
        if not session['watLieverQuestions']:
            background_source=getRandomImage("Games/WatLiever/Eindscherm", InParentFolder=True)
            return render_template("Games/End.html",game="WatLiever", beschrijving="Je hebt alles ingevuld bedankt!", background_source=background_source, href="/WatLiever")
        watLieverVraag = session['watLieverQuestions'].pop(random.randint(0, len(session['watLieverQuestions']) - 1))
        session["currentWatLiever"] = watLieverVraag
        return render_template("Games/WatLiever/watliever_start.html", background_source=getRandomImage("Games/WatLiever/Startscherm", InParentFolder=True), vraag=watLieverVraag)
    elif request.method == 'POST':
        gekozen_optie = request.form['keuze']
        print("Gekozen optie:", gekozen_optie)
        currentVraag = session["currentWatLiever"]
        
        json_file_path = 'Data/' + os.getenv('WATLIEVER_DATA_FILE')
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        updated_data = updateJsonData(data, gekozen_optie)

        with open(json_file_path, 'w') as f:
            json.dump(updated_data, f, indent=4)
        
        write_to_csv("WatLiever/Antwoorden.csv", [datetime.now(), currentVraag, gekozen_optie])
        return render_template("Games/WatLiever/watliever_tussenscherm.html", background_source=getRandomImage("Games/WatLiever/Startscherm", InParentFolder=True), vraag=currentVraag, procent=50) 