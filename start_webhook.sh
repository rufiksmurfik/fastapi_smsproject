#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Запуск FastAPI приложения и ngrok для Twilio webhook...${NC}"

# Проверяем, что .env файл настроен
if [ ! -f .env ]; then
    echo -e "${RED}❌ Файл .env не найден!${NC}"
    echo "Создайте файл .env с вашими API ключами:"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo "TWILIO_SID=your_twilio_account_sid_here"
    echo "TWILIO_TOKEN=your_twilio_auth_token_here"
    echo "TWILIO_NUMBER=your_twilio_phone_number_here"
    exit 1
fi

# Запускаем FastAPI приложение в фоне
echo -e "${YELLOW}📡 Запуск FastAPI сервера на порту 8000...${NC}"
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Ждем несколько секунд для запуска сервера
sleep 3

# Проверяем, что сервер запустился
if curl -s http://localhost:8000/docs > /dev/null; then
    echo -e "${GREEN}✅ FastAPI сервер успешно запущен!${NC}"
else
    echo -e "${RED}❌ Ошибка запуска FastAPI сервера${NC}"
    kill $FASTAPI_PID
    exit 1
fi

# Запускаем ngrok
echo -e "${YELLOW}🌐 Запуск ngrok для проброса webhook...${NC}"
ngrok http 8000 &
NGROK_PID=$!

echo -e "${GREEN}✅ Все запущено!${NC}"
echo -e "${YELLOW}📋 Следующие шаги:${NC}"
echo "1. Откройте ngrok web interface: http://localhost:4040"
echo "2. Скопируйте HTTPS URL (например: https://abc123.ngrok.io)"
echo "3. Добавьте к URL путь /sms (например: https://abc123.ngrok.io/sms)"
echo "4. Вставьте полный URL в Twilio Console:"
echo "   - Перейдите в Twilio Console → Phone Numbers → Manage → Active numbers"
echo "   - Выберите ваш номер → Messaging → A message comes in → Webhook URL"
echo "   - Метод: HTTP POST"
echo ""
echo -e "${YELLOW}🛑 Для остановки нажмите Ctrl+C${NC}"

# Обработка сигнала для корректного завершения
trap 'echo -e "\n${YELLOW}🛑 Остановка сервисов...${NC}"; kill $FASTAPI_PID $NGROK_PID; exit 0' INT

# Ждем завершения
wait
