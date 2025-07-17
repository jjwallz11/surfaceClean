from .auth_routes import router as auth_router
from .users_routes import router as users_router
from .machines_routes import router as machines_router
from .parts_routes import router as parts_router
from .images_routes import router as images_router
from .testimonials_routes import router as testimonials_router
from .faqs_routes import router as faqs_router

__all__ = [
    "auth_router",
    "users_router",
    "machines_router",
    "parts_router",
    "images_router",
    "testimonials_router",
    "faqs_router"
]