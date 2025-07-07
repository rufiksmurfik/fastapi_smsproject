from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

# GET /hello
@app.get("/hello")
def hello():
    return {"message": "GET работает!"}

# POST /sms (form-data)
@app.post("/sms")
def sms_form(text: str = Form(...)):
    return {"you_sent": text}

# Модель для JSON-запроса
class Item(BaseModel):
    text: str

# POST /json (JSON body)
@app.post("/json")
def sms_json(item: Item):
    return {"you_sent": item.text}
