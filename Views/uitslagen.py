import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template

uitslagen_view = Blueprint('uitslagen', __name__, template_folder='templates')

@uitslagen_view.route("")
def uitslagen():
    url = "https://bcoostende.be/wedstrijd-uitslagen/"

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        event_list = soup.find("div", class_="sp-template sp-template-event-list")

        if event_list:
            # Zoek en verwijder alle <a> elementen
            for a_tag in event_list.find_all("a"):
                a_tag.unwrap()

            # Zoek en verwijder de laatste kolom met de classnaam "data-article"
            for row in event_list.find_all("tr"):
                last_cell = row.find("td", class_="data-article")
                if last_cell:
                    last_cell.decompose()

            # Zoek en verwijder de kolomnaam "article"
            for row in event_list.find_all("th", class_="data-article"):
                row.decompose()

            return render_template("Uitslagen/uitslagen.html", event_list=event_list)
        else:
            return "Er zijn nog geen uitslagen", 500
    else:
        return "Er liep iets mis.", 500
