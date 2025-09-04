import pytest


class TestBaseProduct:
    """Тесты для абстрактного класса BaseProduct"""

    def test_base_product_is_abstract(self):
        """Тест, что BaseProduct является абстрактным классом"""
        from src.product import BaseProduct

        with pytest.raises(TypeError):
            BaseProduct("Test", "Desc", 100, 10)


class TestCreationLoggerMixin:
    """Тесты миксина CreationLoggerMixin"""

    class TestCreationLoggerMixin:
        """Тесты миксина CreationLoggerMixin"""

    def test_creation_logger_output(self, product_class, capture_console_output):
        """Тест вывода информации при создании объекта"""
        product = product_class("Test Product", "Test Description", 1000, 10)  # Эта переменная используется
        # Убедимся, что переменная используется
        assert product is not None  # Добавим проверку, чтобы переменная использовалась

        captured = capture_console_output.readouterr()
        output = captured.out

        # Проверяем основные части вывода
        assert "Создан объект класса Product с параметрами:" in output
        assert "Test Product" in output
        assert "1000" in output
        assert "10" in output

    def test_creation_logger_repr(self, product_class):
        """Тест метода __repr__ миксина"""
        product = product_class("Test Product", "Test Description", 1000, 10)
        repr_str = repr(product)

        assert "Product(" in repr_str
        assert "Test Product" in repr_str
        assert "1000" in repr_str
        assert "10" in repr_str


class TestProductInheritance:
    """Тесты наследования и полиморфизма"""

    def test_product_inheritance_chain(self, product_class):
        """Тест цепочки наследования"""
        from src.product import BaseProduct, CreationLoggerMixin

        assert issubclass(product_class, BaseProduct)
        assert issubclass(product_class, CreationLoggerMixin)

    def test_abstract_methods_implementation(self, product_class):
        """Тест, что все абстрактные методы реализованы"""
        product = product_class("Test", "Desc", 100, 10)
        assert product is not None
        assert str(product) is not None


class TestEnhancedProductFunctionality:
    """Тесты расширенной функциональности Product"""

    def test_product_with_mixin_functionality(self, product_class, capture_console_output):
        """Тест совместимости старой функциональности с миксином"""
        product = product_class("Test", "Desc", 100, 10)
        assert product.name == "Test"

        captured = capture_console_output.readouterr()
        assert "Создан объект класса" in captured.out

    def test_product_addition_with_mixin(self, product_class):
        """Тест сложения продуктов с миксином"""
        product1 = product_class("A", "Desc", 100, 2)
        product2 = product_class("B", "Desc", 200, 3)

        result = product1 + product2
        assert result == 100 * 2 + 200 * 3


class TestSmartphoneWithMixin:
    """Тесты для Smartphone с миксином"""

    def test_smartphone_creation_with_mixin(self, smartphone_class, capture_console_output):
        """Тест создания смартфона с миксином"""
        smartphone = smartphone_class("iPhone", "Smartphone", 99999, 2, "High", "15 Pro", 256, "Black")

        assert smartphone.name == "iPhone"

        captured = capture_console_output.readouterr()
        assert "Создан объект класса Smartphone" in captured.out

    def test_smartphone_str_representation(self, smartphone_class):
        """Тест строкового представления смартфона"""
        smartphone = smartphone_class("iPhone", "Smartphone", 99999, 2, "High", "15 Pro", 256, "Black")

        str_repr = str(smartphone)
        assert "iPhone" in str_repr
        assert "99999" in str_repr
        assert "Производительность: High" in str_repr
        assert "Модель: 15 Pro" in str_repr


class TestLawnGrassWithMixin:
    """Тесты для LawnGrass с миксином"""

    def test_lawn_grass_creation_with_mixin(self, lawn_grass_class, capture_console_output):
        """Тест создания газонной травы с миксином"""
        grass = lawn_grass_class("Premium Grass", "Lawn grass", 2500, 10, "Germany", 14, "Green")

        assert grass.name == "Premium Grass"

        captured = capture_console_output.readouterr()
        assert "Создан объект класса LawnGrass" in captured.out

    def test_lawn_grass_str_representation(self, lawn_grass_class):
        """Тест строкового представления газонной травы."""
        grass = lawn_grass_class("Premium Grass", "Lawn grass", 2500, 10, "Germany", 14, "Green")

        str_repr = str(grass)
        assert "Premium Grass" in str_repr
        assert "2500" in str_repr
        assert "Страна: Germany" in str_repr
        assert "Срок прорастания: 14" in str_repr


