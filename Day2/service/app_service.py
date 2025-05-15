from sqlalchemy.orm import Session
from model.app_model import App

def create(db:Session,app:App):
    db.add(app)
    db.commit()
    return app

def getAll(db:Session):
    return db.query(App).all()
def getById(db:Session,app_id:int):
    return db.query(App).filter(App.id==app_id).first()
def update(db:Session,app_data:dict,db_app:App):
    for key,value in app_data.items():
        setattr(db_app,key,value)
    db.commit()
    return db_app
def delete(db:Session,app_id:int):
    db.delete(App).filter(App.id==app.id).first()
    db.commit()
