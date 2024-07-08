from src.common.db.sqlalchemy.models import Product
from src.products.dto import ProductDTO


class StrawberryProductConverter:
    @classmethod
    def convert(cls, dto: ProductDTO) -> Product:
        ...
