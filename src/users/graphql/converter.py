from src.products.graphql.converters.reviews import StrawberryReviewConverter
from src.users.dto import UserDTO
from src.users.graphql.schemas.queries import User


class StrawberryUserConverter:
    review_converter: StrawberryReviewConverter = StrawberryReviewConverter

    @classmethod
    def convert(cls, dto: UserDTO) -> User:
        reviews = {}
        data = dto.model_dump()
        if hasattr(dto, 'reviews'):
            reviews = [cls.review_converter.convert(p) for p in dto.reviews]
            data.pop('reviews')
        product = User(**data, _reviews=reviews)
        return product
