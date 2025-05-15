from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from schemas.app_schema import AppCreate
from config.postgresdb_config import SessionLocal
from model.app_model import App
from service import app_service

router=APIRouter()
def get_db():
    db=SessionLocal()
   return db
@router.post("/apps/")
def create_app(app_data:AppCreate,db:Session=Depends(get_db)):
    db_app=App(name=app_data.name,description=app_data.description)
    return app_service.create(db=db,app=db_app)

@router.get("/apps/")
def get_al_apps(db:Session=Depends(get_db)):
    return app_service.getAll(db)
@router.get("/apps/{app_id}")
def get_app_by_id(app_id:int,db:Session=Depends(get_db)):
    app=app_service.getById(db,app_id)
    return app
@router.put("/apps/{app_id}")
def update_app(app_id:int,updated_data:dict,db:Session=Depends(get_db)):
    db_app=app_service.getById(db,app_id)
    return app_service.update(db,updated_data,db_app)
@router.delete("/apps/{app_id}")
def delete_app(app_id:int,db:Session=Depends(get_db)):
    dp_app=app_service.getById(db,app_id)
    app_service.delete(db,db_app)
