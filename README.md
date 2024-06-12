# Uruchomienie aplikacji
W celu uruchomienia aplikacji należy uruchomić serwer back-endu oraz serwer front-endu.
Instrukcje do uruchomienia serwerów zostały przedstawione poniżej. Do uruchomienia backendu niezbędny
jest plik compose.env ze zmiennymi środowiskowymi.

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
DEST_DIR="sample_dir"
DB_USERNAME='projekt_integracja'
DB_PASSWORD='projekt_integracja'
DB_HOSTNAME='db'
DB_NAME='projekt_integracja'
POSTGRES_PASSWORD='projekt_integracja'
KAGGLE_USERNAME='kaggle_username'
KAGGLE_KEY='kaggle_key'
DATASETS_SOURCE_FILE='sample_dir'
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@admin.com
DJANGO_SUPERUSER_USERNAME=admin
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
