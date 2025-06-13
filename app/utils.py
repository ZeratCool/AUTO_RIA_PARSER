import subprocess
from datetime import datetime
from sqlalchemy import text

def dump_db():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dump/dump_{ts}.sql"
    subprocess.run([
        "pg_dump",
        "-U", "postgres",
        "-h", "db",
        "-f", filename,
        "autoria"
    ], check=True)
    print(f"БД сохранена в {filename}")

async def clear_table(self):
    async with self.db_session.begin():
        await self.db_session.execute(text("TRUNCATE TABLE cars"))
    print("Таблица cars очищена")