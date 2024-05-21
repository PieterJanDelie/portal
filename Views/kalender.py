import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, session
from datetime import datetime, timedelta
from services.algemeneFuncties import getRandomImage

kalender_view = Blueprint('kalender', __name__, template_folder='templates')

@kalender_view.route("")
def kalender():
    if 'kalender_content' in session:
        expiration_time = session.get('kalender_expiration')
        if expiration_time and datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
            kalender_content = session['kalender_content']
            background_source = session.get('background_source', getRandomImage("Sfeer"))
            return render_template("Kalender/kalender.html", kalender_content=kalender_content, background_source=background_source)
    
    url = "https://bcoostende.be/event/speelkalender-2023-2024/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        kalender_content = soup.find("div", class_="sp-section-content sp-section-content-data")

        if kalender_content:
            for a_tag in kalender_content.find_all('a'):
                a_tag.unwrap()
            
            for date_element in kalender_content.find_all("date"):
                date_element.extract()

            session['kalender_content'] = str(kalender_content)
            session['kalender_expiration'] = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            background_source = getRandomImage("Sfeer")
            session['background_source'] = background_source

            return render_template("Kalender/kalender.html", kalender_content=kalender_content, background_source=background_source)
        else:
            return "Er zijn geen komende matchen.", 500
    else:
        return "Er liep iets verkeerd.", 500
