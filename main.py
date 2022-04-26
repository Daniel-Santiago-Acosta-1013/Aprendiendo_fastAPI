from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"hello": "world"}


#Request and response Body

@app.post("/person/new")
def create_person():
    pass 