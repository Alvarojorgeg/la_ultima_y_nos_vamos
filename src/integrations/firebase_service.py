# src/integrations/firebase_service.py
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseDB:
    def __init__(self, cred_path="firebase_key.json"):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def guardar_encuesta(self, encuesta_dict):
        self.db.collection("encuestas").add(encuesta_dict)

# Simulación:
# firebase = FirebaseDB()
# firebase.guardar_encuesta(encuesta.to_dict())
