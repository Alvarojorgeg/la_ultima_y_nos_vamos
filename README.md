# La Última y Nos Vamos - Plataforma de Votaciones Interactivas

Plataforma interactiva para crear, votar y gestionar encuestas, con emisión de NFTs como comprobantes de voto y un asistente virtual. ¡Incluye integración con bases de datos modernas como Neo4j, MongoDB y Firebase!

---

## Características principales

- Creación y votación de encuestas (simples y múltiples)
- Emisión de tokens NFT por voto
- Gestión de usuarios y autenticación segura
- CLI interactiva y UI web con Gradio
- Asistente virtual (chatbot)
- **Integración con Neo4j:** registro de relaciones de votos en grafo
- **Integración con MongoDB:** persistencia alternativa de encuestas
- **Integración con Firebase:** almacenamiento en la nube de encuestas

---

## Instalación

```bash
pip install -r requirements.txt
```

---

## Integraciones destacadas

- **Neo4j:** Consulta y registra relaciones de votos entre usuarios y encuestas en un grafo ([`Neo4jEncuestaGraph`](src/integrations/neo4j_repo.py))
- **MongoDB:** Guarda y consulta encuestas en una base de datos NoSQL ([`MongoEncuestaRepository`](src/integrations/mongo_repo.py))
- **Firebase:** Almacena encuestas en la nube usando Firestore ([`FirebaseDB`](src/integrations/firebase_service.py))

---

## Ejecución

**Modo CLI:**
```bash
python src/app.py
```

**Modo UI Gradio:**
```bash
python src/app.py --ui
```

---

## Estructura del Proyecto

```
la_ultima_y_nos_vamos/
├── src/
│   ├── app.py
│   ├── config.py
│   ├── controllers/
│   ├── integrations/
│   │   ├── mongo_repo.py
│   │   ├── neo4j_repo.py
│   │   └── firebase_service.py
│   ├── models/
│   ├── patterns/
│   ├── repositories/
│   ├── services/
│   └── ui/
├── la_ultima_y_nos_vamos/data/
├── tests/
├── requirements.txt
└── README.md
```

---

## Tecnologías

- Python 3.10+
- [Gradio](https://gradio.app/) (UI web)
- [Transformers](https://huggingface.co/transformers/) (chatbot)
- [bcrypt](https://pypi.org/project/bcrypt/) (hash de contraseñas)
- [pymongo](https://pymongo.readthedocs.io/) (**MongoDB**)
- [neo4j](https://neo4j.com/) (**Neo4j**)
- [firebase-admin](https://firebase.google.com/docs/admin/setup) (**Firebase**)


---

## Pruebas

```bash
pytest
```

---

## Créditos

Desarrollado por el equipo de La Última y Nos Vamos.