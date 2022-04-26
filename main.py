# python
from lib2to3.pytree import Base
from typing import Optional 

#Pydantic
from pydantic import BaseModel

# fastAPI 
from fastapi import FastAPI
from fastapi import Body, Query


#Models 
class Person(BaseModel):
    first_name: str 
    last_name: str 
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

app = FastAPI()

@app.get("/")
def home():
    return {"hello": "world"}


#Request and response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# validaciones: Query Parameters 

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...)
): 

    return {name: age}