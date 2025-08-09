from rp_comm.client import choice
import asyncio

async def periodic_choice():
    while True:
        await choice()
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(periodic_choice())