class TestBackwardCompatibility:
    """Тесты обратной совместимости"""

    def test_old_tests_still_work(self, product_class, smartphone_class, lawn_grass_class):
        """Тест, что старые тесты продолжают работать"""
        product = product_class("Test", "Desc", 100, 10)
        assert product.name == "Test"
        assert product.price == 100
        assert product.quantity == 10

        smartphone = smartphone_class("Phone", "Desc", 50000, 2, "High", "Model", 128, "Black")
        assert smartphone.name == "Phone"
        assert smartphone.price == 50000

        grass = lawn_grass_class("Grass", "Desc", 2000, 5, "USA", 10, "Green")
        assert grass.name == "Grass"
        assert grass.price == 2000

        result = product + product
        assert result == 100 * 10 * 2


class TestProductEdgeCases:
    """Тесты для крайних случаев Product"""

    def test_product_creation_zero_quantity(self, product_class):
        """Тест создания продукта с нулевым количеством"""
        product = product_class("Test", "Desc", 100, 0)
        assert product.quantity == 0
        assert str(product) == "Test, 100 руб. Остаток: 0 шт."

    def test_product_negative_price_creation(self, product_class):
        """Тест создания продукта с отрицательной ценой"""
        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class("Test", "Desc", -100, 10)

    def test_product_zero_price_creation(self, product_class):
        """Тест создания продукта с нулевой ценой"""
        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class("Test", "Desc", 0, 10)

    def test_product_price_setter_negative(self, product_class):
        """Тест установки отрицательной цены через сеттер"""
        product = product_class("Test", "Desc", 100, 10)
        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product.price = -50

    def test_product_price_setter_zero(self, product_class):
        """Тест установки нулевой цены через сеттер"""
        product = product_class("Test", "Desc", 100, 10)
        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product.price = 0

    def test_product_float_price(self, product_class):
        """Тест работы с float ценой"""
        product = product_class("Test", "Desc", 99.99, 5)
        assert product.price == 99.99
        product.price = 149.50
        assert product.price == 149.50


class TestProductAdditionEdgeCases:
    """Тесты для крайних случаев сложения продуктов"""

    def test_add_products_different_types_error(self, product_class, smartphone_class):
        """Тест ошибки при сложении продуктов разных типов"""
        product = product_class("Product", "Desc", 100, 10)
        smartphone = smartphone_class("Phone", "Desc", 50000, 2, "High", "Model", 128, "Black")

        with pytest.raises(TypeError):
            product + smartphone

    def test_add_product_with_invalid_type(self, product_class):
        """Тест ошибки при сложении с неправильным типом"""
        product = product_class("Product", "Desc", 100, 10)

        with pytest.raises(TypeError):
            product + "invalid"

        with pytest.raises(TypeError):
            product + 123

    def test_add_products_with_float_prices(self, product_class):
        """Тест сложения продуктов с float ценами"""
        product_a = product_class("Товар A", "Описание A", 99.99, 5)
        product_b = product_class("Товар B", "Описание B", 149.50, 3)

        result = product_a + product_b
        expected = 99.99 * 5 + 149.50 * 3
        assert abs(result - expected) < 0.01

    def test_add_product_with_zero_quantity(self, product_class):
        """Тест сложения продуктов с нулевым количеством"""
        product_a = product_class("Товар A", "Описание A", 100, 0)
        product_b = product_class("Товар B", "Описание B", 200, 5)

        result = product_a + product_b
        expected = 0 + 200 * 5
        assert result == expected

    def test_add_products_commutative(self, product_class):
        """Тест коммутативности сложения продуктов"""
        product_a = product_class("Товар A", "Описание A", 100, 10)
        product_b = product_class("Товар B", "Описание B", 200, 2)

        result1 = product_a + product_b
        result2 = product_b + product_a
        assert result1 == result2


