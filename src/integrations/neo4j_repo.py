# src/repositories/neo4j_repo.py
from neo4j import GraphDatabase

class Neo4jEncuestaGraph:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def registrar_voto(self, username, encuesta_id):
        with self.driver.session() as session:
            session.run(
                "MERGE (u:User {name: $username}) "
                "MERGE (e:Encuesta {id: $encuesta_id}) "
                "MERGE (u)-[:VOTO]->(e)",
                username=username,
                encuesta_id=encuesta_id
            )

# Simulación para integrar al votar:
# graph = Neo4jEncuestaGraph()
# graph.registrar_voto("alvaro", "encuesta123")
