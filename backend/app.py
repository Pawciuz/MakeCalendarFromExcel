from flask import Flask, request, send_file, send_from_directory
import pandas as pd
from ics import Calendar, Event
from datetime import datetime
import pytz
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Brak pliku", 400

    file = request.files['file']
    if file.filename == '':
        return "Brak pliku", 400

    if file and file.filename.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file)

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

        ics_file = 'kalendarz.ics'
        with open(ics_file, 'w') as f:
            f.writelines(calendar)

        return send_file(ics_file, as_attachment=True)

    return "Niepoprawny format pliku", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
