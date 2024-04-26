import requests

url = "http://127.0.0.1:5000/Uitslagen"

try:
    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
    else:
        print("Fout bij het ophalen van de pagina. Statuscode:", response.status_code)
except requests.RequestException as e:
    print("Er is een fout opgetreden bij het uitvoeren van de aanvraag:", e)