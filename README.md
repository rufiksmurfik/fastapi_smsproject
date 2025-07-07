# FastAPI SMS Bot с OpenAI

Это простое FastAPI приложение, которое получает SMS через Twilio webhook, отправляет текст в OpenAI ChatGPT и возвращает ответ обратно через SMS.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения в файле `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
TWILIO_SID=your_twilio_account_sid_here
TWILIO_TOKEN=your_twilio_auth_token_here
TWILIO_NUMBER=your_twilio_phone_number_here
```

## Запуск

### Автоматический запуск (рекомендуется)

```bash
./start_webhook.sh
```

### Ручной запуск

1. Запустите FastAPI сервер:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. В другом терминале запустите ngrok:
```bash
ngrok http 8000
```

## Использование

Приложение предоставляет endpoint `/sms` для обработки Twilio webhooks.

### Настройка Twilio

1. **Получите ngrok URL:**
   - После запуска ngrok, скопируйте HTTPS URL (например: `https://abc123.ngrok.io`)
   - Полный webhook URL будет: `https://abc123.ngrok.io/sms`

2. **Настройте Twilio Console:**
   - Откройте [Twilio Console](https://console.twilio.com/)
   - Перейдите в **Phone Numbers** → **Manage** → **Active numbers**
   - Выберите ваш Twilio номер телефона
   - В разделе **Messaging** найдите **A message comes in**
   - Вставьте ваш webhook URL: `https://abc123.ngrok.io/sms`
   - Убедитесь, что метод установлен как **HTTP POST**
   - Нажмите **Save configuration**

3. **Тестирование:**
   - Отправьте SMS на ваш Twilio номер
   - Бот должен ответить через OpenAI ChatGPT
   - Проверьте логи в терминале для отладки

4. **Мониторинг:**
   - Откройте http://localhost:4040 для ngrok web interface
   - Проверьте http://localhost:8000/docs для FastAPI документации

## Исправленные ошибки

- Убран неправильный импорт `from .env import ...`
- Обновлен код для новой версии OpenAI API (v1+)
- Добавлена правильная инициализация OpenAI клиента
- Исправлен вызов `openai_client.chat.completions.create()` вместо устаревшего `openai.ChatCompletion.create()`
- Улучшена обработка переменных окружения
