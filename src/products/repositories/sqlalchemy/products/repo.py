from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.sqlalchemy.models import Product
from src.products.dto import ProductDTO
from src.products.repositories.base import AbstractProductRepository


class SQLAlchemyProductRepository(AbstractProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, id: int) -> ProductDTO | None:
        stmt = select(Product).where(Product.id == id)
        result = await self.session.execute(stmt)
        product = result.scalars().first()
        if not product:
            return None
        return ProductDTO(id=id, title=product.title, description=product.description)

    async def get_list(
        self,
        *fields: tuple[str],
        offset: int = 0,
        limit: int = 20,
    ) -> list[ProductDTO]:
        stmt = select(*[getattr(Product, f) for f in fields]).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return [ProductDTO(id=p.id, title=p.title, description=p.description) for p in result.all()]
