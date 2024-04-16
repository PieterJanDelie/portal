import os
from flask import Blueprint, render_template, request, session
from datetime import datetime
from services.algemeneFuncties import getRandomImage, write_to_csv, get_random

questransfer_view = Blueprint('quesstransfer', __name__, template_folder='templates')

@questransfer_view.route("/")
def questransfer_home():
    session['players_answered'] = 0
    print("reset")
    session['correct_answers'] = 0
    session['asked_players'] = []
    return render_template("Games/Quess_Transfer/player.html", background_source=getRandomImage("Games/Quesstransfer/startscherm", InParentFolder=False))

@questransfer_view.route("/Start", methods=['GET', 'POST'])
def start_questransfer():
    if request.method == 'GET':
        if session.get('players_answered', 0) >= 3:
            eindscore = session.get('correct_answers', 0)
            session.pop('players_answered', None)
            session.pop('correct_answers', None)
            session.pop('asked_players', None)
            if eindscore >= 1:
                background_source=getRandomImage("Games/Quesstransfer/Eindscore/Goed")
            else:
                background_source=getRandomImage("Games/Quesstransfer/Eindscore/Slecht")
                write_to_csv("QuesTransfer/Eindscores.csv", [datetime.now(), eindscore])
            return render_template("Games/Quess_Transfer/player_end.html", eindscore=eindscore, background_source=background_source)
        else:
            player_data = get_random(os.getenv('TRANSFER_DATA_FILE'), 'spelers',asked_objecten=session.get('asked_players', []), localvariabele='history')
            history = player_data['history']
            player = player_data['juist_speler']
            session['asked_players'].append(player)
            print("player: ", player)
            mogelijke_antwoorden = player_data['mogelijke_spelers']
            session['current_quesstransfer_question'] = player_data
            return render_template("Games/Quess_Transfer/player_start.html", vraag=history, mogelijke_antwoorden=mogelijke_antwoorden, background_source=getRandomImage("Spelers"), VraagNummer= session.get('players_answered', 0) + 1)
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
            return render_template("Games/Quess_Transfer/player_correct.html", antwoord=juist_antwoord, laatste_tekstje=player_data["laatste_tekstje"], background_source=getRandomImage("Games/Quesstransfer/Antwoorden/Juist"))
        else:
            return render_template("Games/Quess_Transfer/player_incorrect.html", antwoord=juist_antwoord, geantwoord=answer, laatste_tekstje=player_data["laatste_tekstje"], background_source=getRandomImage("Games/Quesstransfer/Antwoorden/Fout"))
