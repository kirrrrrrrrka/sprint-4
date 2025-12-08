import pytest
from main import BooksCollector


class TestBooksCollector:
    
    # Пример теста из задания (не параметризуем)
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('book_name, should_be_added', [
        ('А', True),   
        ('Нормальное название', True),
        ('О' * 40, True),
        ('', False),    
        ('О' * 41, False), 
    ])
    def test_add_new_book_name_length_boundaries(self, book_name, should_be_added):
        """Один сценарий: проверка границ длины названия"""
        collector = BooksCollector()
        collector.add_new_book(book_name)
        
        if should_be_added:
            assert book_name in collector.books_genre
            assert collector.books_genre[book_name] == ''
        else:
            assert book_name not in collector.books_genre

    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Дубликат')
        collector.add_new_book('Дубликат')
        assert list(collector.books_genre.keys()) == ['Дубликат']

    @pytest.mark.parametrize('genre', ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'])
    def test_set_book_genre_valid_genres(self, genre):
        """Один сценарий: установка разных валидных жанров"""
        collector = BooksCollector()
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', genre)
        assert collector.books_genre['Тестовая книга'] == genre

    def test_set_book_genre_invalid_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий')
        assert collector.books_genre['Книга'] == ''

    def test_set_book_genre_empty_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', '')
        assert collector.books_genre['Книга'] == ''

    def test_set_book_genre_for_nonexisting_book(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая', 'Фантастика')
        assert 'Несуществующая' not in collector.books_genre

    @pytest.mark.parametrize('book_name, genre_in_dict, expected_genre', [
        ('Книга с жанром', 'Комедии', 'Комедии'),
        ('Книга без жанра', '', ''),
    ])
    def test_get_book_genre_different_book_states(self, book_name, genre_in_dict, expected_genre):
        """Один сценарий: получение жанра для книг в разных состояниях"""
        collector = BooksCollector()
        collector.books_genre[book_name] = genre_in_dict
        assert collector.get_book_genre(book_name) == expected_genre

    def test_get_book_genre_nonexisting_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Неизвестная книга') is None

    @pytest.mark.parametrize('target_genre, expected_books', [
        ('Фантастика', ['Книга 1', 'Книга 2']),
        ('Детективы', ['Книга 3']),
        ('Комедии', []), 
        ('Несуществующий', []), 
    ])
    def test_get_books_with_specific_genre(self, target_genre, expected_books):
        """Один сценарий: получение книг по разным жанрам"""
        collector = BooksCollector()
        collector.books_genre = {
            'Книга 1': 'Фантастика',
            'Книга 2': 'Фантастика',
            'Книга 3': 'Детективы',
            'Книга 4': '',
        }
        
        result = collector.get_books_with_specific_genre(target_genre)
        assert sorted(result) == sorted(expected_books)

    def test_get_books_genre_returns_empty_dict_for_new_collector(self):
        collector = BooksCollector()
        assert collector.get_books_genre() == {}

    def test_get_books_genre_returns_correct_dict(self):
        collector = BooksCollector()
        collector.books_genre = {'Книга 1': 'Фантастика', 'Книга 2': ''}
        expected = {'Книга 1': 'Фантастика', 'Книга 2': ''}
        assert collector.get_books_genre() == expected

    @pytest.mark.parametrize('genre, is_for_children', [
        ('Мультфильмы', True),  
        ('Комедии', True),    
        ('Фантастика', True),     
        ('Ужасы', False),         
        ('Детективы', False),     
    ])
    def test_get_books_for_children_by_genre(self, genre, is_for_children):
        """Один сценарий: проверка разных жанров на пригодность для детей"""
        collector = BooksCollector()
        collector.books_genre = {'Тестовая книга': genre}
        
        children_books = collector.get_books_for_children()
        
        if is_for_children:
            assert 'Тестовая книга' in children_books
        else:
            assert 'Тестовая книга' not in children_books

    def test_get_books_for_children_does_not_return_books_without_genre(self):
        collector = BooksCollector()
        collector.books_genre = {'Книга без жанра': ''}
        assert collector.get_books_for_children() == []

    def test_add_book_in_favorites_book_in_catalog(self):
        collector = BooksCollector()
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        assert 'Любимая книга' in collector.favorites

    def test_add_book_in_favorites_book_not_in_catalog(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Неизвестная книга')
        assert 'Неизвестная книга' not in collector.favorites

    def test_add_book_in_favorites_duplicate_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert collector.favorites == ['Книга']

    def test_delete_book_from_favorites_existing_book(self):
        collector = BooksCollector()
        collector.favorites = ['Книга']
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.favorites

    def test_delete_book_from_favorites_nonexisting_book(self):
        collector = BooksCollector()
        collector.favorites = ['Книга']
        collector.delete_book_from_favorites('Неизвестная')
        assert 'Книга' in collector.favorites

    def test_get_list_of_favorites_books_returns_empty_list_for_new_collector(self):
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_returns_correct_list(self):
        collector = BooksCollector()
        collector.favorites = ['Книга 1', 'Книга 2']
        assert sorted(collector.get_list_of_favorites_books()) == ['Книга 1', 'Книга 2']