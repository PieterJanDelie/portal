from flask import Blueprint, render_template

kalender_view = Blueprint('kalender', __name__, template_folder='templates')

@kalender_view.route("")
def kalender():
    return render_template("kalender.html")