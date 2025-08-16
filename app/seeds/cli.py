# app/seeds/cli.py

import asyncio
import typer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from utils.db import engine

# models
from models.users import User
from models.machines import Machine
from models.images import Image
from models.faqs import FAQ
from models.testimonials import Testimonial

# your existing seed/undo funcs
from seeds import (
    seed_users, undo_users,
    seed_machines, undo_machines,
    seed_images, undo_images,
    seed_faqs, undo_faqs,
    seed_testimonials, undo_testimonials
)

app = typer.Typer()
Session = async_sessionmaker(engine, expire_on_commit=False)

async def _has_rows(model) -> bool:
    async with Session() as s:
        res = await s.execute(select(model).limit(1))
        return res.scalar_one_or_none() is not None

# === export this for main.py ===
async def seed_all_async():
    if not await _has_rows(User):
        typer.echo("Seeding users…"); await seed_users()
    else:
        typer.echo("Users present — skipping.")

    if not await _has_rows(Machine):
        typer.echo("Seeding machines…"); await seed_machines()
    else:
        typer.echo("Machines present — skipping.")

    if not await _has_rows(Image):
        typer.echo("NOT Seeding images…")
    else:
        typer.echo("Images present — skipping.")

    if not await _has_rows(FAQ):
        typer.echo("Seeding FAQs…"); await seed_faqs()
    else:
        typer.echo("FAQs present — skipping.")

    if not await _has_rows(Testimonial):
        typer.echo("Seeding testimonials…"); await seed_testimonials()
    else:
        typer.echo("Testimonials present — skipping.")

    typer.echo("✅ Seeding complete (idempotent).")

@app.command()
def all():
    asyncio.run(seed_all_async())

@app.command()
def undo():
    asyncio.run(_undo_all())

async def _undo_all():
    typer.echo("Undoing seeded data…")
    await undo_testimonials()
    await undo_faqs()
    await undo_images()
    await undo_machines()
    await undo_users()
    typer.echo("🗑️ Undo complete!")

if __name__ == "__main__":
    app()