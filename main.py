# python
from typing import Optional 
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# fastAPI 
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form, Header, Cookie

app = FastAPI()

#Models 

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Santiago"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Acosta"
        )
    age: int = Field(
        ...,
        gt=0,
        le=105,
        example=17
        )

    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None)

class Person(PersonBase):
    
    password: str = Field(..., min_length=8, example="esto es un ejemplo de contraña")

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(..., max_length= 20, example="Santiago2022")

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK 
    )
def home():
    return {"hello": "world"}


#Request and response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

# validaciones: Query Parameters 

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK 
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person name",
        description="Este es el nombre de la persona, este solo va entre 1 y 50 caracteres",
        example="Andrea" 
        ),
    age: str = Query(
        ...,
        title="Person age",
        description="Esta es la edad de la persona, es requerido",
        example=25
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
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    # Location: Location = Body(...)
):
    # results = person.dict()
    # results.update(Location.dict())
    return person

# Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers Parameters 

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent