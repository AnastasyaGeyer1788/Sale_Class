import json
import os
import pytest
from unittest.mock import mock_open, patch

from src.utils import read_json, create_objects_from_json
from src.category import Category


def test_read_json_file_exists(tmp_path):
    """Тест чтения существующего JSON файла"""
    # Создаем временный файл
    test_data = {"key": "value", "number": 42}
    test_file = tmp_path / "test.json"
    test_file.write_text(json.dumps(test_data), encoding="UTF-8")

    # Читаем файл
    result = read_json(str(test_file))

    assert result == test_data


def test_read_json_file_not_exists():
    """Тест чтения несуществующего JSON файла"""
    with pytest.raises(FileNotFoundError):
        read_json("non_existent_file.json")


def test_read_json_invalid_json(tmp_path):
    """Тест чтения файла с невалидным JSON"""
    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json}", encoding="UTF-8")

    with pytest.raises(json.JSONDecodeError):
        read_json(str(test_file))


def test_create_objects_from_json_empty_data():
    """Тест создания объектов из пустых данных"""
    result = create_objects_from_json([])
    assert result == []
    assert len(result) == 0


def test_create_objects_from_json_valid_data():
    """Тест создания объектов из валидных данных JSON"""
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Мобильные устройства",
            "products": [
                {"name": "iPhone 15", "description": "Новый iPhone", "price": 100000.0, "quantity": 10},
                {"name": "Samsung Galaxy", "description": "Android smartphone", "price": 80000.0, "quantity": 5},
            ],
        },
        {
            "name": "Ноутбуки",
            "description": "Компьютерная техника",
            "products": [{"name": "MacBook Pro", "description": "Apple notebook", "price": 200000.0, "quantity": 3}],
        },
    ]

    categories = create_objects_from_json(test_data)

    # Проверяем количество категорий
    assert len(categories) == 2
    assert isinstance(categories[0], Category)
    assert isinstance(categories[1], Category)

    # Проверяем первую категорию
    assert categories[0].name == "Смартфоны"
    assert categories[0].description == "Мобильные устройства"

    # Вместо проверки объектов Product, проверяем форматированный вывод
    products_output = categories[0].products
    assert len(products_output) == 2
    assert "iPhone 15, 100000.0 руб. Остаток: 10 шт." in products_output[0]
    assert "Samsung Galaxy, 80000.0 руб. Остаток: 5 шт." in products_output[1]

    # Проверяем вторую категорию
    assert categories[1].name == "Ноутбуки"
    assert categories[1].description == "Компьютерная техника"

    # Проверяем вывод продуктов второй категории
    products_output_2 = categories[1].products
    assert len(products_output_2) == 1
    assert "MacBook Pro, 200000.0 руб. Остаток: 3 шт." in products_output_2[0]


def test_create_objects_from_json_with_missing_fields():
    """Тест создания объектов с отсутствующими полями"""
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар без цены",
                    "description": "Описание",
                    # Нет price и quantity - должны быть значения по умолчанию
                }
            ],
        }
    ]

    # Должно вызвать исключение при создании Product
    with pytest.raises(TypeError):
        create_objects_from_json(test_data)


def test_read_json_with_mock():
    """Тест read_json с использованием mock"""
    test_data = {"test": "data", "number": 123}

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))) as mock_file:
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = test_data

            result = read_json("dummy_path.json")

            # Проверяем, что файл был открыт с правильными параметрами
            mock_file.assert_called_once_with(os.path.abspath("dummy_path.json"), "r", encoding="UTF-8")
            mock_json_load.assert_called_once()
            assert result == test_data


def test_create_objects_from_json_with_empty_products():
    """Тест создания категорий с пустыми продуктами"""
    test_data = [{"name": "Пустая категория", "description": "Без продуктов", "products": []}]

    categories = create_objects_from_json(test_data)

    assert len(categories) == 1
    assert categories[0].name == "Пустая категория"
    assert categories[0].description == "Без продуктов"
    assert len(categories[0].products) == 0


def test_read_json_absolute_path(tmp_path):
    """Тест чтения JSON с абсолютным путем"""
    test_data = {"absolute": "path_test"}
    test_file = tmp_path / "absolute_test.json"
    test_file.write_text(json.dumps(test_data), encoding="UTF-8")

    result = read_json(str(test_file))
    assert result == test_data
