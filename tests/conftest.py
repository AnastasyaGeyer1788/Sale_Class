import pytest


@pytest.fixture
def product_class():
    """Фикстура возвращает класс Product для использования в тестах"""
    from src.product import Product

    return Product


@pytest.fixture
def category_class():
    """Фикстура возвращает класс Category для использования в тестах"""
    from src.category import Category

    return Category


@pytest.fixture
def sample_product(product_class):
    """Фикстура для создания тестового продукта"""
    return product_class("Test Product", "Test Description", 1000, 10)


@pytest.fixture
def sample_products(product_class):
    """Фикстура для создания нескольких тестовых продуктов"""
    return [
        product_class("Product 1", "Description 1", 1000, 5),
        product_class("Product 2", "Description 2", 2000.0, 8),
        product_class("Product 3", "Description 3", 3000.50, 12),
    ]


@pytest.fixture
def sample_category(category_class, sample_products):
    """Фикстура для создания тестовой категории"""
    return category_class("Test Category", "Test Category Description", sample_products)


@pytest.fixture(autouse=True)
def reset_counters(category_class):
    """Автоматический сброс счетчиков перед каждым тестом"""
    category_class.category_count = 0
    category_class.product_count = 0
    yield
    category_class.category_count = 0
    category_class.product_count = 0
