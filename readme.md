# ContactApi

Ett REST API byggt med FastAPI för hantering av kontakter, ungefär som en kontaktlista i en mobiltelefon.

Projektet är utvecklat som ett slutprojekt i kursen Pythonprogrammering och fokuserar på:

* REST API-design
* FastAPI
* Pydantic-modeller
* JSON-baserad persistent lagring
* Validering av data
* CRUD-operationer

GitHub repository:
[ContactApi Github Repository](https://github.com/john-lund-af/ContactApi?utm_source=chatgpt.com)

---

# Funktionalitet

API stödjer följande funktioner:

* Skapa kontakt
* Hämta alla kontakter
* Hämta specifik kontakt
* Uppdatera kontakt
* Ta bort kontakt
* Söka efter kontakter
* Favoritmarkering av kontakter
* Validering av e-postadresser

Varje kontakt kan innehålla:

* Förnamn
* Efternamn
* Anteckningar
* Flera kontaktuppgifter
* Flera adresser
* Favoritmarkering
* Skapad- och uppdaterad-tid

---

# Tekniker

Projektet använder:

* Python
* FastAPI
* Pydantic
* UUID
* JSON som databas
* Uvicorn

---

# Beskrivning av kodens struktur

Projektet är uppdelat i flera lager för att skapa en tydlig och skalbar struktur.

## Models

Pydantic-modeller används för:

* validering av inkommande data
* strukturering av API-svar
* separering mellan create/update/read-modeller

Exempel:

* `ContactCreate`
* `ContactUpdate`
* `Contact`
* `ContactInfo`
* `Address`

---

## Repository

Repository-lagret ansvarar för:

* CRUD-operationer
* sökning
* hantering av affärslogik
* kommunikation med JSON-databasen

Detta gör att routes hålls rena och fokuserade på HTTP-hantering.


## Projektstruktur

```text
app/
├── main.py
├── readme.md
├── models/
│   └── contact_models.py
├── repositories/
│   └── contacts_repo.py
├── database/
│   └── json_db.py
├── routes/
│   └── contacts.py
└── db/
    └── contacts.json
```

---

## Database

JSON används som enkel persistent databas.

Datat lagras i:

```text
contacts.json
```

Database-lagret ansvarar endast för:

* läsa data
* skriva data

---

## Routes

Routes ansvarar för:

* HTTP-endpoints
* request/response
* statuskoder
* validering via FastAPI

---

# Installation

## Klona projektet

```bash
git clone https://github.com/john-lund-af/ContactApi.git
```

## Installera beroenden

```bash
pip install fastapi[standard]
```

## Starta servern

```bash
fastapi dev app/main.py
```

eller:

```bash
uvicorn app.main:app --reload
```

---

# Swagger dokumentation

När servern körs:

```text
http://127.0.0.1:8000/docs
```

---

# Exempel på API-anrop

## 1. Skapa kontakt

### POST `/contacts`

```json
{
    "first_name": "Anna",
    "last_name": "Svensson",
    "notes": "Gammal kollega",
    "favorite": true,
    "contact_infos": [
        {
            "type": "private",
            "phone": "0701234567",
            "email": "anna@example.com"
        }
    ],
    "addresses": [
        {
            "type": "home",
            "street": "Storgatan 1",
            "city": "Stockholm",
            "country": "Sweden"
        }
    ]
}
```

---

## 2. Hämta alla kontakter

### GET `/contacts`

```bash
curl http://127.0.0.1:8000/contacts
```

---

## 3. Söka efter kontakt

### GET `/contacts/search/?query=anna`

```bash
curl "http://127.0.0.1:8000/contacts/search/?query=anna"
```

---

## 4. Uppdatera kontakt

### PUT /contacts/{contact_id}

```json
{
    "first_name": "Maria",
    "last_name": "Andersson",
    "notes": "Ny kollega från jobbet",
    "favorite": false,
    "contact_infos": [
        {
            "type": "work",
            "phone": "0701112233",
            "email": "maria.andersson@company.se"
        }
    ],
    "addresses": [
        {
            "type": "home",
            "street": "Sveavägen 10",
            "city": "Stockholm",
            "country": "Sweden"
        }
    ]
}
```

---

## 5. Ta bort kontakt

### DELETE `/contacts/{contact_id}`

```bash
curl -X DELETE http://127.0.0.1:8000/contacts/{contact_id}
```

---

# Reflektion

Det som var svårast i projektet var att:

* designa modellerna på ett flexibelt sätt
* strukturera projektet i olika lager

Det som hade förbättrats vid mer tid:

* riktig databas istället för JSON
* autentisering och användarhantering
* bättre felhantering
* tester
* dependency injection samt repository pattern
* async implementation

Projektet gav en bättre förståelse för:

* REST API-design
* FastAPI
* Pydantic
* repository pattern
* validering
* separation of concerns
