from re import I
from sre_constants import SUCCESS
from tkinter.messagebox import NO
from wsgiref.util import request_uri
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None
    

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None
    
inventory = {}

#Below code is to create endpoints 
# @app.get("/")

# def home():
#     return {"Data":"Testing"}

# @app.get("/about")
# def about():
#     return {"Data":"About"}

## PATH PARAMETER AND QUERY PARAMETER

@app.get("/get_item/{item_id}")
def get_item(item_id: int = Path(None,description="The ID of the item you'd like to view.") ):
    return inventory[item_id]

@app.get("/get_by_name")
def get_item(*, name:Optional[str] =None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code= 404, detail="Item name not found.")



### REQUEST BODY AND POST METHOD

@app.post("/create-item/{item_id}")
def create_item(item_id:int,item : Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exixts.")
    
    inventory[item_id]= item
    return inventory[item_id]
        
#### PUT METHOD
@app.put("/update-item/{item_id}")
def update_item(item_id:int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code= 404, detail="Item id doest not exists.")
    
    if item.name!= None:
        inventory[item_id].name = item.name
        
    if item.price!= None:
        inventory[item_id].price = item.price
        
    if item.brand!= None:
        inventory[item_id].brand = item.brand
    
    return inventory[item_id]
    

#### DELETE ITEM
@app.delete("/delete-item")
def delete_item(item_id : int = Query(..., description="The ID of the item to be deleted.")):
    if item_id not in inventory:
        raise HTTPException(status_code= 404, detail="Item name not found.")
    
    del inventory[item_id]
    return {"Success" : "Item deleted!!"}
