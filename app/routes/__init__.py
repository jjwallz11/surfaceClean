# app/api/__init__.py

from fastapi import APIRouter
from .auth_routes import router as auth_router
from .users_routes import router as users_router
from .machines_routes import router as machines_router
from .images_routes import router as images_router
from .testimonials_routes import router as testimonials_router
from .faqs_routes import router as faqs_router

router = APIRouter()

router.include_router(auth_router, prefix="/api", tags=["Auth"])
router.include_router(users_router, prefix="/api/users", tags=["Users"])
router.include_router(machines_router, prefix="/api/machines", tags=["Machines"])
router.include_router(images_router, prefix="/api/images", tags=["Images"])
router.include_router(testimonials_router, prefix="/api/testimonials", tags=["Testimonials"])
router.include_router(faqs_router, prefix="/api/faqs", tags=["FAQs"])