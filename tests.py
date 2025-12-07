import pytest 
from main import BooksCollector


class TestBooksCollector:
    
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    
    @pytest.mark.parametrize('book_name, should_be_added', [
        ('А', True),
        ('Книга с нормальным названием', True),
        ('О' * 40, True),
        ('', False),
        ('О' * 41, False),
    ])
    def test_add_new_book_with_different_lengths(self, book_name, should_be_added):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        
        if should_be_added:
            assert book_name in collector.books_genre
            assert collector.books_genre[book_name] == ''
        else:
            assert book_name not in collector.books_genre

    @pytest.mark.parametrize('genre, is_valid', [
        ('Фантастика', True),
        ('Ужасы', True),
        ('Детективы', True),
        ('Несуществующий', False),
        ('', False),
    ])
    def test_set_book_genre_validation(self, genre, is_valid):
        collector = BooksCollector()
        book_name = 'Тестовая книга'
        collector.add_new_book(book_name)
        
        collector.set_book_genre(book_name, genre)
        
        if is_valid:
            assert collector.get_book_genre(book_name) == genre
        else:
            assert collector.get_book_genre(book_name) == ''

    @pytest.mark.parametrize('genre, is_for_children', [
        ('Мультфильмы', True),
        ('Комедии', True),
        ('Фантастика', True),
        ('Ужасы', False),
        ('Детективы', False),
        ('', False),
    ])
    def test_get_books_for_children_filtering(self, genre, is_for_children):
        collector = BooksCollector()
        book_name = 'Тестовая книга'
        collector.add_new_book(book_name)
        
        if genre:
            collector.set_book_genre(book_name, genre)
        
        children_books = collector.get_books_for_children()
        
        if is_for_children:
            assert book_name in children_books
        else:
            assert book_name not in children_books

    @pytest.mark.parametrize('book_in_catalog, operation, expected_in_favorites', [
        (True, 'add_once', True),
        (True, 'add_twice', True),
        (False, 'add_once', False),
    ])
    def test_favorites_operations(self, book_in_catalog, operation, expected_in_favorites):
        collector = BooksCollector()
        book_name = 'Тестовая книга'
        
        if book_in_catalog:
            collector.add_new_book(book_name)
        
        if operation == 'add_once':
            collector.add_book_in_favorites(book_name)
        elif operation == 'add_twice':
            collector.add_book_in_favorites(book_name)
            collector.add_book_in_favorites(book_name)
        
        if expected_in_favorites:
            assert book_name in collector.favorites
            if operation == 'add_twice':
                assert collector.favorites.count(book_name) == 1
        else:
            assert book_name not in collector.favorites

    def test_delete_from_favorites(self):
        collector = BooksCollector()
        book_name = 'Тестовая книга'
        
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites
        
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.favorites

    @pytest.mark.parametrize('target_genre, expected_books', [
        ('Фантастика', ['Книга 1', 'Книга 2']),
        ('Детективы', ['Книга 3']),
        ('Комедии', []),
        ('Несуществующий', []),
    ])
    def test_get_books_with_specific_genre(self, target_genre, expected_books):
        collector = BooksCollector()
        
        test_data = [
            ('Книга 1', 'Фантастика'),
            ('Книга 2', 'Фантастика'),
            ('Книга 3', 'Детективы'),
            ('Книга 4', ''),
        ]
        
        for name, genre in test_data:
            collector.add_new_book(name)
            if genre:
                collector.set_book_genre(name, genre)
        
        result = collector.get_books_with_specific_genre(target_genre)
        assert sorted(result) == sorted(expected_books)

    def test_no_duplicate_books(self):
        collector = BooksCollector()
        book_name = 'Уникальная книга'
        
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        
        assert list(collector.books_genre.keys()) == [book_name]
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize('book_count', [1, 3, 5])
    def test_complete_workflow(self, book_count):
        collector = BooksCollector()
        
        for i in range(book_count):
            book_name = f'Книга {i+1}'
            collector.add_new_book(book_name)
            
            if i % 2 == 0:
                genre = 'Фантастика' if i % 4 == 0 else 'Мультфильмы'
                collector.set_book_genre(book_name, genre)
            
            if i % 3 == 0:
                collector.add_book_in_favorites(book_name)
        
        assert len(collector.books_genre) == book_count
        
        books_dict = collector.get_books_genre()
        assert isinstance(books_dict, dict)
        assert len(books_dict) == book_count
        
        favorites = collector.get_list_of_favorites_books()
        expected_favorites_count = (book_count + 2) // 3
        assert len(favorites) == expected_favorites_count

    def test_get_book_genre(self):
        collector = BooksCollector()
        
        collector.add_new_book('Книга с жанром')
        collector.set_book_genre('Книга с жанром', 'Комедии')
        assert collector.get_book_genre('Книга с жанром') == 'Комедии'
        
        collector.add_new_book('Книга без жанра')
        assert collector.get_book_genre('Книга без жанра') == ''
        
        assert collector.get_book_genre('Несуществующая книга') is None

    @pytest.mark.parametrize('book_exists', [True, False])
    def test_set_genre_for_existing_and_nonexisting_book(self, book_exists):
        collector = BooksCollector()
        book_name = 'Тестовая книга'
        
        if book_exists:
            collector.add_new_book(book_name)
        
        collector.set_book_genre(book_name, 'Фантастика')
        
        if book_exists:
            assert collector.get_book_genre(book_name) == 'Фантастика'
        else:
            assert book_name not in collector.books_genre