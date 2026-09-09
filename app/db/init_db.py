import asyncio
import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    print("Try to connect to db :^ ")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("Try to read schema.sql...")
        with open("db/schema.sql", "r") as file:
            schema = file.read()
        
        print("Create tables...")
        await conn.execute(schema)
        print("Comgratulations!")
        
    except asyncpg.exceptions.DuplicateTableError:
        print("Tables have already existed. Creations passed.")
    except Exception as e:
        print(f"Pu-pu-pu, we have some problems here: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db())