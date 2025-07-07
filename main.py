import os
from fastapi import FastAPI, Form, HTTPException, Request
from dotenv import load_dotenv
from twilio.rest import Client
from openai import OpenAI

load_dotenv()  # подтягиваем .env

# Получаем переменные окружения
openai_api_key = os.getenv("OPENAI_API_KEY")
twilio_sid = os.getenv("TWILIO_SID")
twilio_token = os.getenv("TWILIO_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")

# Проверяем наличие всех необходимых переменных
if not all([openai_api_key, twilio_sid, twilio_token, twilio_number]):
    raise RuntimeError("Нет переменных окружения OpenAI / Twilio")

# Настраиваем OpenAI и Twilio клиентов
openai_client = OpenAI(api_key=openai_api_key)
twilio_client = Client(twilio_sid, twilio_token)

app = FastAPI()

@app.get("/")
async def root():
    """Корневой endpoint для проверки работоспособности"""
    return {"message": "FastAPI SMS Bot is running!", "endpoints": {"/sms": "Twilio webhook", "/docs": "API documentation"}}

@app.get("/sms")
async def sms_webhook_get(request: Request):
    """GET endpoint для проверки Twilio webhook"""
    # Получаем все query параметры для отладки
    query_params = dict(request.query_params)
    return {
        "status": "webhook is working", 
        "method": "GET",
        "query_params": query_params,
        "url": str(request.url)
    }

@app.post("/sms")
async def sms_webhook(
    Body: str = Form(...),                               # текст SMS
    From: str = Form(...),                               # номер отправителя
):
    """Получаем SMS → отправляем в ChatGPT → отвечаем той же SMS."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": Body}],
            temperature=0.7,
            max_tokens=120,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        # не валимся в молчании — сообщаем клиенту и логируем
        raise HTTPException(status_code=502, detail=f"OpenAI error: {e}")

    try:
        twilio_client.messages.create(
            body=reply,
            from_=twilio_number,
            to=From
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Twilio error: {e}")

    return {"status": "sent"}                            # 200 OK
