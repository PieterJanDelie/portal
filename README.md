# Quiz

Al de code is te vinden op [https://github.com/PieterJanDelie/quiz](https://github.com/PieterJanDelie/quiz).

## Inhoudstafel

- [Quiz](#quiz)
  - [Inhoudstafel](#inhoudstafel)
  - [Good to know!](#good-to-know)
    - [Alle antwoorden komen in de map Data/Response](#alle-antwoorden-komen-in-de-map-dataresponse)
    - [Afbeeldingen worden random gegenereerd](#afbeeldingen-worden-random-gegenereerd)
    - [Vragen toevoegen of wijzigen](#vragen-toevoegen-of-wijzigen)
      - [Volledige nieuwe vragen maken](#volledige-nieuwe-vragen-maken)
  - [Code](#code)
    - [main.py](#mainpy)
    - [Views/init.py](#viewsinitpy)
    - [Views/quiz.py](#viewsquizpy)
    - [Documentatie voor Quiz Webpagina's](#documentatie-voor-quiz-webpaginas)
      - [quiz.html](#quizhtml)
      - [quiz\_start.html](#quiz_starthtml)
      - [quiz\_correct.html](#quiz_correcthtml)
      - [quiz\_incorrect.html](#quiz_incorrecthtml)
      - [quiz\_end.html](#quiz_endhtml)

## Good to know!

### Alle antwoorden komen in de map [Data/Response](./Data/Responses)

Daarin wordt er per dag een extra folder opgeslagen. Dit is om een gemakkelijker overzicht te krijgen over al de matchen heen. Als een quiz is ingevuld voor 7u sochtends komt dit automatisch bij de folder van gisteren, dit is om ervoor te zorgen da er op avondmatchen niet net na 12 u al de antwoorden in een andere folder komen.
In de folders per dag vindt u een Antwoorden.csv en een Eindscores.csv. In Antwoorden.csv staan de antwoorden elk individueel terwijl bij Eindscores.csv staat enkel hoeveel iemand heeft behaald.

### Afbeeldingen worden random gegenereerd

Afbeeldingen staan allemaal in de map [Static](./static). **(Dit mag niet worden veranderd van naam!!!)** Het random genereren van de afbeeldingen gebeurd automatisch. De code zal zelf kijken hoeveel en welke afbeelding in de folders staan. Er kunnen dus zoveel afbeeldingen worden toegevoegd als gewenst. De code zal deze afbeelding zelf toevoegen. Als je een afbeelding toevoegd best wel eerst comprimeren met bijvoorbeeld [Deze site](https://imagecompressor.com/nl/). Probeer de afbeeldingen liefst onder de **2 à 3mb** te houden.

### Vragen toevoegen of wijzigen

Al de vragen staan in [Data/Vragen](./Data/Vragen/QuizVragen.json). Dit kan je vrij aanpassen zoals gewenst. Zorg er wel voor dat de structuur behouden blijft als volgt.

```json
{
  "vragen": [
    {
      "vraag": "",
      "mogelijke_antwoorden": ["","", "", ""],
      "juist_antwoord": "",
      "laatste_tekstje": ""
    },
  ]
}
```

Er kunnen wel zoveel als gewenst vragen toegevoegd worden. Dit doe je door een object in de "vragen": [] toe te voegen. Zorg er wel voor dat de variabele-namen perfect identiek blijven anders zal de applicatie crashen. Ook moet het juist_antwoord perfect overéén komen met een optie van mogelijke_antwoorden. Momenteel worden er overal maar 4 opties meegegeven maar dit is **vrij te kiezen.**

#### Volledige nieuwe vragen maken

Je kan ook volledige nieuwe vragen maken. Stel je wilt bijvoorbeeld vragen voor in de foyer en vragen voor in de VIP. Je voegt een nieuwe .json toe in de folder [Data/Vragen](./Data/Vragen). De andere file mag je laten staan. Zorg dat de structuur overeen komt met de eerder gegeven structuur. Tot slot moet je nog tegen de applicatie zeggen welke file deze moet gebruiken om de vragen van uit te lezen. Dit doe je door u te verplaatsen naar de file .env. Daarin zie je

```
DATA_FILE="QuizVragen.json"
```

Verander hierin de datafile naar de naam van de nieuwe file. **Opgepast! de "-haaktjes moeten blijven staan rond de filenaam.

## Code

De codebase van de quizapplicatie is opgedeeld in verschillende modules en bestanden om de functionaliteit georganiseerd en onderhoudbaar te houden. Hieronder wordt een gedetailleerde beschrijving gegeven van elk onderdeel van de code.

### [main.py](main.py)

[`main.py`](main.py) vormt de kern van de applicatie. Hier wordt een Flask-applicatie geïnitialiseerd en geconfigureerd. De `Flask`-klasse wordt geïmporteerd vanuit het Flask-framework. Daarnaast worden ook enkele belangrijke bibliotheken zoals `Flask`, `request`, `render_template`, `session`, en `os` geïmporteerd voor de functionaliteit van de applicatie. 

- `Flask(__name__)`: Hier wordt een Flask-applicatie geïnitialiseerd met de naam van het bestand.
- `app.secret_key`: De geheime sleutel wordt ingesteld voor sessiebeheer, waarbij de waarde wordt opgehaald uit een omgevingsvariabele met behulp van `os.getenv`.
- Routes worden toegevoegd aan de applicatie met behulp van `app.add_url_rule`, die verwijzen naar functies in de `quiz_home` en `start_quiz` views.

### [Views/init.py](./Views/init.py)

Dit bestand bevat code die gerelateerd is aan de initialisatie en configuratie van de quizmodule binnen de Flask-applicatie.

- `register_blueprints`: Een functie die de blueprint van de quizmodule registreert bij de Flask-applicatie. Een blueprint is een manier om verschillende delen van een applicatie te organiseren en te moduleren.
- Importeren van `quiz_view` vanuit [`Views/quiz.py`](./Views/quiz.py).
- Registratie van de blueprint en toevoeging van URL-routes voor de quizweergaven.

### [Views/quiz.py](./Views/quiz.py)

Dit bestand bevat de kernfunctionaliteit van de quizapplicatie. Het omvat functies voor het beheren van vragen, het genereren van afbeeldingen, het verwerken van quizlogica en het schrijven naar CSV-bestanden voor antwoorden.

- `quiz_view`: Een blueprint voor het definiëren van quizroutes en -weergaven. Hier worden URL-routes gedefinieerd voor de quizhomepagina en het starten van de quiz.
- `get_image_paths`: Een functie die de paden van afbeeldingen ophaalt uit de statische map.
- `get_random_question`: Een functie die willekeurige vragen selecteert uit een JSON-bestand met vragen.
- `write_to_csv`: Een functie voor het schrijven van gegevens naar CSV-bestanden, zoals antwoorden en eindscores.
- Andere hulpprogrammafuncties zoals `getRandomImage` en `get_images` worden gebruikt voor het beheren van afbeeldingen.

Elke functie is ontworpen om een specifieke taak uit te voeren binnen de quizapplicatie, zoals het renderen van pagina's, het verwerken van gebruikersinvoer en het beheren van quizgegevens.

De code maakt gebruik van externe bibliotheken zoals Flask voor het bouwen van de webapplicatie, en dotenv voor het laden van omgevingsvariabelen uit een `.env`-bestand. Het is modulair opgebouwd om onderhoud en uitbreiding gemakkelijker te maken.

### Documentatie voor Quiz Webpagina's

In dit deel zullen we de structuur en functionaliteit van verschillende HTML-pagina's bespreken die worden gebruikt voor een quizapplicatie. Deze pagina's omvatten:

- **quiz.html:** De startpagina van de quiz.
- **quiz_start.html:** Pagina voor het starten van een vraag.
- **quiz_correct.html:** Pagina die wordt weergegeven bij een correct antwoord.
- **quiz_incorrect.html:** Pagina die wordt weergegeven bij een incorrect antwoord.
- **quiz_end.html:** Pagina die wordt weergegeven aan het einde van de quiz.

Alles is te vinden in de folder templates. Deze naam moet hetzelfde blijven.

#### quiz.html

Dit is de startpagina van de quiz. Hier kunnen gebruikers de quiz starten door op de knop "Start Quiz" te klikken.

1. **Structuur:**

   - Header: Bevat de titel van de quiz.
   - Start Quiz Button: Een knop waarmee gebruikers de quiz kunnen starten.
   - Footer: Toont het logo van de organisator van de quiz.

2. **Functionaliteit:**
    - Het logo wordt weergegeven.
    - De achtergrondafbeelding wordt geladen.
    - Gebruikers kunnen op de knop "Start Quiz" klikken om naar de eerste vraag te gaan.

#### quiz_start.html

Deze pagina wordt weergegeven wanneer een nieuwe vraag begint.

1. **Structuur:**
    - Vraagnummer: Toont het huidige vraagnummer.
    - Vraag: Toont de vraag.
    - Antwoordopties: Toont de mogelijke antwoordopties als keuzerondjes.
    - Volgende-knop: Hiermee kunnen gebruikers naar de volgende vraag gaan.

1. **Functionaliteit:**
    - Gebruikers kunnen een antwoord kiezen.
    - Bij het klikken op "Volgende" wordt het antwoord verwerkt en gaat de gebruiker naar de volgende vraag.

#### quiz_correct.html

Deze pagina wordt weergegeven wanneer een gebruiker een vraag correct beantwoordt.

1. **Structuur:**
    - Bericht: Toont een felicitatiebericht voor het correct beantwoorden van de vraag.
    - Volgende-knop: Hiermee kunnen gebruikers doorgaan naar de volgende vraag.

1. **Functionaliteit:**
    - Geeft feedback aan de gebruiker over het juiste antwoord.
    - Biedt de mogelijkheid om door te gaan naar de volgende vraag.

#### quiz_incorrect.html

Deze pagina wordt weergegeven wanneer een gebruiker een vraag fout beantwoordt.

1. **Structuur:**
    - Bericht: Toont een foutbericht en het juiste antwoord.
    - Volgende-knop: Hiermee kunnen gebruikers doorgaan naar de volgende vraag.

1. **Functionaliteit:**
    - Geeft feedback aan de gebruiker over het foute antwoord en toont het juiste antwoord.
    - Biedt de mogelijkheid om door te gaan naar de volgende vraag.

#### quiz_end.html

Deze pagina wordt weergegeven aan het einde van de quiz.

1. **Structuur:**
    - Bedankbericht: Toont een bedankbericht voor het deelnemen aan de quiz.
    - Eindscore: Toont de eindscore van de gebruiker.
    - Opnieuw spelen-knop: Hiermee kunnen gebruikers de quiz opnieuw starten.

1. **Functionaliteit:**
    - Geeft een samenvatting van de quizresultaten weer.
    - Biedt de mogelijkheid om de quiz opnieuw te starten.
    - Dit zijn de verschillende pagina's en hun functionaliteit binnen de quizapplicatie. Ze bieden een intuïtieve gebruikerservaring en begeleiden de gebruiker door het quizproces.
