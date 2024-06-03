class Article:
    _registry = []  # Class variable to track all articles

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author) or not isinstance(magazine, Magazine):
            raise TypeError("Author and Magazine must be the correct instances")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        
        self._author = author
        self._magazine = magazine
        self._title = title
        Article._registry.append(self)  # Register the article globally
        author._articles.append(self)
        magazine._articles.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError("Cannot change the title after it's set")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("Author must be an instance of Author")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("Magazine must be an instance of Magazine")
        self._magazine = value

    @classmethod
    def all(cls):
        return cls._registry

class Author:
    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError("Name cannot be empty and must be a string")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name cannot be changed once set")

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def articles(self):
        return self._articles

    def magazines(self):
        return list(set(article.magazine for article in self._articles))

    def topic_areas(self):
        areas = set(article.magazine.category for article in self._articles)
        return list(areas) if areas else None

class Magazine:
    all_magazines = []  # Class variable to store all instances of Magazine

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category cannot be empty and must be a string")
        
        self._name = name
        self._category = category
        self._articles = []
        Magazine.all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and value.strip():
            self._category = value
        else:
            raise ValueError("Category cannot be empty and must be a string")

    def articles(self):
        return self._articles

    def article_titles(self):
        return [article.title for article in self._articles]

    def contributors(self):
        return list(set(article.author for article in self._articles))

    def contributing_authors(self):
        author_counts = {}
        for article in self._articles:
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1
        return [author for author, count in author_counts.items() if count > 2]

    @classmethod
    def top_publisher(cls):
        if not cls.all_magazines or all(len(magazine.articles()) == 0 for magazine in cls.all_magazines):
            return None
        return max(cls.all_magazines, key=lambda magazine: len(magazine.articles()), default=None)
