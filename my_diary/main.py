# main.py
from db.init_db import init_db
from ui.main_menu import main_menu

def main():
    init_db('notes.db')  # Inizializza il DB se non esiste
    main_menu()          # Avvia il menu interattivo

if __name__ == "__main__":
    main()
