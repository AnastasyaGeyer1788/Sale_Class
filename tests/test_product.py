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


def test_product_zero_price_int(capsys):
    """Тест продукта с нулевой целочисленной ценой"""
    product = Product("Free Product", "Description", 0, 10)

    # Проверяем сообщение об ошибке
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out

    assert product.price == 0
    assert isinstance(product.price, int)


def test_product_zero_price_float(capsys):
    """Тест продукта с нулевой дробной ценой"""
    product = Product("Free Product", "Description", 0.0, 10)

    # Проверяем сообщение об ошибке
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out

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


# Новые тесты для приватной цены и геттеров/сеттеров
def test_price_getter():
    """Тест геттера для цены"""
    product = Product("Test Product", "Test Description", 1000, 10)
    assert product.price == 1000
    assert isinstance(product.price, int)


def test_price_setter_valid():
    """Тест сеттера для корректной цены"""
    product = Product("Test Product", "Test Description", 1000, 10)

    # Устанавливаем новую цену
    product.price = 1500
    assert product.price == 1500

    # Устанавливаем дробную цену
    product.price = 2000.50
    assert product.price == 2000.50
    assert isinstance(product.price, float)


def test_price_setter_invalid_negative(capsys):
    """Тест сеттера для отрицательной цены"""
    product = Product("Test Product", "Test Description", 1000, 10)
    original_price = product.price

    # Пытаемся установить отрицательную цену
    product.price = -100

    # Проверяем сообщение об ошибке
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out

    # Проверяем, что цена не изменилась
    assert product.price == original_price


def test_price_setter_invalid_zero(capsys):
    """Тест сеттера для нулевой цены"""
    product = Product("Test Product", "Test Description", 1000, 10)
    original_price = product.price

    # Пытаемся установить нулевую цену
    product.price = 0

    # Проверяем сообщение об ошибке
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out

    # Проверяем, что цена не изменилась
    assert product.price == original_price


def test_price_types_consistency():
    """Тест сохранения типов данных при работе с ценой"""
    # int цена
    product_int = Product("Int Product", "Desc", 1000, 5)
    assert isinstance(product_int.price, int)

    product_int.price = 1500
    assert isinstance(product_int.price, int)

    # float цена
    product_float = Product("Float Product", "Desc", 1000.50, 5)
    assert isinstance(product_float.price, float)

    product_float.price = 1500.75
    assert isinstance(product_float.price, float)

    # Смена типа (int -> float)
    product_int.price = 2000.25
    assert isinstance(product_int.price, float)

    # Смена типа (float -> int)
    product_float.price = 3000
    assert isinstance(product_float.price, int)


# Тесты для класс-метода new_product
def test_new_product_creation():
    """Тест создания нового товара через класс-метод"""
    product_data = {"name": "Test Product", "description": "Test Description", "price": 1000, "quantity": 5}

    product = Product.new_product(product_data)

    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 1000
    assert product.quantity == 5


def test_new_product_duplicate_update():
    """Тест обновления существующего товара через класс-метод"""
    existing_products = [Product("Existing Product", "Old Desc", 1000, 5)]

    product_data = {
        "name": "Existing Product",
        "description": "New Desc",
        "price": 1500,  # Более высокая цена
        "quantity": 3,  # Добавляемое количество
    }

    product = Product.new_product(product_data, existing_products)

    # Проверяем обновление
    assert product.name == "Existing Product"
    assert product.description == "New Desc"  # Описание обновилось
    assert product.price == 1500  # Цена увеличилась
    assert product.quantity == 8  # 5 + 3 = 8

    # Проверяем, что это тот же объект
    assert product is existing_products[0]


def test_new_product_duplicate_lower_price():
    """Тест, что при дубликате с меньшей ценой цена не меняется"""
    existing_products = [Product("Existing Product", "Desc", 1000, 5)]

    product_data = {"name": "Existing Product", "description": "Desc", "price": 500, "quantity": 3}  # Меньшая цена

    product = Product.new_product(product_data, existing_products)

    assert product.price == 1000  # Цена осталась прежней (большая)
    assert product.quantity == 8  # Количество увеличилось


def test_new_product_case_insensitive():
    """Тест регистронезависимого сравнения названий"""
    existing_products = [Product("iPhone", "Desc", 1000, 5)]

    product_data = {"name": "IPHONE", "description": "New Desc", "price": 1500, "quantity": 3}  # Разный регистр

    product = Product.new_product(product_data, existing_products)

    # Должен найти дубликат и обновить
    assert product.name == "iPhone"  # Оригинальное название
    assert product.quantity == 8


def test_new_product_invalid_price(capsys):
    """Тест создания товара с некорректной ценой через класс-метод"""
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": -100,  # Некорректная цена
        "quantity": 5,
    }

    product = Product.new_product(product_data)

    # Проверяем сообщение об ошибке
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out

    # Но продукт создается
    assert product.name == "Test Product"
    assert product.quantity == 5
