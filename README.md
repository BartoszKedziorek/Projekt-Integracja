## Uruchomienie servera backend
```bash
mkdir Projekt_IS
cd Projekt_Is
git init
git pull https://github.com/BartoszKedziorek/Projekt-Integracja.git
cd nodes/backend/
```
W katalogu "nodes/backend" należy utworzyć plik compose.env
Plik ten zawiera zmienne środowiskowe niezbędne do uruchomienia
serwera. Przykładowa zawartośc pliku compose.env:
```
DEST_DIR=data
DB_USERNAME=password
DB_PASSWORD=password
DB_HOSTNAME=127.0.0.1
DB_NAME=db
POSTGRES_PASSWORD=password
```
Po utworzeniu pliku **compose.env** i ustawieniu w nim zmiennych
środowiskowych należy wykonać polecenie:
```bash
docker compose up --build
```

Po mniej więcej minucie serwer powinien zostać uruchomiony. Poprawoność działania
Serwera można sprawdzić pod adresem:
```127.0.0.1:8001/api/schema/swagger-ui```<br /><br />
Powinna zostać wyświetlona **dokumentacja API** udostępnianego przez serwer

## Uruchomienie servera frontend
```bash
cd Projekt_Is
cd nodes/frontend/
npm start
```
