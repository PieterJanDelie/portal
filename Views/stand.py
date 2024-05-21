import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, session
from datetime import datetime, timedelta
from services.algemeneFuncties import getRandomImage

stand_view = Blueprint('stand', __name__, template_folder='templates')

@stand_view.route("")
def stand():
    if 'stand_content' in session:
        expiration_time = session.get('stand_expiration')
        if expiration_time and datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
            stand_content = session['stand_content']
            background_source = session.get('background_source', getRandomImage("Sfeer"))
            return render_template("Stand/stand.html", stand_content=stand_content, background_source=background_source)
    
    url = "https://bcoostende.be/uitslagen/elite-gold/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        stand_content = soup.find("div", class_="bigslam-single-article")

        if stand_content:
            session['stand_content'] = str(stand_content)
            session['stand_expiration'] = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            background_source = getRandomImage("Sfeer")
            session['background_source'] = background_source

            return render_template("Stand/stand.html", stand_content=stand_content, background_source=background_source)
        else:
            return "De vereiste div kon niet worden gevonden op de website.", 500
    else:
        return "De website kon niet worden bereikt.", 500
