import asyncio

from app.database.session import SessionLocal
from app.database.test_data import insert_test_data


async def create_test_data() -> None:
    async with SessionLocal() as session:
        await insert_test_data(session)


async def main() -> None:
    await create_test_data()


if __name__ == "__main__":
    asyncio.run(main())
