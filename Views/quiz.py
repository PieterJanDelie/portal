from flask import Blueprint, render_template, request, session
import os
from datetime import datetime
from services.gameFuncties import get_random, write_to_csv, getRandomImage

quiz_view = Blueprint('quiz', __name__, template_folder='templates')


@quiz_view.route("/")
def quiz_home():
    session['questions_answered'] = 0
    session['correct_answers'] = 0
    session['asked_questions'] = []
    return render_template("Quiz/quiz.html", background_source=getRandomImage("quiz/startscherm", InParentFolder=False))

@quiz_view.route("/StartQuiz", methods=['GET', 'POST'])
def start_quiz():
    if request.method == 'GET':
        print("Get")
        if session.get('questions_answered', 0) >= 3:
            print("Get if >= 3")
            eindscore = session.get('correct_answers', 0)
            session.pop('questions_answered', None)
            session.pop('correct_answers', None)
            session.pop('asked_questions', None)
            if eindscore >= 1:
                print("Get if eindscore >= 3")
                background_source=getRandomImage("quiz/eindscore/goed")
            else:
                print("Get else eindscore >= 3")
                background_source=getRandomImage("quiz/eindscore/slecht")
            write_to_csv("Quiz/Eindscores.csv", [datetime.now(), eindscore])
            return render_template("Quiz/quiz_end.html", eindscore=eindscore, background_source=background_source)
        else:
            print("Get else")
            vraag_data = get_random(os.getenv('QUIZ_DATA_FILE'),'vragen', asked_objecten=session.get('asked_questions', []), localvariabele='vraag')
            print("1")
            vraag = vraag_data['vraag']
            print("2")
            session['asked_questions'].append(vraag)
            print("Vraag: ", vraag)
            mogelijke_antwoorden = vraag_data['mogelijke_antwoorden']
            session['current_quiz_question'] = vraag_data
            return render_template("Quiz/quiz_start.html", vraag=vraag, mogelijke_antwoorden=mogelijke_antwoorden, background_source=getRandomImage("spelers"), VraagNummer= session.get('questions_answered', 0) + 1)
    elif request.method == 'POST':
        print("Post elif")
        session['questions_answered'] += 1
        vraag_data = session.get('current_quiz_question')
        juist_antwoord = vraag_data['juist_antwoord']
        vraag = vraag_data['vraag']
        answer = request.form['answer']
        write_to_csv("Quiz/Antwoorden.csv", [datetime.now(), vraag, answer])
        print("Vraag: ", vraag)
        print("Antwoord: ", answer ,"juist = ",answer == juist_antwoord)
        if answer == juist_antwoord:
            print("Post answer if == juist_antwoord")
            session['correct_answers'] = session.get('correct_answers', 0) + 1

        if answer == juist_antwoord:
            print("Post answer if == juist_antwoord")
            return render_template("Quiz/quiz_correct.html", antwoord=juist_antwoord, laatste_tekstje=vraag_data["laatste_tekstje"], background_source=getRandomImage("quiz/antwoorden/juist"))
        else:
            print("Post answer else == juist_antwoord")
            return render_template("Quiz/quiz_incorrect.html", antwoord=juist_antwoord, geantwoord=answer, laatste_tekstje=vraag_data["laatste_tekstje"], background_source=getRandomImage("quiz/antwoorden/fout"))
