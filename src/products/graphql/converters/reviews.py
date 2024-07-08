from src.products.dto import ReviewDTO
from src.products.graphql.schemas.reviews.queries import Review
from src.common.base.dto import Entity


class StrawberryReviewConverter:
    @classmethod
    def convert(cls, dto: ReviewDTO) -> Review:
        from src.products.graphql.schemas.products.queries import Product
        from src.users.graphql.schemas.queries import User

        data = dto.model_dump()
        product_data = {}
        user_data = {}

        if 'user_id' in data:
            user_data['_user_id'] = data.pop('user_id')
        if 'product_id' in data:
            product_data['_product_id'] = data.pop('product_id')

        if Entity.USER in data:
            _user = User(**data.pop('user'))
            user_data['_user'] = _user
        if Entity.PRODUCT in data:
            _product = Product(**data.pop('product'))
            product_data['_product'] = _product

        return Review(**product_data, **user_data, **data)
