import json
import random
from flask import Blueprint, render_template, request, session
import os

quiz_view = Blueprint('quiz', __name__, template_folder='templates')

def get_random_question(asked_questions):
    with open('Data/QuizVragen.json', 'r') as f:
        vragen = json.load(f)['vragen']
        beschikbare_vragen = [vraag for vraag in vragen if vraag['vraag'] not in asked_questions]
        return random.choice(beschikbare_vragen)

def getRandomImage(subfolder, InParentFolder = True):
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

@quiz_view.route("/")
def quiz_home():
    session['questions_answered'] = 0
    session['correct_answers'] = 0
    session['asked_questions'] = []
    return render_template("Quiz/quiz.html", background_source=getRandomImage("startscherm", InParentFolder=False))

@quiz_view.route("/StartQuiz", methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'GET':
        if session.get('questions_answered', 0) >= 5:
            eindscore = session.get('correct_answers', 0)
            session.pop('questions_answered', None)
            session.pop('correct_answers', None)
            session.pop('asked_questions', None)
            if eindscore >= 3:
                background_source=getRandomImage("eindscore/goed")
                eindtekst = "Nu ben je officieel lid van de Yellow-Wall"
            else:
                background_source=getRandomImage("eindscore/slecht")
                eindtekst = "Blijf het proberen!"
            return render_template("Quiz/quiz_end.html", eindscore=eindscore, background_source=background_source, eindtekst=eindtekst)
        else:
            vraag_data = get_random_question(session.get('asked_questions', []))
            vraag = vraag_data['vraag']
            session['asked_questions'].append(vraag)
            mogelijke_antwoorden = vraag_data['mogelijke_antwoorden']
            session['current_quiz_question'] = vraag_data
            return render_template("Quiz/quiz_start.html", vraag=vraag, mogelijke_antwoorden=mogelijke_antwoorden, background_source=getRandomImage("spelers"))
    elif request.method == 'POST':
        session['questions_answered'] += 1
        vraag_data = session.get('current_quiz_question')
        juist_antwoord = vraag_data['juist_antwoord']
        answer = request.form['answer']
        if answer == juist_antwoord:
            session['correct_answers'] = session.get('correct_answers', 0) + 1

        if answer == juist_antwoord:
            return render_template("Quiz/quiz_correct.html", antwoord=juist_antwoord, laatste_tekstje=vraag_data["laatste_tekstje"], background_source=getRandomImage("antwoorden/juist"))
        else:
            return render_template("Quiz/quiz_incorrect.html", antwoord=juist_antwoord, geantwoord=answer, laatste_tekstje=vraag_data["laatste_tekstje"], background_source=getRandomImage("antwoorden/fout"))
