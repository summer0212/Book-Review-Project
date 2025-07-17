from flask import Blueprint
from flask_restx import Namespace, Resource, fields, Api
from .models import Book, Review, db
# from .import db
from .services import get_from_cache, BOOKS_CACHE_KEY,set_in_cache,invalidate_cache

# api = Namespace('books',description="Book and review related operations")
api_bp = Blueprint('api',__name__, url_prefix='/api')

api = Api(api_bp,
          title = 'Book Review API',
          versio ='1.0',
          description = 'A simple API for managing books and reviews.',
          doc='/doc')

books_namespace = api.namespace('books',description = 'Book related operations')

book_model = books_namespace.model("Book",{
    'id': fields.Integer(readonly = True, description = 'The book unique identifier'),
    'title' : fields.String(required = True, description = "The book title"),
    'author' : fields.String(required=True, description='The book author')
})

review_model = books_namespace.model("Review",{
    'id': fields.Integer(readonly=True, description='The review unique identifier'),
    'content': fields.String(required=True, description='The content of the review'),
    'book_id': fields.Integer(readonly=True, description='The ID of the book this review belongs to')
})

review_input_model = books_namespace.model("ReviewInput",{
    'content':fields.String(required=True, description = "The content of the reviews")
})

@books_namespace.route('/')
class BookList(Resource):
    
    @books_namespace.doc('list_books')
    @books_namespace.marshal_list_with(book_model)
    def get(self):
         # 1. First, try to fetch from cache
        cached_books = get_from_cache(BOOKS_CACHE_KEY)
        if cached_books:
            print("CACHE HIT!")
            
            return cached_books
        # 2. If it's a cache miss, fetch from DB
        print("CACHE MISS! Fetching from DB.")
        books = Book.query.all()
         # Convert the list of Book objects to a list of dictionaries for caching
        books_dict = [book.to_dict() for book in books]
        
        # 3. Populate the cache for next time
        set_in_cache(BOOKS_CACHE_KEY, books_dict)
        
        return books_dict
    
    
    @books_namespace.doc('create_book')
    @books_namespace.expect(book_model, validate=True)
    @books_namespace.marshal_with(book_model,code=200)
    def post(self):
        data = books_namespace.payload

        # Checking if the book already exists
        if Book.query.filter_by(title=data['title']).first():
            books_namespace.abort(400, f"Book with title '{data['title']}'already exists.")

        new_book = Book(title = data['title'], author = data['author'])
        db.session.add(new_book)
        db.session.commit()

        # Invalidate the cache because the list of books has changed
        invalidate_cache(BOOKS_CACHE_KEY)
        return new_book,201
    
# To Get the Book as per id and create Review as per Book id
@books_namespace.route('/<int:book_id>/reviews')
@books_namespace.param('book_id','The book identifier')
class ReviewList(Resource):
    @books_namespace.doc('get_reviews_for_book')
    @books_namespace.marshal_list_with(review_model)
    def get(self,book_id):
        book = Book.query.get_or_404(book_id,description=f"Book with id {book_id} not found")
        return book.reviews
    
    @books_namespace.doc('add_review_to_book')
    @books_namespace.expect(review_input_model, validate=True)
    @books_namespace.marshal_with(review_model, code=201)
    def post(self, book_id):
        """Add a new review to a specific book"""
        book = Book.query.get_or_404(book_id, description=f"Book with id {book_id} not found.")
        data = books_namespace.payload
        
        new_review = Review(content=data['content'], book_id=book.id)
        db.session.add(new_review)
        db.session.commit()
        
        return new_review, 201