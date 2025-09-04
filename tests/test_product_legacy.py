import pytest


class TestProductLegacy:
    """Легаси-тесты для обратной совместимости"""

    def test_product_creation(self, product_class):
        """Тест создания продукта"""
        product = product_class("Test Product", "Test Description", 1000, 10)
        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 1000
        assert product.quantity == 10

    def test_price_getter_setter(self, product_class):
        """Тест геттера и сеттера цены"""
        product = product_class("Test Product", "Test Description", 1000, 10)
        assert product.price == 1000

        product.price = 1500
        assert product.price == 1500

        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product.price = -100

    def test_new_product_creation(self, product_class):
        """Тест создания нового продукта"""
        product_data = {"name": "New Product", "description": "New Description", "price": 1500, "quantity": 20}
        product = product_class.new_product(product_data)
        assert product.name == "New Product"
        assert product.price == 1500
        assert product.quantity == 20

    def test_str_representation(self, product_class):
        """Тест строкового представления продукта"""
        product = product_class("Телефон", "Смартфон", 80000, 15)
        expected_str = "Телефон, 80000 руб. Остаток: 15 шт."
        assert str(product) == expected_str

    def test_add_products(self, product_class):
        """Тест сложения двух продуктов"""
        product_a = product_class("Товар A", "Описание A", 100, 10)
        product_b = product_class("Товар B", "Описание B", 200, 2)
        result = product_a + product_b
        expected = 100 * 10 + 200 * 2
        assert result == expected
