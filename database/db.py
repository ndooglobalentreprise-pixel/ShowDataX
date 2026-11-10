import sqlite3

DB_NAME = "vortex.db"

def init_db():
    """Initialise la base de données SQLite pour VortexIoT"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Création de la table des mesures météo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données SQLite initialisée avec succès !")

if __name__ == "__main__":
    init_db()