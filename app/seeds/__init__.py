# seeds/__init__.py

from .users import seed_users
from .machines import seed_machines
from .parts import seed_parts
from .images import seed_images
from .faqs import seed_faqs
from .testimonials import seed_testimonials

__all__ = [
    "seed_users",
    "seed_machines",
    "seed_parts",
    "seed_images",
    "seed_faqs",
    "seed_testimonials"
]