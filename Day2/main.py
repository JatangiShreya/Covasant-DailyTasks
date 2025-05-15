from fastapi import FastAPI
from routes import app_routes
from config.postgresdb_config import Base, engine
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(app_routes.router)
