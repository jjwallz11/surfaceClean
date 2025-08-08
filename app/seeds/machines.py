# app/seeds/machines.py

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db import AsyncSessionLocal, Base, engine
from models.machines import Machine
from decimal import Decimal

async def seed_machines():
    # Ensure schema exists
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        machines = [
            Machine(
                name="Tennant T300 walk behind scrubber",
                price=3950.00,
                hours_used=Decimal("61.00"),
                condition="Used - like new",
                description="Tennant T300 brush assist 20 inch scrubber. Only 61 original hours use. All wear items new. New batteries with onboard charger. Works fine new. Free delivery in DFW area. Sweeper floor concrete advance nilfisk powerboss factory cat"
            ),
            Machine(
                name="Tennant T600",
                price=6500.00,
                hours_used=Decimal("203.00"),
                condition="Used - Good",
                description="Tennant T600 28 inch scrubber with new pad drivers. Only 203 original hours use. Great condition with slightly used higher capacity batteries. Has onboard charger. Works like new. Free delivery in DFW area. Sweeper scrubber floor concrete advance nilfisk powerboss factory cat Tennant"
            ),
            Machine(
                name="Advance Tennant CS7010 Sweeper Scrubber",
                price=20000.00,
                hours_used=Decimal("1229.00"),
                condition="Used - like New",
                description="Tennant Advance CS7010 lp powered sweeper scrubber with 1229 original hours use. Built September 2019. Kubota engine run on propane. Everything works as it should and all wear items are new or in good condition. Ready for delivery. Great machine at half what dealer would ask. Sweeps or scrubs separately or all together. Free delivery in Texas by me. OBO!! Tennant factory cat floor concrete powerboss sweeper scrubber"
            ),
            Machine(
                name="Tennant T16 Sweeper Scrubber",
                price=25000.00,
                hours_used=Decimal("48.00"),
                condition="Used - like New",
                description="2021 Tennant T16 with only 48 original hours use. Absolutely like new and works like it too. Just put new larger capacity US 125 batteries in it and installed manual battery fill system. This scrubber has the optional “pre sweep”. Machine can be operated as a sweeper, scrubber or both at the same time. Has lights, back up alarm and clean out hose on back of machine. Works perfectly and almost half price if you include the sweep system OBO free delivery in Texas. Powerboss advance nilfisk floor concrete factory cat sweeper scrubber"
            )
        ]

        db.add_all(machines)
        await db.commit()
        print("🚜 Seeded machines")

async def undo_machines():
    async with AsyncSessionLocal() as db:
        await db.execute(text("DELETE FROM machines"))
        await db.commit()
        print("🗑️ Deleted all machines")

# Optional standalone runner
if __name__ == "__main__":
    asyncio.run(seed_machines())