# app/seeds/cli.py

import typer
import asyncio
from seeds import (
    seed_users, undo_users,
    seed_machines, undo_machines,
    # seed_parts, undo_parts,  # ❌ Temporarily disabled
    seed_images, undo_images,
    seed_faqs, undo_faqs,
    seed_testimonials, undo_testimonials
)
from config import settings

app = typer.Typer()

@app.command()
def all():
    asyncio.run(_seed_all())

async def _seed_all():
    if settings.ENVIRONMENT == 'production':
        typer.echo("Production environment detected. Undoing existing data before seeding...")
        await _undo_all()

    typer.echo("Seeding users...")
    await seed_users()

    typer.echo("Seeding machines...")
    await seed_machines()

    # typer.echo("Seeding parts...")       # ❌ Temporarily disabled
    # await seed_parts()                   # ❌ Temporarily disabled

    typer.echo("Seeding images...")
    await seed_images()

    typer.echo("Seeding FAQs...")
    await seed_faqs()

    typer.echo("Seeding testimonials...")
    await seed_testimonials()

    typer.echo("✅ Seeding complete!")

@app.command()
def undo():
    asyncio.run(_undo_all())

async def _undo_all():
    typer.echo("Undoing seeded data...")

    await undo_testimonials()
    await undo_faqs()
    await undo_images()

    # await undo_parts()  # ❌ Temporarily disabled

    await undo_machines()
    await undo_users()

    typer.echo("🗑️ Undo complete!")

if __name__ == "__main__":
    app()