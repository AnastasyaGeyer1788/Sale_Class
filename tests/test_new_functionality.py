import pytest


class TestAveragePrice:
    """Тесты для метода get_average_price"""

    def test_average_price_empty_category(self, category_class):
        """Тест средней цены для пустой категории"""
        category = category_class("Пустая", "Нет товаров")
        assert category.get_average_price() == 0.0

    def test_average_price_single_product(self, category_class, product_class):
        """Тест средней цены для одного товара"""
        category = category_class("Электроника", "Электронные товары")
        product = product_class("Телефон", "Смартфон", 10000, 2)
        category.add_product(product)

        assert category.get_average_price() == 10000.0

    def test_average_price_multiple_products(self, category_class, product_class):
        """Тест средней цены для нескольких товаров"""
        category = category_class("Электроника", "Электронные товары")

        # Товар 1: 10000 * 2 = 20000
        product1 = product_class("Телефон", "Смартфон", 10000, 2)
        # Товар 2: 50000 * 1 = 50000
        product2 = product_class("Ноутбук", "Игровой", 50000, 1)

        category.add_product(product1)
        category.add_product(product2)

        # Средняя цена: (20000 + 50000) / (2 + 1) = 70000 / 3 ≈ 23333.33
        expected_average = round(70000 / 3, 2)
        assert category.get_average_price() == expected_average

    def test_average_price_with_different_quantities(self, category_class, product_class):
        """Тест средней цены с разными количествами товаров"""
        category = category_class("Магазин", "Разные товары")

        # Дешевый товар в большом количестве
        product1 = product_class("Карандаш", "Простой", 10, 100)  # 10 * 100 = 1000
        # Дорогой товар в малом количестве
        product2 = product_class("Ноутбук", "Дорогой", 100000, 2)  # 100000 * 2 = 200000

        category.add_product(product1)
        category.add_product(product2)

        # Средняя цена: (1000 + 200000) / (100 + 2) = 201000 / 102 ≈ 1970.59
        expected_average = round(201000 / 102, 2)
        assert category.get_average_price() == expected_average

    def test_average_price_float_values(self, category_class, product_class):
        """Тест средней цены с float значениями"""
        category = category_class("Магазин", "Товары с дробными ценами")

        product1 = product_class("Товар 1", "Описание", 99.99, 3)  # 99.99 * 3 = 299.97
        product2 = product_class("Товар 2", "Описание", 149.50, 2)  # 149.50 * 2 = 299.00

        category.add_product(product1)
        category.add_product(product2)

        # Средняя цена: (299.97 + 299.00) / (3 + 2) = 598.97 / 5 = 119.794 ≈ 119.79
        expected_average = round(598.97 / 5, 2)
        assert category.get_average_price() == expected_average


class TestZeroQuantityValidation:
    """Тесты для валидации нулевого количества"""

    def test_product_zero_quantity_creation(self, product_class):
        """Тест создания продукта с нулевым количеством"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            product_class("Телефон", "Смартфон", 10000, 0)

    def test_smartphone_zero_quantity_creation(self, smartphone_class):
        """Тест создания смартфона с нулевым количеством"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            smartphone_class("iPhone", "Смартфон", 50000, 0, "Высокая", "15", 256, "Black")

    def test_lawn_grass_zero_quantity_creation(self, lawn_grass_class):
        """Тест создания газонной травы с нулевым количеством"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            lawn_grass_class("Трава", "Газонная", 1000, 0, "Россия", 30, "Зеленая")

    def test_add_zero_quantity_product_to_category(self, category_class, product_class):
        """Тест добавления товара с нулевым количеством в категорию"""
        category = category_class("Электроника", "Электронные товары")

        # Создаем продукт с нулевым количеством (это должно вызвать исключение)
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            product = product_class("Телефон", "Смартфон", 10000, 0)
            category.add_product(product)

    def test_new_product_zero_quantity(self, product_class):
        """Тест создания нового товара с нулевым количеством через new_product"""
        product_data = {"name": "Телефон", "description": "Смартфон", "price": 10000, "quantity": 0}

        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            product_class.new_product(product_data)

    def test_new_product_update_to_zero_quantity(self, product_class):
        """Тест обновления существующего товара до нулевого количества"""
        existing_product = product_class("Телефон", "Смартфон", 10000, 5)
        product_data = {"name": "Телефон", "price": 10000, "quantity": -5}  # 5 + (-5) = 0

        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            product_class.new_product(product_data, [existing_product])


class TestBackwardCompatibility:
    """Тесты обратной совместимости"""

    def test_old_tests_still_pass(self, category_class, product_class):
        """Тест, что старые тесты продолжают работать"""
        # Создаем категорию и продукты
        category = category_class("Электроника", "Электронные товары")
        product1 = product_class("Телефон", "Смартфон", 10000, 2)
        product2 = product_class("Ноутбук", "Игровой", 50000, 1)

        # Добавляем продукты
        category.add_product(product1)
        category.add_product(product2)

        # Проверяем старую функциональность
        assert category.name == "Электроника"
        assert len(category.products) == 2
        assert category.total_products_quantity == 3
        assert str(category) == "Электроника, количество продуктов: 3 шт."

        # Проверяем новую функциональность
        assert category.get_average_price() == round(70000 / 3, 2)

    def test_product_addition_still_works(self, product_class):
        """Тест, что сложение продуктов продолжает работать"""
        product1 = product_class("Товар A", "Описание", 100, 10)
        product2 = product_class("Товар B", "Описание", 200, 5)

        result = product1 + product2
        assert result == 100 * 10 + 200 * 5

    def test_price_validation_still_works(self, product_class):
        """Тест, что валидация цены продолжает работать"""
        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class("Товар", "Описание", -100, 10)

        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class("Товар", "Описание", 0, 10)
