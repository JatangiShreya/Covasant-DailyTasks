from fastapi import FastAPI
app=FastAPI()

# @app.get("/hello")
# async def hello():
    # return "Welcome to FastAPI world"
    
    
@app.get("/myname/{name}")
async def myname(name)
    return f"Welcome {name}"
