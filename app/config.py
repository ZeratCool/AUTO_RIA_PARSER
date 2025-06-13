from dotenv import load_dotenv
import os

load_dotenv()

# DB_CONF
DB_NAME: str = os.getenv("DB_NAME", default='autoria')
DB_USERNAME: str = os.getenv("DB_USERNAME", default='postgres')
DB_PASSWORD: str = os.getenv("DB_PASSWORD", default='postgres')
DB_HOST: str = os.getenv("DB_HOST", default='db')
DB_PORT: str = os.getenv("DB_PORT", default='5432')

DB_URL: str = os.getenv(
    "DATABASE_URL",
    default=f'postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# PARSER_CONF
START_URL = os.getenv("START_URL", default="https://auto.ria.com/uk/car/used/")

# SHEDULER CONF
SCRAPING_CRON = os.getenv("SCRAPING_CRON", default="0 12 * * *")
DUMP_CRON = os.getenv("DUMP_CRON", default="30 12 * * *")


def cron_to_kwargs(cron_str):
    if not cron_str:
        raise ValueError("⛔ CRON-строка не найдена.")
    fields = cron_str.split()
    if len(fields) != 5:
        raise ValueError(f"Неверная CRON-строка: {cron_str}")
    return {
        'minute': fields[0],
        'hour': fields[1],
        'day': fields[2],
        'month': fields[3],
        'day_of_week': fields[4]
    }
