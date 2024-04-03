import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template

stand_view = Blueprint('stand', __name__, template_folder='templates')

@stand_view.route("")
def stand():
    url = "https://bcoostende.be/uitslagen/elite-gold/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        stand_content = soup.find("div", class_="bigslam-single-article")

        if stand_content:
            return render_template("Stand/stand.html", stand_content=stand_content)
        else:
            return "De vereiste div kon niet worden gevonden op de website.", 500
    else:
        return "De website kon niet worden bereikt.", 500
