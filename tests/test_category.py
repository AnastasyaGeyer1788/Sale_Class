from src.category import Category
from src.product import Product


def test_category_with_mixed_price_types():
    """Тест категории с продуктами разных типов цен"""
    products = [
        Product("Product 1", "Desc", 1000, 5),  # int
        Product("Product 2", "Desc", 2000.50, 8),  # float
        Product("Product 3", "Desc", 3000, 12),  # int
        Product("Product 4", "Desc", 4000.75, 3),  # float
    ]

    category = Category("Mixed Prices", "Products with different price types", products)

    assert len(category.products) == 4
    assert isinstance(category.products[0].price, int)
    assert isinstance(category.products[1].price, float)
    assert isinstance(category.products[2].price, int)
    assert isinstance(category.products[3].price, float)


def test_category_product_count_with_mixed_prices():
    """Тест подсчета продуктов с разными типами цен"""
    Category.category_count = 0
    Category.product_count = 0

    products = [
        Product("P1", "Desc", 100, 1),  # int
        Product("P2", "Desc", 200.50, 2),  # float
        Product("P3", "Desc", 300, 3),  # int
    ]

    category = Category("Test Category", "Desc", products)

    assert Category.product_count == 3
    assert Category.category_count == 1


def test_category_initialization():
    """Тест корректной инициализации категории с mixed prices"""
    products = [
        Product("Product 1", "Description 1", 1000, 5),  # int
        Product("Product 2", "Description 2", 2000.0, 8),  # float
        Product("Product 3", "Description 3", 3000.50, 12),  # float
    ]

    category = Category("Test Category", "Test Category Description", products)

    assert category.name == "Test Category"
    assert category.description == "Test Category Description"
    assert len(category.products) == 3

    # Проверяем типы цен
    assert isinstance(category.products[0].price, int)  # 1000
    assert isinstance(category.products[1].price, float)  # 2000.0
    assert isinstance(category.products[2].price, float)  # 3000.50


def test_category_price_access():
    """Тест доступа к ценам продуктов в категории"""
    products = [
        Product("Cheap", "Desc", 10, 100),  # int
        Product("Medium", "Desc", 99.99, 50),  # float
        Product("Expensive", "Desc", 1000, 10),  # int
    ]

    category = Category("Price Test", "Testing price access", products)

    assert category.products[0].price == 10
    assert category.products[1].price == 99.99
    assert category.products[2].price == 1000

    assert isinstance(category.products[0].price, int)
    assert isinstance(category.products[1].price, float)
    assert isinstance(category.products[2].price, int)


def test_category_with_empty_products():
    """Тест категории с пустым списком продуктов"""
    category = Category("Empty Category", "No products", [])

    assert category.name == "Empty Category"
    assert category.description == "No products"
    assert category.products == []
    assert len(category.products) == 0


def test_category_count_increment():
    """Тест подсчета количества категорий"""
    Category.category_count = 0
    Category.product_count = 0

    assert Category.category_count == 0

    category1 = Category("Cat 1", "Desc 1", [])
    assert Category.category_count == 1

    category2 = Category("Cat 2", "Desc 2", [])
    assert Category.category_count == 2


def test_product_count_increment():
    """Тест подсчета количества продуктов"""
    Category.category_count = 0
    Category.product_count = 0

    assert Category.product_count == 0

    products1 = [
        Product("P1", "Desc", 100, 1),  # int
        Product("P2", "Desc", 200.50, 2),  # float
    ]
    category1 = Category("Cat 1", "Desc 1", products1)
    assert Category.product_count == 2

    products2 = [
        Product("P3", "Desc", 300, 3),  # int
        Product("P4", "Desc", 400.75, 4),  # float
        Product("P5", "Desc", 500, 5),  # int
    ]
    category2 = Category("Cat 2", "Desc 2", products2)
    assert Category.product_count == 5  # 2 + 3


def test_category_direct_attribute_access():
    """Тест прямого доступа к атрибутам категории"""
    products = [Product("Test", "Desc", 1000, 5)]
    category = Category("Test Category", "Test Description", products)

    # Проверяем, что можем получить все атрибуты
    assert hasattr(category, "name")
    assert hasattr(category, "description")
    assert hasattr(category, "products")

    # Проверяем значения
    assert category.name == "Test Category"
    assert category.description == "Test Description"
    assert category.products == products
