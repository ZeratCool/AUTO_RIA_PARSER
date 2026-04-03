# 🚗 AutoRia Parser (Hybrid Edition)

Асинхронный парсер для сайта [auto.ria.com](https://auto.ria.com), который собирает данные о б/у авто, объединяя данные из HTML и JSON API. Поддерживает PostgreSQL, pandas CSV-экспорт, планировщик, логирование и работу в Docker.

---

## 📦 Возможности

- 📊 Сбор данных: `title`, `price_usd`, `odometer`, `phone_number`, `username`, `car_number`, `car_vin` и др.
- 🔄 Асинхронный обход всех страниц
- ⚡ Быстрый сбор данных из API (JSON) + доп. поля из HTML
- 📁 Сохранение: PostgreSQL + pandas CSV
- 📞 Получение телефона через API (`hash`, `expires`)
- ⏰ Планировщик через `APScheduler` (cron из `.env`)
- 🐳 Поддержка Docker и docker-compose

---

## 🧬 Структура данных

```json
{
  "url": "...",
  "title": "...",
  "price_usd": 9500,
  "odometer": 95000,
  "username": "Олег",
  "phone_number": "380631234567",
  "image_url": "...",
  "images_count": 1,
  "car_number": "AA 1234 XX",
  "car_vin": "WBAYA8C50ED825202",
  "datetime_found": "2025-06-13T12:00:00"
}
```

---

## 🚀 Быстрый старт (Docker)

1. Клонируй репозиторий:

```bash
git clone https://github.com/yourname/autorai-parser.git
cd autorai-parser
```

2. Создай `.env` файл:

```env
DB_NAME=autoria
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
START_URL=https://auto.ria.com/uk/car/used/
SCRAPING_CRON=0 12 * * *
DUMP_CRON=30 12 * * *
LOG_LEVEL=INFO
LOG_FILE=app.log
```

3. Запусти контейнер:

```bash
docker-compose up --build
```

---

##  Структура проекта

```
.
├── app/
│   ├── scraper.py
│   ├── scheduler.py
│   ├── database.py
│   ├── models.py
│   ├── logger.py
│   ├── utils.py
│   ├── config.py
│   └── main.py
├── dumps/
├── .env
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---



##  Команды

| Действие           | Команда                                                     |
|--------------------|-------------------------------------------------------------|
| Собрать контейнер  | `docker-compose build`                                      |
| Запустить          | `docker-compose up`                                         |
| Остановить         | `docker-compose down`                                       |
| Дамп БД вручную    | `docker-compose exec app python utils.py`                  |
| Создать БД вручную | `docker-compose exec db psql -U postgres -c "CREATE DATABASE autoria;"` |

---

## 🧑‍💻 Автор

[ZeratCool](https://github.com/ZeratCool)

---



