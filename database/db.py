import os
import sqlite3

# Chemin absolu dynamique vers database/ShowDataX.db
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ShowDataX.db")


def init_db():
  """Initialise la base de données SQLite pour ShowDataX"""
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  # Création de la table des mesures météo et niveau d'eau
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            water_level REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

  conn.commit()
  conn.close()
  print(f"Base de données SQLite initialisée avec succès sur : {DB_PATH}")


if __name__ == "__main__":
  init_db()
