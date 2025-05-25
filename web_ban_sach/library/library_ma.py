from .extension import ma
from .model import Books, Author, Category, User, Cart, Img, Hoa_Don


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class CatSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True


class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True

class ImgSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Img
        load_instance = True

# class BorrowSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'book_id', 'student_id', 'borrow_date', 'return_date')


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Books
        load_instance = True

# class ImageSchema(ma.Schema):
#     class Meta:
#         fields = ('id')

class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True

class Hoa_DonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hoa_Don
        load_instance = True

class AfterCartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hoa_Don
        load_instance = True
        fields = ('id', 'user_id', 'book_id', 'quantity', 'price', 'information')