import json
import random
from flask import Blueprint, render_template, request, session
import os
import csv
from datetime import datetime, timedelta

questransfer_view = Blueprint('quesstransfer', __name__, template_folder='templates')

def get_image_paths():
    image_paths = []
    static_dir = "static/"
    for root, _, files in os.walk(static_dir):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def get_random_question(asked_players):
    with open('Data/Spelers/' + os.getenv('TRANSFER_DATA_FILE'), 'r') as f:
        spelers = json.load(f)['spelers']
        beschikbare_spelers = [speler for speler in spelers if speler['history'] not in asked_players]
        return random.choice(beschikbare_spelers)

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

@questransfer_view.route("/")
def questransfer_home():
    session['players_answered'] = 0
    print("reset")
    session['correct_answers'] = 0
    session['asked_players'] = []
    image_paths = get_image_paths()
    return render_template("Quess_Transfer/player.html", background_source=getRandomImage("quesstransfer/startscherm", InParentFolder=False),imagesources=image_paths)

@questransfer_view.route("/Start", methods=['GET', 'POST'])
def start_questransfer():
    if request.method == 'GET':
        if session.get('players_answered', 0) >= 3:
            eindscore = session.get('correct_answers', 0)
            session.pop('players_answered', None)
            session.pop('correct_answers', None)
            session.pop('asked_players', None)
            if eindscore >= 1:
                background_source=getRandomImage("quesstransfer/eindscore/goed")
            else:
                background_source=getRandomImage("quesstransfer/eindscore/slecht")
                write_to_csv("QuesTransfer/Eindscores.csv", [datetime.now(), eindscore])
            return render_template("Quess_Transfer/player_end.html", eindscore=eindscore, background_source=background_source)
        else:
            player_data = get_random_question(session.get('asked_players', []))
            history = player_data['history']
            player = player_data['juist_speler']
            session['asked_players'].append(player)
            print("player: ", player)
            mogelijke_antwoorden = player_data['mogelijke_spelers']
            session['current_quesstransfer_question'] = player_data
            return render_template("Quess_Transfer/player_start.html", vraag=history, mogelijke_antwoorden=mogelijke_antwoorden, background_source=getRandomImage("quesstransfer/spelers"), VraagNummer= session.get('players_answered', 0) + 1)
    elif request.method == 'POST':
        session['players_answered'] += 1
        player_data = session.get('current_quesstransfer_question')
        juist_antwoord = player_data['juist_speler']
        player = player_data['history']
        answer = request.form.get('answer')
        write_to_csv("Quesstransfer/Antwoorden.csv", [datetime.now(), player, answer])
        print("player: ", player)
        print("Antwoord: ", answer ,"juist = ",answer == juist_antwoord)
        if answer == juist_antwoord:
            session['correct_answers'] = session.get('correct_answers', 0) + 1

        if answer == juist_antwoord:
            return render_template("Quess_Transfer/player_correct.html", antwoord=juist_antwoord, laatste_tekstje=player_data["laatste_tekstje"], background_source=getRandomImage("quesstransfer/antwoorden/juist"))
        else:
            return render_template("Quess_Transfer/player_incorrect.html", antwoord=juist_antwoord, geantwoord=answer, laatste_tekstje=player_data["laatste_tekstje"], background_source=getRandomImage("quesstransfer/antwoorden/fout"))
