# src/repositories/mongo_repo.py
from pymongo import MongoClient

class MongoEncuestaRepository:
    def __init__(self, uri="mongodb://localhost:27017", db_name="encuestas_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["encuestas"]

    def guardar(self, encuesta_dict):
        self.collection.insert_one(encuesta_dict)

    def listar_todas(self):
        return list(self.collection.find())

# Simulación para el proyecto actual
# repo = MongoEncuestaRepository()
# repo.guardar(encuesta.to_dict())
