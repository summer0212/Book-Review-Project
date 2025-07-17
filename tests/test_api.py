import pytest
import json
from app import create_app
from app.models import db,Book
from config import TestingConfig
from unittest.mock import MagicMock

@pytest.fixture()
def test_client():
    app = create_app(config_class=TestingConfig)

   
    # app.redis_client = MagicMock()

    # with app.app_context():
    #     db.create_all()

    #     # client = app.test_client()

    #     yield  app.test_client()

    #     db.drop_all()

    
    with app.app_context():
        db.create_all()
        client = app.test_client()
        yield client
        db.session.remove()
        db.drop_all()

#  Unit test cases 
def test_create_book(test_client):
    # Testing the POST method 
    # 1. REquest Payload
    book_data =  {"title" : 'Test Book ', "author" : 'Test Author'}

    # 2. Make a POST request
    response = test_client.post('/api/books/',
                                data=json.dumps(book_data),
                                content_type='application/json')
    
    # 3. Check the response
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data['title'] == 'Test Book'
    assert response_data['author'] == 'Test Author'
    assert 'id' in response_data

    # # 4. Check if the book was actually saved to the database
    # book = Book.query.filter_by(title='Test Book').first()
    # assert book is not None
    # assert book.author == 'Test Author'

     #  Wrap the database check in the app context
    with test_client.application.app_context():
        book = Book.query.filter_by(title='Test Book').first()
        assert book is not None
        assert book.author == 'Test Author'


def test_get_all_books_empty(test_client):
    # Testing GET 
    response = test_client.get('/api/books/')
    
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert isinstance(response_data, list)
    assert len(response_data) == 0

# Integration test case

def test_get_books_cache_miss_integration(test_client, mocker):

    with test_client.application.app_context():
    
    
        book = Book(title='Cache Test Book', author='Cache Author')
        db.session.add(book)
        db.session.commit()


    mock_get_cache = mocker.patch('app.routes.get_from_cache', return_value=None)
    mock_set_cache = mocker.patch('app.routes.set_in_cache')
    
    # Make the GET request
    response = test_client.get('/api/books/')
    
    # Assertions
    assert response.status_code == 200
    
    # 1. Check that we tried to get from cache
    mock_get_cache.assert_called_once_with('all_books')
    
    # 2. Check that since it was a miss, we then tried to set the cache
    mock_set_cache.assert_called_once()
    
    # 3. Check that the response contains the book we created
    response_data = json.loads(response.data)
    assert len(response_data) == 1
    assert response_data[0]['title'] == 'Cache Test Book'