from flask import Flask, request, send_file, send_from_directory
import pandas as pd
from ics import Calendar, Event
from datetime import datetime

from ics.grammar.parse import ContentLine
from pandas.io.parsers.base_parser import DatetimeIndex
import pytz
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
CORS(app)


def remove_previous_calendar(ics_file):
    if os.path.exists(ics_file):
        os.remove(ics_file)


@app.route("/")
def index():
    if app.static_folder:
        return send_from_directory(app.static_folder, "index.html")
    else:
        return "Static folder not found", 500


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "Brak pliku", 400

    file = request.files["file"]
    if file.filename == "":
        return "Brak pliku", 400

    if file and file.filename and file.filename.endswith((".xlsx", ".xls")):
        try:
            df = pd.read_excel(
                file,
            )

            calendar = Calendar()
            poland_tz = pytz.timezone("Europe/Warsaw")

            for index, row in df.iterrows():
                if bool(pd.notna(row["Godzina rozpoczecia"])) and bool(
                    pd.notna(row["Godzina zakonczenia"])
                ):
                    event = Event()
                    event.name = str(row["Nazwa wydarzenia"])
                    start_dt = datetime.combine(
                        row["Data"],
                        row["Godzina rozpoczecia"],
                    )
                    start_dt = poland_tz.localize(start_dt)
                    end_dt = datetime.combine(
                        row["Data"],
                        row["Godzina zakonczenia"],
                    )
                    end_dt = poland_tz.localize(end_dt)
                    event.begin = start_dt
                    event.end = end_dt

                    if "Powtarzaj" in df.columns and pd.notna(row["Powtarzaj"]):
                        repeat_interval = str(row["Powtarzaj"]).strip().lower()

                        if repeat_interval == "dzień":
                            event.extra.append(ContentLine.parse("RRULE:FREQ=DAILY"))
                        elif repeat_interval == "tydzień":
                            event.extra.append(ContentLine.parse("RRULE:FREQ=WEEKLY"))
                        elif repeat_interval == "2 tydzień":
                            event.extra.append(ContentLine.parse("RRULE:FREQ=WEEKLY;INTERVAL=2"))
                        elif repeat_interval == "miesiąc":
                            event.extra.append(ContentLine.parse("RRULE:FREQ=MONTHLY"))
                    calendar.events.add(event)
            ics_file = "/tmp/kalendarz.ics"

            remove_previous_calendar(ics_file)

            with open(ics_file, "w") as f:
                f.writelines(calendar)
                print(f"Plik {ics_file} został zapisany.")

            return send_file(ics_file, as_attachment=True)

        except Exception as e:
            return "Wystąpił błąd podczas przetwarzania pliku", 500

    return "Niepoprawny format pliku", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)),debug=True)
