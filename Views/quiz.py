import json
import random
from flask import Blueprint, render_template, request, session
import os
import csv
from datetime import datetime, timedelta

quiz_view = Blueprint('quiz', __name__, template_folder='templates')

def get_image_paths():
    image_paths = []
    static_dir = "static/"
    for root, _, files in os.walk(static_dir):
        for file in files:
            if file.endswith(('.jpg', '.png')):
                image_paths.append(os.path.join(root, file))
    return image_paths

def get_random_question(asked_questions):
    with open('Data/Vragen/' + os.getenv('DATA_FILE'), 'r') as f:
        vragen = json.load(f)['vragen']
        beschikbare_vragen = [vraag for vraag in vragen if vraag['vraag'] not in asked_questions]
        return random.choice(beschikbare_vragen)

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

@quiz_view.route("/")
def quiz_home():
    session['questions_answered'] = 0
    session['correct_answers'] = 0
    session['asked_questions'] = []
    image_paths = get_image_paths()
    return render_template("Quiz/quiz.html", background_source=getRandomImage("quiz/startscherm", InParentFolder=False),imagesources=image_paths)

@quiz_view.route("/StartQuiz", methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'GET':
        if session.get('questions_answered', 0) >= 3:
            eindscore = session.get('correct_answers', 0)
            session.pop('questions_answered', None)
            session.pop('correct_answers', None)
            session.pop('asked_questions', None)
            if eindscore >= 1:
                background_source=getRandomImage("quiz/eindscore/goed")
            else:
                background_source=getRandomImage("quiz/eindscore/slecht")
            write_to_csv("Quiz/Eindscores.csv", [datetime.now(), eindscore])
            return render_template("Quiz/quiz_end.html", eindscore=eindscore, background_source=background_source)
        else:
            vraag_data = get_random_question(session.get('asked_questions', []))
            vraag = vraag_data['vraag']
            session['asked_questions'].append(vraag)
            print("Vraag: ", vraag)
            mogelijke_antwoorden = vraag_data['mogelijke_antwoorden']
            session['current_quiz_question'] = vraag_data
            return render_template("Quiz/quiz_start.html", vraag=vraag, mogelijke_antwoorden=mogelijke_antwoorden, background_source=getRandomImage("quiz/spelers"), VraagNummer= session.get('questions_answered', 0) + 1)
    elif request.method == 'POST':
        session['questions_answered'] += 1
        vraag_data = session.get('current_quiz_question')
        juist_antwoord = vraag_data['juist_antwoord']
        vraag = vraag_data['vraag']
        answer = request.form['answer']
        write_to_csv("Quiz/Antwoorden.csv", [datetime.now(), vraag, answer])
        print("Vraag: ", vraag)
        print("Antwoord: ", answer ,"juist = ",answer == juist_antwoord)
        if answer == juist_antwoord:
            session['correct_answers'] = session.get('correct_answers', 0) + 1

        if answer == juist_antwoord:
            return render_template("Quiz/quiz_correct.html", antwoord=juist_antwoord, laatste_tekstje=vraag_data["laatste_tekstje"], background_source=getRandomImage("quiz/antwoorden/juist"))
        else:
            return render_template("Quiz/quiz_incorrect.html", antwoord=juist_antwoord, geantwoord=answer, laatste_tekstje=vraag_data["laatste_tekstje"], background_source=getRandomImage("quiz/antwoorden/fout"))
