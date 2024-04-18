from flask import Blueprint, render_template, request, session
import os
from datetime import datetime
from services.algemeneFuncties import get_random, write_to_csv, getRandomImage

quiz_view = Blueprint('quiz', __name__, template_folder='templates')


@quiz_view.route("/")
def quiz_home():
    session['questions_answered'] = 0
    session['correct_answers'] = 0
    session['asked_questions'] = []
    background_source=getRandomImage("Games/Quiz/Startscherm", InParentFolder=False)
    return render_template("Games/BeginScherm.html", background_source=background_source, game="Quiz", href="Quiz/Play")

@quiz_view.route("/StartQuiz", methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'GET':
        if session.get('questions_answered', 0) >= 3:
            eindscore = session.get('correct_answers', 0)
            session.pop('questions_answered', None)
            session.pop('correct_answers', None)
            session.pop('asked_questions', None)
            if eindscore >= 1:
                background_source=getRandomImage("Games/Quiz/Eindscore/Goed")
            else:
                background_source=getRandomImage("Games/Quiz/Eindscore/Slecht")
            write_to_csv("Quiz/Eindscores.csv", [datetime.now(), eindscore])
            return render_template("Games/End.html",game="Quiz", beschrijving="Je eindscore is: "+ str(eindscore) +"/3", background_source=background_source, href="/Quiz")
        else:
            vraag_data = get_random(os.getenv('QUIZ_DATA_FILE'),'vragen', asked_objecten=session.get('asked_questions', []), localvariabele='vraag')
            vraag = vraag_data['vraag']
            session['asked_questions'].append(vraag)
            print("Vraag: ", vraag)
            mogelijke_antwoorden = vraag_data['mogelijke_antwoorden']
            session['current_quiz_question'] = vraag_data
            return render_template("Games/Quiz/quiz_start.html", vraag=vraag, mogelijke_antwoorden=mogelijke_antwoorden, background_source=getRandomImage("Spelers"), VraagNummer= session.get('questions_answered', 0) + 1)
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
            background_source=getRandomImage("Games/Quiz/Antwoorden/Juist")
            title="Correct antwoord"
            inhoud=["Proficiat uw antwoord " + answer +" was juist!"]
        else:
            background_source=getRandomImage("Games/Quiz/Antwoorden/Fout")
            title="Fout antwoord"
            inhoud=["Spijtig, jouw antwoord "+ answer +" was verkeerd.","Het juiste antwoord was "+ juist_antwoord + "."]
            
        inhoud.append(vraag_data["laatste_tekstje"])
        return render_template("Games/Tussenscherm.html", background_source=background_source, inhoud=inhoud, href="/Quiz/Play", title=title)
