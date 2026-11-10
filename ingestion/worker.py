import json
import sqlite3
import paho.mqtt.client as mqtt

# Configuration de la base de données
DB_NAME = "database/vortex.db"

# Configuration MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "vortex/meteo/data"

def save_to_db(data):
    """Enregistre les données reçues dans SQLite"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO measurements (station_id, temperature, humidity, pressure)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get("station_id", "unknown"),
            data.get("temperature"),
            data.get("humidity"),
            data.get("pressure")
        ))
        
        conn.commit()
        conn.close()
        print(f"Données enregistrées avec succès : {data}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement en bdd : {e}")

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback exécuté lors de la connexion au broker MQTT"""
    if rc == 0:
        print("Connecté avec succès au broker MQTT Mosquitto !")
        client.subscribe(MQTT_TOPIC)
        print(f"Abonné au topic : {MQTT_TOPIC}")
    else:
        print(f"Échec de la connexion, code d'erreur : {rc}")

def on_message(client, userdata, msg):
    """Callback exécuté lorsqu'un message est reçu sur le topic"""
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        print(f"Message reçu : {data}")
        save_to_db(data)
    except json.JSONDecodeError:
        print("Erreur : Le message reçu n'est pas un JSON valide.")

def main():
    # Initialisation du client MQTT (version CallbackAPIv2)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connexion au broker MQTT sur {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Boucle permanente pour écouter les messages
    client.loop_forever()

if __name__ == "__main__":
    main()