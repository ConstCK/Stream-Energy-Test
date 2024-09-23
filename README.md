# Приложение на FastAPI и aiogram (Мои заметки)

* Скопируйте проект к себе на ПК при помощи: git clone https://github.com/ConstCK/Stream-Energy-Test.git
* Перейдите в папку проекта
* В терминале создайте виртуальное окружение (например python -m venv venv) и активируйте его (venv\scripts\activate)
* Установите все зависимости при помощи pip install -r requirements.txt
* Создайте файл .env в каталоге проекта и пропишите в нем настройки по примеру .env.example
* Создайте BOT_TOKEN при помощи Telegram BotFather 
* Запустите Docker-Desktop

## Запуск Docker-Desktop и контейнер с приложением:

**docker-compose up**

## Ссылка на бот в Telegram:

https://t.me/notes_stream_energy_bot

## Доступ к администрированию БД:

http://localhost:8888/

**_Используйте /start в Telegram для запуска бота и следуйте инструкциям на экране._**

_В проекте использовалось:
FastApi для backend
Uvicorn для сервера
SqlAlchemy для связи с БД
Pydentic для валидации и сериализации на стороне backend
Postgesql - БД
aiogram - для создания telegram бота
requests для запросов к энпоинтам сервера
slowapi - для контроля количества запросов
logging - для логирования
Docker-Desktop для контейнеризации_


