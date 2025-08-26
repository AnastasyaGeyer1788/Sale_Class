import pytest
from src.product import Product, Smartphone, LawnGrass


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
        # Создаем категории
        category1 = category_class("Category 1", "Desc 1")
        category2 = category_class("Category 2", "Desc 2")

        # Добавляем продукты вручную, чтобы увеличить счетчик
        for product in sample_products[:2]:
            category1.add_product(product)
        for product in sample_products[2:]:
            category2.add_product(product)

        # Проверяем что категории созданы правильно
        assert category1.name == "Category 1"
        assert category2.name == "Category 2"
        assert len(category1.products) == 2
        assert len(category2.products) == 1

        assert category_class.category_count == 2
        # Общее количество товаров: 5 + 8 + 12 = 25
        assert category_class.product_count == 25

    def test_str_representation(self, category_class, sample_products):
        """Тест строкового представления категории"""
        category = category_class("Электроника", "Техника", sample_products)

        # Сумма quantity всех продуктов: 5 + 8 + 12 = 25
        expected_str = "Электроника, количество продуктов: 25 шт."
        assert str(category) == expected_str

    def test_str_representation_empty_category(self, category_class):
        """Тест строкового представления пустой категории"""
        category = category_class("Электроника", "Техника")

        expected_str = "Электроника, количество продуктов: 0 шт."
        assert str(category) == expected_str

    def test_total_products_quantity(self, category_class, sample_products):
        """Тест геттера общего количества товаров"""
        category = category_class("Электроника", "Техника", sample_products)

        assert category.total_products_quantity == 25  # 5 + 8 + 12

    def test_products_getter_uses_str_method(self, category_class, sample_products):
        """Тест что геттер products использует __str__ метод продуктов"""
        category = category_class("Электроника", "Техника", sample_products)

        products_list = category.products

        # Проверяем что все элементы являются строковыми представлениями продуктов
        assert products_list[0] == "Product 1, 1000 руб. Остаток: 5 шт."
        assert products_list[1] == "Product 2, 2000.0 руб. Остаток: 8 шт."
        assert products_list[2] == "Product 3, 3000.5 руб. Остаток: 12 шт."

    def test_category_counters_with_quantity(self, category_class):
        """Тест, что счетчики правильно учитывают quantity продуктов"""
        products = [Product("Product 1", "Desc 1", 1000, 10), Product("Product 2", "Desc 2", 2000, 5)]

        category = category_class("Test Category", "Test Description")

        # Добавляем продукты через add_product, чтобы увеличить счетчики
        for product in products:
            category.add_product(product)

        # Проверяем что категория создана правильно
        assert category.name == "Test Category"
        assert len(category.products) == 2

        # Должно быть 15 товаров (10 + 5)
        assert category_class.product_count == 15


class TestCategoryProductValidation:
    """Тесты для проверки валидации типов продуктов в категории"""

    def test_add_valid_product(self, category_class, sample_product):
        """Тест добавления валидного продукта"""
        category = category_class("Test Category", "Test Description")
        category.add_product(sample_product)
        assert len(category.products) == 1

    def test_add_smartphone_product(self, category_class):
        """Тест добавления смартфона (наследник Product)"""
        category = category_class("Test Category", "Test Description")
        smartphone = Smartphone("iPhone", "Smartphone", 100000, 5, "High", "15 Pro", 256, "Black")

        category.add_product(smartphone)
        assert len(category.products) == 1

    def test_add_lawn_grass_product(self, category_class):
        """Тест добавления газонной травы (наследник Product)"""
        category = category_class("Test Category", "Test Description")
        lawn_grass = LawnGrass("Premium Grass", "Lawn grass", 5000, 20, "Germany", 14, "Green")

        category.add_product(lawn_grass)
        assert len(category.products) == 1

    def test_add_invalid_string_product(self, category_class):
        """Тест добавления строки вместо продукта"""
        category = category_class("Test Category", "Test Description")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product("invalid product")

    def test_add_integer_product(self, category_class):
        """Тест добавления числа вместо продукта"""
        category = category_class("Test Category", "Test Description")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product(123)

    def test_add_list_product(self, category_class):
        """Тест добавления списка вместо продукта"""
        category = category_class("Test Category", "Test Description")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product(["product1", "product2"])

    def test_add_dict_product(self, category_class):
        """Тест добавления словаря вместо продукта"""
        category = category_class("Test Category", "Test Description")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product({"name": "test", "price": 100})

    def test_add_none_product(self, category_class):
        """Тест добавления None вместо продукта"""
        category = category_class("Test Category", "Test Description")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product(None)

    def test_add_custom_object_product(self, category_class):
        """Тест добавления пользовательского объекта вместо продукта"""

        class CustomObject:
            def __init__(self, name):
                self.name = name

        category = category_class("Test Category", "Test Description")
        custom_obj = CustomObject("test")

        with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product или его наследников"):
            category.add_product(custom_obj)

    def test_add_multiple_valid_products(self, category_class, sample_product):
        """Тест добавления нескольких валидных продуктов разных типов"""
        category = category_class("Test Category", "Test Description")

        # Обычный продукт
        product1 = sample_product
        # Смартфон
        product2 = Smartphone("Smartphone", "Desc", 50000, 3, "High", "Model", 128, "Blue")
        # Газонная трава
        product3 = LawnGrass("Grass", "Desc", 2000, 10, "USA", 10, "Green")

        category.add_product(product1)
        category.add_product(product2)
        category.add_product(product3)

        assert len(category.products) == 3

    def test_initialization_with_valid_products(self, category_class, sample_products):
        """Тест инициализации категории с валидными продуктами"""
        category = category_class("Test Category", "Test Description", sample_products)
        assert len(category.products) == 3
