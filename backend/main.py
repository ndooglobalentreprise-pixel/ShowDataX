import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VortexIoT API", version="1.0")

# Configuration CORS pour autoriser le frontend à communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = "database/vortex.db"

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API VortexIoT ! Système opérationnel."}

@app.get("/measurements")
def get_measurements(limit: int = 50):
    """Récupère les dernières mesures météo enregistrées"""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, station_id, temperature, humidity, pressure, timestamp 
            FROM measurements 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        results = [dict(row) for row in rows]
        # On inverse pour afficher du plus ancien au plus récent sur le graphique
        return {"total": len(results), "data": list(reversed(results))}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))