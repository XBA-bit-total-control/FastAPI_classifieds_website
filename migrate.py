from database import open_orm, close_orm
import asyncio


async def main():
    await open_orm()
    await close_orm()


try:
    asyncio.run(main())
    print("The 'users' and 'advertisements' tables have been successfully created")
except Exception as err:
    print(f"Tables were not created due to an error {err.__class__.__name__}")
    raise err
