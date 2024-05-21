import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, session
from datetime import datetime, timedelta
from services.algemeneFuncties import getRandomImage

uitslagen_view = Blueprint('uitslagen', __name__, template_folder='templates')

@uitslagen_view.route("")
def uitslagen():
    if 'uitslagen_content' in session:
        expiration_time = session.get('uitslagen_expiration')
        if expiration_time and datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S') > datetime.now():
            event_list = session['uitslagen_content']
            background_source = session.get('background_source', getRandomImage("Sfeer"))
            return render_template("Uitslagen/uitslagen.html", event_list=event_list, background_source=background_source)
    
    url = "https://bcoostende.be/wedstrijd-uitslagen/"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        event_list = soup.find("div", class_="sp-table-wrapper")

        if event_list:
            for a_tag in event_list.find_all("a"):
                a_tag.unwrap()
                
            for date_element in event_list.find_all("date"):
                date_element.extract()

            for row in event_list.find_all("tr"):
                last_cell = row.find("td", class_="data-article")
                if last_cell:
                    last_cell.decompose()

            for row in event_list.find_all("th", class_="data-article"):
                row.decompose()

            session['uitslagen_content'] = str(event_list)
            session['uitslagen_expiration'] = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
            background_source = getRandomImage("Sfeer")
            session['background_source'] = background_source

            return render_template("Uitslagen/uitslagen.html", event_list=event_list, background_source=background_source)
        else:
            return "Er zijn nog geen uitslagen", 500
    else:
        return "Er liep iets mis.", 500
