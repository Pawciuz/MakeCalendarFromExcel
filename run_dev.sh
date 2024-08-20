#!/bin/bash

# Funkcja do zatrzymywania procesów
stop_processes() {
  echo "Stopping processes..."
  kill $backend_pid
  kill $frontend_pid
  wait $backend_pid 2>/dev/null
  wait $frontend_pid 2>/dev/null
  echo "Both backend and frontend have been stopped."
  exit 0
}

# Przechwytywanie sygnału Ctrl+C
trap stop_processes SIGINT

# Uruchom backend w Pythonie
echo "Starting Python backend..."
cd backend
python app.py &
backend_pid=$!

# Uruchom frontend w React
echo "Starting React frontend..."
cd ../frontend
npm start &
frontend_pid=$!

# Poczekaj na zakończenie obu procesów
wait $backend_pid
wait $frontend_pid