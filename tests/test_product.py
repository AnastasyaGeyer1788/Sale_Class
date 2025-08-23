from src.product import Product


def test_product_initialization_int_price():
    """Тест инициализации продукта с целочисленной ценой"""
    product = Product("Samsung Galaxy", "256GB, Серый", 180000, 5)

    assert product.name == "Samsung Galaxy"
    assert product.description == "256GB, Серый"
    assert product.price == 180000
    assert isinstance(product.price, int)
    assert product.quantity == 5


def test_product_initialization_float_price():
    """Тест инициализации продукта с дробной ценой"""
    product = Product("iPhone", "512GB, Space Gray", 210000.99, 8)

    assert product.name == "iPhone"
    assert product.description == "512GB, Space Gray"
    assert product.price == 210000.99
    assert isinstance(product.price, float)
    assert product.quantity == 8


def test_product_price_types_mixed():
    """Тест работы с разными типами цен в разных продуктах"""
    # Целое число
    product1 = Product("Test 1", "Desc", 100, 5)
    assert product1.price == 100
    assert isinstance(product1.price, int)

    # Дробное число
    product2 = Product("Test 2", "Desc", 99.99, 5)
    assert product2.price == 99.99
    assert isinstance(product2.price, float)


def test_product_zero_price_int():
    """Тест продукта с нулевой целочисленной ценой"""
    product = Product("Free Product", "Description", 0, 10)
    assert product.price == 0
    assert isinstance(product.price, int)


def test_product_zero_price_float():
    """Тест продукта с нулевой дробной ценой"""
    product = Product("Free Product", "Description", 0.0, 10)
    assert product.price == 0.0
    assert isinstance(product.price, float)


def test_product_decimal_price():
    """Тест продукта с десятичной ценой"""
    product = Product("Test Product", "Description", 123.45, 7)
    assert product.price == 123.45
    assert isinstance(product.price, float)


def test_product_large_int_price():
    """Тест продукта с большой целочисленной ценой"""
    product = Product("Expensive", "Very expensive", 1000000, 1)
    assert product.price == 1000000
    assert isinstance(product.price, int)


def test_product_large_float_price():
    """Тест продукта с большой дробной ценой"""
    product = Product("Very Expensive", "Extremely expensive", 999999.99, 1)
    assert product.price == 999999.99
    assert isinstance(product.price, float)


def test_product_attributes_types():
    """Тест типов атрибутов продукта"""
    product = Product("Test", "Description", 1000, 10)
    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, (int, float))
    assert isinstance(product.quantity, int)
