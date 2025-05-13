from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
app=FastAPI()
   
@app.get("/myname/{name}")
async def myname(name):
    return f"Welcome {name}"
    
food_items={
    "indian":['samosa','Dosa'],
    "american":['Hot Dog','Apple pie'],
    "italain":['Ravioli','pizza']
}
class availablecusine(str, Enum):
    indian="indian",
    american="american",
    italian="italian"
@app.get("/get_items/{cusine}")
async def get_items(cusine:availablecusine):
    return food_items.get(cusine)
cupn_code={
1:"10%",
2:"20%",
3:"30%",
4:"40%"
}
@app.get("/get_cupn/{cupn_num}")
async def get_cupn(cupn_num:int):
        return {'Your Discount' :cupn_code.get(cupn_num)}
        
class Item(BaseModel):
    name:str
    price:float
    
"""import requests
create =("http://localhost:8000/blogg",requests.post,dict(json=dict(namee="phone",pricee="2000"))                                                                >>> create =("http://localhost:8000/create",requests.post,dict(json=dict(name="iphone",price="2000")))
url,method,data=create
r=method(url,**data)
print(r.json())"""


@app.post("/create")
async def create(item:Item):
    return {"data":f"Name is {item.name} and Price is {item.price}"}
    
class createI(BaseModel):
    namee:str
    pricee:float    

@app.post("/blogg")
async def blogg(c:createI):
    return "creating"