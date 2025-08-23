import pytest

from src.category import Category
from src.product import Product


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Test Product", "Test Description", 1000, 10)  # int price


@pytest.fixture
def sample_products():
    """Фикстура для создания нескольких тестовых продуктов"""
    return [
        Product("Product 1", "Description 1", 1000, 5),  # int
        Product("Product 2", "Description 2", 2000.0, 8),  # float
        Product("Product 3", "Description 3", 3000.50, 12),  # float
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура для создания тестовой категории"""
    return Category("Test Category", "Test Category Description", sample_products)


@pytest.fixture(autouse=True)
def reset_counters():
    """Автоматический сброс счетчиков перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0
    yield
