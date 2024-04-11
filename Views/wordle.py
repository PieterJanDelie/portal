import json
import random
from flask import Blueprint, render_template, request, session
import os
import csv
from datetime import datetime, timedelta

wordle_view = Blueprint('wordle', __name__, template_folder='templates')

def get_image_paths():
    image_paths = []
    static_dir = "static/"
    for root, _, files in os.walk(static_dir):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def get_random_woord():
    with open('Data/Woorden/' + os.getenv('WORDLE_DATA_FILE'), 'r') as f:
        woorden = json.load(f)['woorden']
        return random.choice(woorden)

def write_to_csv(filename, data):
    today_date = datetime.now().strftime('%Y-%m-%d')
    if datetime.now().hour < 7:
        today_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    filepath = f'Data/Responses/{today_date}/{filename}'
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data)

def getRandomImage(subfolder, InParentFolder=True):
    image_dir = "static/"+ subfolder
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    if image_files:
        url = ""
        if InParentFolder:
            url += "../"
        url += image_dir + "/" + random.choice(image_files)
        return url
    else:
        return "../static/yellowbackground.jpg" # Default

def get_images(subfolder):
    image_dir = "static/"+ subfolder
    image_files = [f"{subfolder}/{f}" for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]
    return image_files

@wordle_view.route("/")
def wordle_home():
    session["woord"]=""
    background_source=getRandomImage("wordle/spelers", InParentFolder=False)
    return render_template("Wordle/wordle.html", background_source=background_source, imagesources=get_image_paths())


@wordle_view.route("/Play")
def wordle_game():
    background_source=getRandomImage("wordle/spelers")
    woord = get_random_woord()
    session["woord"] = woord
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