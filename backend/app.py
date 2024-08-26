from flask import Flask, request, send_file, send_from_directory
import pandas as pd
from ics import Calendar, Event
from datetime import datetime
import pytz
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)

def remove_previous_calendar(ics_file):
    """Usuwa plik kalendarza, jeśli istnieje, lub tworzy pusty plik."""
    if os.path.exists(ics_file):
        os.remove(ics_file)
        print(f'Plik {ics_file} został usunięty.')
    else:
        print(f'Plik {ics_file} nie istnieje. Zostanie utworzony nowy plik.')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Brak pliku", 400

    file = request.files['file']
    if file.filename == '':
        return "Brak pliku", 400

    if file and file.filename.endswith(('.xlsx', '.xls')):
        try:
            # Odczyt pliku Excel
            df = pd.read_excel(file)

            # Tworzenie kalendarza
            calendar = Calendar()
            poland_tz = pytz.timezone('Europe/Warsaw')

            for index, row in df.iterrows():
                if pd.notna(row['Godzina rozpoczecia']) and pd.notna(row['Godzina zakonczenia']):
                    event = Event()
                    event.name = row['Nazwa wydarzenia']
                    start_dt = datetime.combine(row['Data'], row['Godzina rozpoczecia'])
                    start_dt = poland_tz.localize(start_dt)
                    end_dt = datetime.combine(row['Data'], row['Godzina zakonczenia'])
                    end_dt = poland_tz.localize(end_dt)
                    event.begin = start_dt
                    event.end = end_dt
                    calendar.events.add(event)

            # Używanie katalogu tymczasowego
            ics_file = '/tmp/kalendarz.ics'
            # Usuwanie poprzedniego pliku lub tworzenie nowego
            remove_previous_calendar(ics_file)

            # Zapisywanie nowego pliku kalendarza
            with open(ics_file, 'w') as f:
                f.writelines(calendar)
                print(f'Plik {ics_file} został zapisany.')

            # Wysyłanie pliku jako załącznika
            return send_file(ics_file, as_attachment=True)

        except Exception as e:
            print(f'Wystąpił błąd: {e}')
            return "Wystąpił błąd podczas przetwarzania pliku", 500

    return "Niepoprawny format pliku", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
