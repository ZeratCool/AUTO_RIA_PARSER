import aiohttp
import asyncio
import re
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, Dict
from sqlalchemy.exc import IntegrityError
from database.models import Car
from database.engine import SessionLocal
import pandas as pd
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.WARNING,  # можно сменить на INFO или DEBUG для более подробного вывода
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("scraper.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoRiaScraper:
    def __init__(self, start_url: str):
        self.start_url = start_url.rstrip('/')
        self.visited = set()
        self.session = None
        self.results = []
        self.db_session = SessionLocal()

    async def start(self):
        headers = {
            "User-Agent": "Mozilla/5.0 ...",
            "Accept-Language": "en-US,en;q=0.9",
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            self.session = session
            page = 0
            while True:
                url = f"{self.start_url}{page}"
                logger.info(f"Парсим страницу {page}...")
                html = await self._fetch(url)
                soup = BeautifulSoup(html, "lxml")
                car_links = soup.select("a.m-link-ticket[href]")
                if not car_links:
                    logger.info("Пустая страница, заканчиваем парсинг.")
                    break
                for a in car_links:
                    url_car = a['href']
                    if url_car not in self.visited:
                        self.visited.add(url_car)
                        data = await self._scrape_car(url_car)
                        if data:
                            logger.info(f"Собрали: {data['title']}")
                page += 1

        df = pd.DataFrame(self.results)
        df.to_csv('cars_data.csv', index=False, encoding='utf-8-sig')
        logger.info("✅ Данные сохранены в cars_data.csv")

    async def _scrape_car(self, url: str) -> Optional[Dict]:
        aid = url.rstrip('/').split('_')[-1].split('.')[0]
        api = await self._get_api(aid)
        details = await self._get_car_details(aid)
        if not details or not api:
            return None
        phone_raw = await self._get_phone(aid, api['hash'], api['expires'])
        phone = self._normalize_phone(phone_raw)
        html = await self._fetch(url)
        soup = BeautifulSoup(html, "lxml")

        def txt(sel):
            el = soup.select_one(sel)
            return el.text.strip() if el else None

        od = re.sub(r'[^\d.]', '', api['race'])
        odometer = int(float(od) * 1000) if od else None
        vin = details.get("VIN")
        car_number_raw = txt(".state-num")
        car_number = car_number_raw.strip()[:10] if car_number_raw else None

        data = {
            "url": url,
            "title": f"{api['marka']} {api['model']}",
            "price_usd": int(api['price_usd']),
            "odometer": odometer,
            "username": txt(".seller_info_name, .seller_info"),
            "phone_number": phone,
            "image_url": api['photo_url'],
            "images_count": len(details.get("photo", [])) if details.get("photo") else 1,
            "car_number": car_number,
            "car_vin": vin,
            "datetime_found": datetime.utcnow().isoformat()
        }
        self.results.append(data)
        await self._save_to_db(data)
        return data

    def _normalize_phone(self, phone_raw: Optional[str]) -> Optional[str]:
        if not phone_raw:
            return None
        digits = re.sub(r'[^\d+]', '', phone_raw)
        return '+380' + digits.lstrip('0') if not digits.startswith('+') else digits

    async def _get_car_details(self, aid: str) -> Optional[Dict]:
        part1, part2, part3 = aid[:4], aid[:6], aid
        url = f"https://auto.ria.com/uk/bu/blocks/json/{part1}/{part2}/{part3}?lang_id=4"
        try:
            async with self.session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    logger.warning(f"Failed to get details JSON for {aid}: Status {resp.status}")
                    return None
                try:
                    return await resp.json()
                except Exception as e:
                    text = await resp.text()
                    logger.error(f"Error parsing JSON for {aid}: {e}, response text: {text}")
                    return None
        except Exception as e:
            logger.error(f"Request failed for {aid}: {e}")
            return None

    async def _get_api(self, aid: str) -> Optional[Dict]:
        url = f"https://auto.ria.com/demo/bu/mainPage/rotator/item/{aid}?type=bu&langId=4"
        try:
            r = await self.session.get(url)
            if r.status != 200:
                return None
            d = await r.json()
            sec = d.get("userSecure", {})
            if not sec.get("hash"):
                return None
            return {
                "marka": d.get("marka"),
                "model": d.get("model"),
                "price_usd": d.get("USD", "").replace(" ", ""),
                "race": d.get("race"),
                "photo_url": d.get("photoBig"),
                "hash": sec.get("hash"),
                "expires": sec.get("expires")
            }
        except Exception as e:
            logger.error(f"Failed to fetch API data for {aid}: {e}")
            return None

    async def _get_phone(self, aid: str, h: str, e: int) -> Optional[str]:
        url = f"https://auto.ria.com/users/phones/{aid}?hash={h}&expires={e}"
        try:
            r = await self.session.get(url)
            if r.status == 200:
                return (await r.json()).get("formattedPhoneNumber")
        except Exception as e:
            logger.warning(f"Failed to get phone for {aid}: {e}")
        return None

    async def _fetch(self, url: str) -> str:
        delay = 1
        for attempt in range(3):
            try:
                async with self.session.get(url, timeout=10) as r:
                    r.raise_for_status()
                    return await r.text()
            except (aiohttp.ClientError, asyncio.TimeoutError, OSError) as e:
                logger.warning(f"⚠️ Ошибка соединения (попытка {attempt + 1}/3): {e}")
                await asyncio.sleep(delay)
                delay *= 2
        logger.error(f"❌ Не удалось получить URL: {url}")
        return ""

    async def _save_to_db(self, data: dict):
        dt_found = data['datetime_found']
        if isinstance(dt_found, str):
            dt_found = datetime.fromisoformat(dt_found)

        car = Car(
            url=data['url'],
            title=data['title'],
            price_usd=data['price_usd'],
            odometer=data['odometer'],
            username=data['username'],
            phone_number=data['phone_number'],
            image_url=data['image_url'],
            images_count=data['images_count'],
            car_number=data['car_number'],
            car_vin=data['car_vin'],
            datetime_found=dt_found
        )
        try:
            self.db_session.add(car)  # Если это AsyncSession, то должно быть: await self.db_session.add(car)
            await self.db_session.commit()
        except IntegrityError:
            await self.db_session.rollback()
            logger.warning(f" Запис з url {data['url']} вже існує в БД")
        except Exception as e:
            await self.db_session.rollback()
            logger.error(f" Помилка при записі в БД: {e}")