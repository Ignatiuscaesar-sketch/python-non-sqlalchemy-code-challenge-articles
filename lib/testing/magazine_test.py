import pytest
from classes.many_to_many import Article, Magazine, Author

class TestMagazine:
    """Tests for the Magazine class"""

    @pytest.fixture(autouse=True)
    def clear_magazine_registry(self):
        Magazine.all_magazines.clear()  # Clear the list of all magazines before each test

    def test_has_name(self):
        """Magazine is initialized with a name"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        assert magazine_1.name == "Vogue"
        assert magazine_2.name == "AD"

    def test_name_is_mutable_string(self):
        """magazine name is of type str and can change"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_1.name = "New Yorker"
        assert magazine_1.name == "New Yorker"
        assert isinstance(magazine_1.name, str)

        # Testing type enforcement for non-string types
        with pytest.raises(ValueError):
            magazine_1.name = 2

    def test_name_len(self):
        """magazine name is between 2 and 16 characters, inclusive"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")

        # Ensuring proper length restrictions
        with pytest.raises(ValueError):
            magazine_1.name = "New Yorker Plus Extra Long Name"
        with pytest.raises(ValueError):
            magazine_2.name = "A"

        assert 2 <= len(magazine_1.name) <= 16
        assert 2 <= len(magazine_2.name) <= 16

    def test_has_category(self):
        """Magazine is initialized with a category"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture")
        assert magazine_1.category == "Fashion"
        assert magazine_2.category == "Architecture"

    def test_category_is_mutable_string(self):
        """magazine category is of type str and can change"""
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_1.category = "Life Style"
        assert magazine_1.category == "Life Style"
        assert isinstance(magazine_1.category, str)

        # Testing type enforcement for non-string types
        with pytest.raises(ValueError):
            magazine_1.category = 2

    def test_category_len(self):
        """magazine category has length greater than 0"""
        magazine_1 = Magazine("Vogue", "Fashion")
        with pytest.raises(ValueError):
            magazine_1.category = ""

        assert len(magazine_1.category) > 0

    def test_has_many_articles(self):
        """magazine has many articles"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        Article(author, magazine, "Dating life in NYC")
        assert len(magazine.articles()) == 2

    def test_articles_of_type_articles(self):
        """magazine articles are of type Article"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        assert isinstance(magazine.articles()[0], Article)

    def test_has_many_contributors(self):
        """magazine has many contributors"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine = Magazine("Vogue", "Fashion")
        Article(author_1, magazine, "How to wear a tutu with style")
        Article(author_2, magazine, "Dating life in NYC")
        assert len(magazine.contributors()) == 2

    def test_contributors_of_type_author(self):
        """magazine contributors are of type Author"""
        author_1 = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author_1, magazine, "How to wear a tutu with style")
        assert all(isinstance(author, Author) for author in magazine.contributors())

    def test_contributors_are_unique(self):
        """magazine contributors are unique"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        Article(author, magazine, "Another article by Carry")
        assert len(set(magazine.contributors())) == 1  # Ensure unique contributors

    def test_article_titles(self):
        """returns list of titles strings of all articles written for that magazine"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        assert magazine.article_titles() == ["How to wear a tutu with style"]

    def test_contributing_authors(self):
        """returns author list who have written more than 2 articles for the magazine"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        Article(author, magazine, "How to wear a tutu with style")
        Article(author, magazine, "Another style article")
        Article(author, magazine, "Yet another style article")
        assert author in magazine.contributing_authors()

    def test_top_publisher_with_no_magazines(self):
        """top_publisher should return None if no magazines are present"""
        assert Magazine.top_publisher() is None

    def test_top_publisher_with_no_articles(self):
        """top_publisher should return None if magazines have no articles"""
        Magazine("Vogue", "Fashion")
        Magazine("AD", "Architecture")
        assert Magazine.top_publisher() is None

    def test_top_publisher_with_varied_article_counts(self):
        """top_publisher should correctly identify the magazine with the most articles"""
        author = Author("Carry Bradshaw")
        vogue = Magazine("Vogue", "Fashion")
        ad = Magazine("AD", "Architecture")
        gq = Magazine("GQ", "Lifestyle")

        Article(author, vogue, "Spring Fashion Trends")
        Article(author, vogue, "Summer Fashion Trends")
        Article(author, ad, "Modern Architecture")
        Article(author, gq, "Winter Fashion")
        Article(author, gq, "Autumn Fashion")
        Article(author, gq, "Summer Accessories")

        assert Magazine.top_publisher() == gq
