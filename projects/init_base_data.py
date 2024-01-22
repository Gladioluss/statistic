import asyncio

from app.database.init import insert_base_data
from app.database.session import SessionLocal

async def create_init_data() -> None:
    async with SessionLocal() as session:
            await insert_base_data(session)

async def main() -> None:
    await create_init_data()

if __name__ == "__main__":
    asyncio.run(main())