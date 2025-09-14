import pytest


class TestProductEdgeCasesFixed:
    """Исправленные тесты для крайних случаев Product"""

    def test_product_creation_zero_quantity_raises_error(self, product_class):
        """Тест что создание продукта с нулевым количеством вызывает исключение"""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            product_class("Test", "Desc", 100, 0)

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


class TestProductAdditionEdgeCasesFixed:
    """Исправленные тесты для крайних случаев сложения продуктов"""

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

    def test_add_products_commutative(self, product_class):
        """Тест коммутативности сложения продуктов"""
        product_a = product_class("Товар A", "Описание A", 100, 10)
        product_b = product_class("Товар B", "Описание B", 200, 2)

        result1 = product_a + product_b
        result2 = product_b + product_a
        assert result1 == result2


class TestProductReprFixed:
    """Исправленные тесты для методов __repr__"""

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
