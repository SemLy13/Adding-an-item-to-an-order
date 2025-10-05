from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .category import Category  # noqa:
from .nomenclature import Nomenclature  # noqa:
from .client import Client  # noqa:
from .orders import Order, OrderItem  # noqa:
