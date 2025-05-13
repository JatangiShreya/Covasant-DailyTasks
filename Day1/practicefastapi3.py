from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, create_engine,select


app = FastAPI()


class Blog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    body: str


engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)


@app.post("/blog")
async def create_blog(blog: Blog):
    with Session(engine) as session:
        session.add(blog)
        session.commit() 
        return blog
        
@app.get("/blogs")
async def get_all_blogs():
    with Session(engine) as session:
        blogs = session.exec(select(Blog)).all()
        return blogs