import pytest
from src.category import Category
from src.product import Product


class TestCategory:
    """Тесты для класса Category"""

    def test_category_creation(self, category_class, sample_products):
        """Тест создания категории"""
        category = category_class("Test Category", "Test Description", sample_products)
        assert category.name == "Test Category"
        assert category.description == "Test Description"
        assert len(category.products) == 3

    def test_add_product(self, category_class, sample_product):
        """Тест добавления продукта в категорию"""
        category = category_class("Test Category", "Test Description")
        category.add_product(sample_product)
        assert len(category.products) == 1
        assert "Test Product, 1000 руб. Остаток: 10 шт." in category.products

    def test_add_invalid_product(self, category_class):
        """Тест добавления невалидного продукта"""
        category = category_class("Test Category", "Test Description")
        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product"):
            category.add_product("invalid product")

    def test_products_property(self, category_class, sample_products):
        """Тест геттера products"""
        category = category_class("Test Category", "Test Description", sample_products)
        products_list = category.products
        assert isinstance(products_list, list)
        assert len(products_list) == 3
        assert all(isinstance(item, str) for item in products_list)

    def test_counters(self, category_class, sample_products):
        """Тест счетчиков категорий и продуктов"""
        # Сбрасываем счетчики перед тестом
        category_class.category_count = 0
        category_class.product_count = 0

        category1 = category_class("Category 1", "Desc 1", sample_products[:2])
        category2 = category_class("Category 2", "Desc 2", sample_products[2:])

        assert category_class.category_count == 2
        assert category_class.product_count == 3