class TestNewProductMethod:
    """Тесты для метода new_product"""

    def test_new_product_missing_name(self, product_class):
        """Тест создания продукта без имени"""
        product_data = {"description": "Desc", "price": 100, "quantity": 10}

        with pytest.raises(ValueError, match="Название товара должно быть указано"):
            product_class.new_product(product_data)

    def test_new_product_negative_price(self, product_class):
        """Тест создания продукта с отрицательной ценой через new_product"""
        product_data = {"name": "Test", "description": "Desc", "price": -100, "quantity": 10}

        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class.new_product(product_data)

    def test_new_product_zero_price(self, product_class):
        """Тест создания продукта с нулевой ценой через new_product"""
        product_data = {"name": "Test", "description": "Desc", "price": 0, "quantity": 10}

        with pytest.raises(ValueError, match="Цена не должна быть нулевая или отрицательная"):
            product_class.new_product(product_data)

    def test_new_product_update_existing_with_higher_price(self, product_class):
        """Тест обновления существующего продукта с более высокой ценой"""
        existing_product = product_class("Existing", "Desc", 100, 10)
        product_data = {"name": "Existing", "price": 150, "quantity": 5}

        updated = product_class.new_product(product_data, [existing_product])
        assert updated is existing_product
        assert updated.price == 150
        assert updated.quantity == 15

    def test_new_product_update_existing_with_lower_price(self, product_class):
        """Тест обновления существующего продукта с более низкой ценой"""
        existing_product = product_class("Existing", "Desc", 100, 10)
        product_data = {"name": "Existing", "price": 50, "quantity": 5}

        updated = product_class.new_product(product_data, [existing_product])
        assert updated is existing_product
        assert updated.price == 100
        assert updated.quantity == 15

    def test_new_product_update_existing_with_description(self, product_class):
        """Тест обновления существующего продукта с новым описанием"""
        existing_product = product_class("Existing", "Old Desc", 100, 10)
        product_data = {"name": "Existing", "description": "New Desc", "price": 100, "quantity": 5}

        updated = product_class.new_product(product_data, [existing_product])
        assert updated is existing_product
        assert updated.description == "New Desc"
        assert updated.quantity == 15

    def test_new_product_create_new(self, product_class):
        """Тест создания нового продукта через new_product"""
        product_data = {"name": "New Product", "description": "Desc", "price": 100, "quantity": 10}

        product = product_class.new_product(product_data)
        assert product.name == "New Product"
        assert product.price == 100
        assert product.quantity == 10

    def test_new_product_case_insensitive_name_matching(self, product_class):
        """Тест нечувствительного к регистру сравнения имен"""
        existing_product = product_class("Existing", "Desc", 100, 10)
        product_data = {"name": "EXISTING", "price": 150, "quantity": 5}

        updated = product_class.new_product(product_data, [existing_product])
        assert updated is existing_product
        assert updated.quantity == 15


class TestSmartphoneSpecific:
    """Тесты специфичные для Smartphone"""

    def test_smartphone_addition_same_type(self, smartphone_class):
        """Тест сложения смартфонов одного типа"""
        phone1 = smartphone_class("Phone1", "Desc", 50000, 2, "High", "Model", 128, "Black")
        phone2 = smartphone_class("Phone2", "Desc", 60000, 3, "High", "Model", 256, "White")

        result = phone1 + phone2
        assert result == 50000 * 2 + 60000 * 3

    def test_smartphone_addition_different_type_error(self, smartphone_class, product_class):
        """Тест ошибки при сложении смартфона с другим типом"""
        phone = smartphone_class("Phone", "Desc", 50000, 2, "High", "Model", 128, "Black")
        product = product_class("Product", "Desc", 100, 10)

        with pytest.raises(TypeError):
            phone + product

    def test_smartphone_attributes(self, smartphone_class):
        """Тест атрибутов смартфона"""
        smartphone = smartphone_class("Phone", "Desc", 50000, 2, "High", "Model X", 256, "Blue")

        assert smartphone.efficiency == "High"
        assert smartphone.model == "Model X"
        assert smartphone.memory == 256
        assert smartphone.color == "Blue"


