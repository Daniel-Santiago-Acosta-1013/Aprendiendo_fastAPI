# python
from lib2to3.pytree import Base
from typing import Optional 

#Pydantic
from pydantic import BaseModel

# fastAPI 
from fastapi import FastAPI
from fastapi import Body, Query, Path


#Models 

class Location(BaseModel):
    city: str
    state: str
    country: str

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
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person name",
        description="Este es el nombre de la persona, este solo va entre 1 y 50 caracteres" 
        ),
    age: str = Query(
        ...,
        title="Person age",
        description="Esta es la edad de la persona, es requerido"
        )
): 

    return {name: age}

# validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def showw_person(
    person_id: int = Path(..., gt=0)
):
    return {person_id: "It exists!"}

# Validaciones: Request Body 

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., 
        title="Person ID",
        description="Este es el ID de la persona",
        gt=0
    ),
    person: Person = Body(...),
    Location: Location = Body(...)
):
    results = person.dict()
    results.update(Location.dict())
    return results