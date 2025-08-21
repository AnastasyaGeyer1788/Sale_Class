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
    # Проверяем содержимое строк, а не атрибуты объектов
    assert "1000 руб." in category.products[0]
    assert "2000.5 руб." in category.products[1]
    assert "3000 руб." in category.products[2]
    assert "4000.75 руб." in category.products[3]


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

    # Проверяем содержимое строк вместо типов
    assert "1000 руб." in category.products[0]
    assert "2000.0 руб." in category.products[1]
    assert "3000.5 руб." in category.products[2]


def test_category_price_access():
    """Тест доступа к ценам продуктов в категории"""
    products = [
        Product("Cheap", "Desc", 10, 100),  # int
        Product("Medium", "Desc", 99.99, 50),  # float
        Product("Expensive", "Desc", 1000, 10),  # int
    ]

    category = Category("Price Test", "Testing price access", products)

    # Проверяем содержимое строк
    assert "10 руб." in category.products[0]
    assert "99.99 руб." in category.products[1]
    assert "1000 руб." in category.products[2]


def test_category_with_empty_products():
    """Тест категории с пустым списком продуктов"""
    category = Category("Empty Category", "No products", [])

    assert category.name == "Empty Category"
    assert category.description == "No products"
    assert category.products == []
    assert len(category.products) == 0


def test_product_count_increment():
    """Тест подсчета количества продуктов"""
    Category.category_count = 0
    Category.product_count = 0

    assert Category.product_count == 0

    products1 = [
        Product("P1", "Desc", 100, 1),  # int
        Product("P2", "Desc", 200.50, 2),  # float
    ]
    # Создание продуктов уже увеличило счетчик
    assert Category.product_count == 2  # Теперь здесь 2

    Category("Cat 1", "Desc 1", products1)
    assert Category.product_count == 4

    products2 = [
        Product("P3", "Desc", 300, 3),  # int
        Product("P4", "Desc", 400.75, 4),  # float
        Product("P5", "Desc", 500, 5),  # int
    ]
    # Создание еще 3 продуктов
    assert Category.product_count == 7  # 2 + 5 = 7

    Category("Cat 2", "Desc 2", products2)
    assert Category.product_count == 10


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
    # Теперь products возвращает список строк, а не объектов
    assert len(category.products) == 1
    assert "Test, 1000 руб. Остаток: 5 шт." in category.products[0]


# Новые тесты для приватного списка товаров и метода add_product()
def test_add_product_to_category():
    """Тест добавления товара в категорию через add_product"""
    category = Category("Test Category", "Test Description", [])
    product = Product("New Product", "Description", 1000, 5)

    # Изначально пусто
    assert len(category.products) == 0

    # Добавляем товар
    category.add_product(product)

    # Проверяем, что товар добавлен (в виде строки)
    assert len(category.products) == 1
    assert "New Product" in category.products[0]
    assert "1000 руб." in category.products[0]


def test_add_product_increments_counter():
    """Тест, что add_product увеличивает счетчик продуктов"""
    Category.category_count = 0
    Category.product_count = 0

    category = Category("Test Category", "Test Description", [])
    product = Product("New Product", "Description", 1000, 5)

    initial_count = Category.product_count
    category.add_product(product)

    assert Category.product_count == initial_count + 1


def test_add_multiple_products():
    """Тест добавления нескольких товаров в категорию"""
    category = Category("Test Category", "Test Description", [])

    products = [
        Product("Product 1", "Desc", 1000, 5),
        Product("Product 2", "Desc", 2000, 3),
        Product("Product 3", "Desc", 3000, 7),
    ]

    for product in products:
        category.add_product(product)

    assert len(category.products) == 3
    assert Category.product_count == 6


def test_products_property_format():
    """Тест формата вывода свойства products"""
    products = [Product("Product 1", "Description 1", 1000, 5), Product("Product 2", "Description 2", 2000.50, 3)]

    category = Category("Test Category", "Test Description", products)

    # Проверяем формат вывода с \n
    products_list = category.products
    assert len(products_list) == 2
    assert products_list[0] == "Product 1, 1000 руб. Остаток: 5 шт.\n"
    assert products_list[1] == "Product 2, 2000.5 руб. Остаток: 3 шт.\n"


def test_add_product_with_different_price_types():
    """Тест добавления товаров с разными типами цен"""
    category = Category("Test Category", "Test Description", [])

    product_int = Product("Int Price", "Desc", 1000, 5)  # int
    product_float = Product("Float Price", "Desc", 2000.50, 3)  # float

    category.add_product(product_int)
    category.add_product(product_float)

    assert len(category.products) == 2
    # Проверяем содержимое строк
    assert "1000 руб." in category.products[0]
    assert "2000.5 руб." in category.products[1]


def test_category_products_immutability():
    """Тест, что нельзя напрямую изменить список продуктов"""
    products = [Product("Test", "Desc", 1000, 5)]
    category = Category("Test Category", "Test Description", products)

    # Получаем список продуктов (строк)
    original_products = category.products
    original_products.append("invalid item")  # Это добавится в копию

    # Но оригинальный список в категории не должен измениться
    assert len(category.products) == 1  # Все еще 1 товар
    assert "Test" in category.products[0]  # Все еще содержит оригинальный товар