class TestLawnGrassSpecific:
    """Тесты специфичные для LawnGrass"""

    def test_lawn_grass_addition_same_type(self, lawn_grass_class):
        """Тест сложения газонных трав одного типа"""
        grass1 = lawn_grass_class("Grass1", "Desc", 2000, 5, "USA", 10, "Green")
        grass2 = lawn_grass_class("Grass2", "Desc", 2500, 3, "Germany", 14, "Dark Green")

        result = grass1 + grass2
        assert result == 2000 * 5 + 2500 * 3

    def test_lawn_grass_addition_different_type_error(self, lawn_grass_class, product_class):
        """Тест ошибки при сложении газонной травы с другим типом"""
        grass = lawn_grass_class("Grass", "Desc", 2000, 5, "USA", 10, "Green")
        product = product_class("Product", "Desc", 100, 10)

        with pytest.raises(TypeError):
            grass + product

    def test_lawn_grass_attributes(self, lawn_grass_class):
        """Тест атрибутов газонной травы"""
        grass = lawn_grass_class("Grass", "Desc", 2000, 5, "France", 12, "Dark Green")

        assert grass.country == "France"
        assert grass.germination_period == 12
        assert grass.color == "Dark Green"


class TestProductRepr:
    """Тесты для методов __repr__"""

    def test_product_repr(self, product_class):
        """Тест __repr__ для Product"""
        product = product_class("Test", "Description", 100, 10)
        repr_str = repr(product)

        assert "Product(" in repr_str
        assert "name='Test'" in repr_str
        assert "description='Description'" in repr_str
        assert "price=100" in repr_str
        assert "quantity=10" in repr_str

    def test_smartphone_repr(self, smartphone_class):
        """Тест __repr__ для Smartphone"""
        smartphone = smartphone_class("Phone", "Desc", 50000, 2, "High", "Model X", 256, "Blue")
        repr_str = repr(smartphone)

        assert "Smartphone(" in repr_str
        assert "efficiency='High'" in repr_str
        assert "model='Model X'" in repr_str
        assert "memory=256" in repr_str
        assert "color='Blue'" in repr_str

    def test_lawn_grass_repr(self, lawn_grass_class):
        """Тест __repr__ для LawnGrass"""
        grass = lawn_grass_class("Grass", "Desc", 2000, 5, "France", 12, "Dark Green")
        repr_str = repr(grass)

        assert "LawnGrass(" in repr_str
        assert "country='France'" in repr_str
        assert "germination_period=12" in repr_str
        assert "color='Dark Green'" in repr_str

    class TestProductReprAdvanced:
        """Расширенные тесты для методов __repr__"""

    def test_product_repr_with_special_chars(self, product_class):
        """Тест __repr__ с специальными символами в названии"""
        product = product_class("Test's Product", 'Description with "quotes"', 100, 10)
        repr_str = repr(product)

        assert "Test's Product" in repr_str
        assert 'Description with "quotes"' in repr_str

    def test_smartphone_repr_all_attributes(self, smartphone_class):
        """Тест __repr__ со всеми атрибутами смартфона"""
        smartphone = smartphone_class(
            "Phone", "Description", 50000, 2, "Very High", "Model X Pro", 512, "Midnight Blue"
        )
        repr_str = repr(smartphone)

        assert all(
            attr in repr_str
            for attr in ["Phone", "Description", "50000", "2", "Very High", "Model X Pro", "512", "Midnight Blue"]
        )


class TestProductPricePrecision:
    """Тесты точности цен"""

    def test_product_high_precision_price(self, product_class):
        """Тест высокой точности цены"""
        product = product_class("Test", "Desc", 123.456789, 10)
        assert abs(product.price - 123.456789) < 0.000001

        product.price = 987.654321
        assert abs(product.price - 987.654321) < 0.000001


class TestProductQuantityEdgeCases:
    """Тесты крайних случаев количества"""

    def test_product_large_quantity(self, product_class):
        """Тест большого количества"""
        product = product_class("Test", "Desc", 100, 1000000)
        assert product.quantity == 1000000

        # Тест сложения с большими количествами
        product2 = product_class("Test2", "Desc2", 200, 500000)
        result = product + product2
        assert result == 100 * 1000000 + 200 * 500000

    def test_product_quantity_overflow(self, product_class):
        """Тест на переполнение количества (должен работать нормально)"""
        product = product_class("Test", "Desc", 100, 10)
        product2 = product_class("Test2", "Desc2", 200, 20)

        result = product + product2
        assert result == 100 * 10 + 200 * 20
