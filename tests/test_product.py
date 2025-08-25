import pytest
from src.product import Product


class TestProduct:
    """Тесты для класса Product"""

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

        # Проверяем геттер
        assert product.price == 1000

        # Проверяем сеттер с валидным значением
        product.price = 1500
        assert product.price == 1500

        # Проверяем сеттер с невалидным значением
        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product.price = -100

    def test_negative_price_creation(self, product_class):
        """Тест создания продукта с отрицательной ценой"""
        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class("Test Product", "Test Description", -100, 10)

    def test_float_price(self, product_class):
        """Тест работы с float ценой"""
        product = product_class("Test Product", "Test Description", 999.99, 10)
        assert product.price == 999.99

    def test_new_product_creation(self, product_class):
        """Тест создания нового продукта через classmethod"""
        product_data = {"name": "New Product", "description": "New Description", "price": 1500, "quantity": 20}

        product = product_class.new_product(product_data)
        assert product.name == "New Product"
        assert product.price == 1500
        assert product.quantity == 20

    def test_new_product_update_existing(self, product_class):
        """Тест обновления существующего продукта"""
        # Создаем первый продукт
        existing_product = product_class("Existing Product", "Desc", 1000, 10)

        # Пытаемся создать "новый" продукт с тем же именем
        product_data = {"name": "Existing Product", "description": "Updated Desc", "price": 1200, "quantity": 5}

        updated_product = product_class.new_product(product_data, [existing_product])

        # Должен вернуться существующий продукт с обновленными данными
        assert updated_product is existing_product
        assert updated_product.quantity == 15  # 10 + 5
        assert updated_product.price == 1200  # Новая цена выше
        assert updated_product.description == "Updated Desc"

    def test_new_product_missing_name(self, product_class):
        """Тест создания продукта без имени"""
        product_data = {"description": "Description", "price": 1000, "quantity": 10}

        with pytest.raises(ValueError, match="Название товара должно быть указано"):
            product_class.new_product(product_data)

    def test_new_product_negative_price(self, product_class):
        """Тест создания продукта с отрицательной ценой через new_product"""
        product_data = {"name": "Test Product", "description": "Test Description", "price": -100, "quantity": 10}

        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class.new_product(product_data)
