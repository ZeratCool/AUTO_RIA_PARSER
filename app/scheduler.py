import os
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from parser import AutoRiaScraper
from utils import dump_db
from app.database.engine import init_db

from config import START_URL, SCRAPING_CRON, DUMP_CRON, cron_to_kwargs


async def main():
    await init_db()
    scraper = AutoRiaScraper(start_url=f"{START_URL}?limit=99999999&page=")

    print('First parse:')

    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(scraper.start()), 'cron',
                      **cron_to_kwargs(SCRAPING_CRON))
    scheduler.add_job(dump_db, 'cron', **cron_to_kwargs(DUMP_CRON))
    scheduler.start()

    print("Scheduler запущен. Ctrl+C для остановки.")
    await asyncio.Event().wait()


def cron_to_kwargs(cron_str):
    fields = cron_str.split()
    return {'minute': fields[0], 'hour': fields[1], 'day': fields[2], 'month': fields[3], 'day_of_week': fields[4]}


if __name__ == "__main__":
    asyncio.run(main())
