import pytest


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
        """Тест создания нового продукта"""
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

    def test_str_representation(self, product_class):
        """Тест строкового представления продукта"""
        product = product_class("Телефон", "Смартфон", 80000, 15)
        expected_str = "Телефон, 80000 руб. Остаток: 15 шт."
        assert str(product) == expected_str

    def test_str_representation_float_price(self, product_class):
        """Тест строкового представления с float ценой"""
        product = product_class("Книга", "Художественная", 499.99, 3)
        expected_str = "Книга, 499.99 руб. Остаток: 3 шт."
        assert str(product) == expected_str

    def test_add_products(self, product_class):
        """Тест сложения двух продуктов"""
        product_a = product_class("Товар A", "Описание A", 100, 10)
        product_b = product_class("Товар B", "Описание B", 200, 2)

        result = product_a + product_b
        expected = 100 * 10 + 200 * 2  # 1000 + 400 = 1400

        assert result == expected
        assert isinstance(result, (int, float))

    def test_add_products_commutative(self, product_class):
        """Тест коммутативности сложения продуктов"""
        product_a = product_class("Товар A", "Описание A", 100, 10)
        product_b = product_class("Товар B", "Описание B", 200, 2)

        result1 = product_a + product_b
        result2 = product_b + product_a

        assert result1 == result2

    def test_add_products_with_float_prices(self, product_class):
        """Тест сложения продуктов с float ценами"""
        product_a = product_class("Товар A", "Описание A", 99.99, 5)
        product_b = product_class("Товар B", "Описание B", 149.50, 3)

        result = product_a + product_b
        expected = 99.99 * 5 + 149.50 * 3  # 499.95 + 448.50 = 948.45

        assert abs(result - expected) < 0.01  # Учитываем погрешность float

    def test_add_product_with_zero_quantity(self, product_class):
        """Тест сложения продуктов с нулевым количеством"""
        product_a = product_class("Товар A", "Описание A", 100, 0)
        product_b = product_class("Товар B", "Описание B", 200, 5)

        result = product_a + product_b
        expected = 0 + 200 * 5  # 0 + 1000 = 1000

        assert result == expected

    def test_add_product_with_different_types_error(self, product_class):
        """Тест ошибки при сложении с неправильным типом"""
        product = product_class("Товар", "Описание", 100, 10)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + "не продукт"

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + 123

    def test_add_products_chain(self, product_class):
        """Тест цепочного сложения продуктов"""
        product_a = product_class("Товар A", "Описание A", 100, 2)
        product_b = product_class("Товар B", "Описание B", 200, 3)
        product_c = product_class("Товар C", "Описание C", 300, 4)

        # Просто проверяем что сумма всех трех равна ожидаемому значению
        total = (product_a + product_b) + (product_c.price * product_c.quantity)
        expected = (100 * 2 + 200 * 3) + (300 * 4)

        assert total == expected


class TestProductAdditionValidation:
    """Тесты для проверки сложения продуктов разных категорий"""

    def test_add_same_category_products(self, product_class):
        """Тест сложения продуктов одной категории"""
        product1 = product_class("Product 1", "Desc", 100, 5)
        product2 = product_class("Product 2", "Desc", 200, 3)

        result = product1 + product2
        assert result == 100 * 5 + 200 * 3

    def test_add_different_category_products_error(self):
        """Тест ошибки при сложении продуктов разных категорий"""
        from src.product import Smartphone, LawnGrass

        smartphone = Smartphone("Phone", "Desc", 50000, 2, "High", "Model", 128, "Black")
        lawn_grass = LawnGrass("Grass", "Desc", 2000, 5, "USA", 10, "Green")

        with pytest.raises(TypeError, match="Нельзя складывать товары разных категорий"):
            smartphone + lawn_grass

    def test_add_smartphones(self):
        """Тест сложения смартфонов"""
        from src.product import Smartphone

        smartphone1 = Smartphone("Phone 1", "Desc", 50000, 2, "High", "Model", 128, "Black")
        smartphone2 = Smartphone("Phone 2", "Desc", 60000, 3, "High", "Model", 256, "White")

        result = smartphone1 + smartphone2
        assert result == 50000 * 2 + 60000 * 3

    def test_add_lawn_grasses(self):
        """Тест сложения газонных трав"""
        from src.product import LawnGrass

        grass1 = LawnGrass("Grass 1", "Desc", 2000, 5, "USA", 10, "Green")
        grass2 = LawnGrass("Grass 2", "Desc", 2500, 3, "Germany", 14, "Dark Green")

        result = grass1 + grass2
        assert result == 2000 * 5 + 2500 * 3
