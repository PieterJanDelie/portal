from flask import Blueprint, render_template, request
from services.algemeneFuncties import write_to_csv, getRandomImage
from datetime import datetime

feedback_view = Blueprint('feedback', __name__, template_folder='templates')

@feedback_view.route("", methods=['GET', 'POST'])
def feedback():
    if request.method == 'GET':
        background_source = background_source=getRandomImage("Sfeer")
        return render_template("Feedback/feedback.html", background_source=background_source)
    elif request.method == 'POST':
        aankoop = request.form['aankoop']
        randanimatie = request.form['randanimatie']
        suggesties = request.form['suggesties']
        write_to_csv("Feedback/feedback.csv", [datetime.now(), aankoop, randanimatie, suggesties])
        background_source = background_source=getRandomImage("Sfeer")
        return render_template("Feedback/feedback_thanks.html", background_source=background_source)