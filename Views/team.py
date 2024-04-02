from flask import Blueprint, render_template

team_view = Blueprint('team', __name__, template_folder='templates')

@team_view.route("")
def team():
    return render_template("team.html")