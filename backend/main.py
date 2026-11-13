import os
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Correction du titre pour afficher ShowDataX au lieu de VortexIoT
app = FastAPI(title="ShowDataX API", version="1.0")

# Configuration CORS pour autoriser le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemin absolu dynamique vers la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "ShowDataX.db")


def get_db_connection():
    """Ouvre une connexion propre à la base de données SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def read_root():
    # Correction du message de bienvenue
    return {"message": "Bienvenue sur l'API ShowDataX ! Système opérationnel."}


@app.get("/measurements")
def get_measurements(limit: int = 50):
    """Récupère les dernières mesures météo et niveau d'eau enregistrées"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, station_id, temperature, humidity, pressure, water_level, timestamp 
            FROM measurements 
            ORDER BY id DESC 
            LIMIT ?
        """,
        (limit,),
        )

        rows = cursor.fetchall()
        results = [dict(row) for row in rows]

        return {"total": len(results), "data": list(reversed(results))}

    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur de base de données: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
