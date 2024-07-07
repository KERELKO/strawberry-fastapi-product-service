from src.products.dto import ReviewDTO
from src.products.graphql.schemas.reviews.queries import Review


class StrawberryReviewConverter:
    @classmethod
    def convert(cls, dto: ReviewDTO) -> Review:
        from src.products.graphql.schemas.products.queries import Product
        from src.users.graphql.schemas.queries import User

        data = dto.model_dump()
        product_data = {}
        user_data = {}
        if 'user' in data:
            _user_id = data.pop('user_id')
            _user = User(**data.pop('user'))
            user_data = {'_user': _user, '_user_id': _user_id}
        if 'product' in data:
            _product_id = data.pop('product_id')
            _product = Product(**data.pop('product'))
            product_data = {'_product': _product, '_product_id': _product_id}
        return Review(**product_data, **user_data, **data)
