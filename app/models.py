from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150) , nullable = False, unique = True)
    author = db.Column(db.String(100),nullable = False)

    reviews = db.relationship("Review", backref = "book", lazy = True, cascade = "all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author" : self.author
        }

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'),nullable = False, index=True)

    def to_dict(self):
        return {
            "id":self.id,
            "content": self.content,
            "book_id" : self.book_id
        }