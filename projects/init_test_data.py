import asyncio

from app.utils.test_data.insert_data import insert_test_data
from app.database.session import SessionLocal

async def create_test_data() -> None:
    async with SessionLocal() as session:
            await insert_test_data(session)

async def main() -> None:
    await create_test_data()

if __name__ == "__main__":
    asyncio.run(main())