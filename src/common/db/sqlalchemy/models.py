from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    reviews: Mapped[list['Review']] = relationship(
        back_populates='user', cascade='all, delete-orphan',
    )

    def __str__(self) -> str:
        return f'SQLAlchemy:User(id={self.id} username={self.username})'

    def as_dict(self) -> dict[str, Any]:
        data = {
            'username': self.username,
            'id': self.id,
        }
        return data


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship()
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped['Product'] = relationship()

    def __str__(self) -> str:
        return (
            f'SQLAlchemy:Review(id={self.id} content={self.content}'
            f'user_id={self.user_id} product_id={self.product_id})'
        )

    def as_dict(self) -> dict[str, Any]:
        data = {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'product_id': self.product_id,
        }
        return data


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column()
    reviews: Mapped[list['Review']] = relationship(back_populates='product')

    def __str__(self) -> str:
        return f'SQLAlchemy:Product(id={self.id} title={self.title} description={self.description})'

    def as_dict(self) -> dict[str, Any]:
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }
        return data
