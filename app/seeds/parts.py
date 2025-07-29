# app/seeds/parts.py

import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db import AsyncSessionLocal, Base, engine
from models.parts import Part

async def seed_parts():
    # Ensure schema exists
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        parts = [
            Part(name="Pad Driver", description="20-inch pad driver for Tennant T300", price=89.99, quantity=5),
            Part(name="Squeegee Blade Set", description="Replacement squeegee blades for Tennant T600", price=49.95, quantity=10),
            Part(name="Brush Motor", description="High-torque brush motor compatible with T300/T600 models", price=149.99, quantity=3),
            Part(name="Battery Pack", description="US 125 deep cycle battery for floor scrubbers", price=299.99, quantity=8),
            Part(name="Water Filter", description="In-line water filter to keep solution tank clean", price=12.50, quantity=20),
            Part(name="Vacuum Hose", description="Flexible vacuum hose, 6 ft, fits multiple models", price=39.99, quantity=12),
            Part(name="Propane Tank", description="Standard LP tank for CS7010 model", price=89.00, quantity=4),
            Part(name="Brush Set", description="Heavy-duty brushes for Advance CS7010", price=129.50, quantity=6),
            Part(name="Control Panel Overlay", description="Replacement panel overlay for T16", price=59.99, quantity=2),
            Part(name="Solution Tank Cap", description="Cap with seal for solution tank (Tennant universal)", price=9.99, quantity=15),
        ]

        db.add_all(parts)
        await db.commit()
        print("🔧 Seeded parts")

async def undo_parts():
    async with AsyncSessionLocal() as db:
        await db.execute(text("DELETE FROM parts"))
        await db.commit()
        print("🗑️ Deleted all parts")

# Optional standalone runner
if __name__ == "__main__":
    asyncio.run(seed_parts())