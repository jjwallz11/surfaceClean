# app/schemas/__init__.py

from .users import UserBase, UserCreate, UserUpdate, UserResponse
from .machines import MachineBase, MachineCreate, MachineUpdate, MachineResponse
from .parts import PartBase, PartCreate, PartUpdate, PartResponse
from .images import ImageBase, ImageCreate, ImageUpdate, ImageResponse
from .testimonials import TestimonialBase, TestimonialCreate, TestimonialUpdate, TestimonialResponse
from .faqs import FAQBase, FAQCreate, FAQUpdate, FAQResponse