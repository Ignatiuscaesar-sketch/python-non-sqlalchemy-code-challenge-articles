import pytest

from classes.many_to_many import Article
from classes.many_to_many import Magazine
from classes.many_to_many import Author


class TestAuthor:
    """Author in many_to_many.py"""

    def test_has_name(self):
        """Author is initialized with a name"""
        author_1 = Author("Carry Bradshaw")
        assert author_1.name == "Carry Bradshaw"

    def test_name_is_immutable_string(self):
        """author name is of type str and cannot change"""
        author = Author("Carry Bradshaw")
        with pytest.raises(AttributeError):
            author.name = "ActuallyTopher"

    def test_name_len(self):
        """author name is longer than 0 characters"""
        with pytest.raises(ValueError):
            Author("")

    def test_has_many_articles(self):
        """author has many articles"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author, magazine, "How to wear a tutu with style")
        article_2 = Article(author, magazine, "Dating life in NYC")
        assert len(author.articles()) == 2

    def test_articles_of_type_articles(self):
        """author articles are of type Article"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article = Article(author, magazine, "How to wear a tutu with style")
        assert isinstance(author.articles()[0], Article)

    def test_has_many_magazines(self):
        """author has many magazines"""
        author = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        Article(author, magazine_1, "How to wear a tutu with style")
        Article(author, magazine_2, "2023 Eccentric Design Trends")
        assert magazine_1 in author.magazines()
        assert magazine_2 in author.magazines()

    def test_magazines_of_type_magazine(self):
        """author magazines are of type Magazine"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        assert isinstance(author.magazines()[0], Magazine)

    def test_magazines_are_unique(self):
        """author magazines are unique"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        Article(author, magazine, "Fashion in 2020")
        assert len(set(author.magazines())) == 1

    def test_add_article(self):
        """creates and returns a new article given a magazine and title"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article = author.add_article(magazine, "How to wear a tutu with style")
        assert isinstance(article, Article)
        assert article in author.articles()

    def test_topic_areas(self):
        """returns a list of topic areas for all articles by author"""
        author = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        author.add_article(magazine_1, "How to wear a tutu with style")
        author.add_article(magazine_2, "2023 Eccentric Design Trends")
        areas = author.topic_areas()
        assert "Fashion" in areas
        assert "Architecture" in areas
        assert len(areas) == 2

    def test_topic_areas_are_unique(self):
        """topic areas are unique"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        author.add_article(magazine, "How to wear a tutu with style")
        author.add_article(magazine, "Fashion in 2020")
        areas = author.topic_areas()
        assert len(areas) == 1
