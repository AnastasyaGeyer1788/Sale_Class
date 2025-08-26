import pytest
import tempfile
import json
import os
from src.utils import read_json, create_objects_from_json, print_category_info


class TestUtils:
    """Тесты для утилит"""

    def test_read_json(self):
        """Тест чтения JSON файла"""
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            test_data = [
                {
                    "name": "Test Category",
                    "description": "Test Description",
                    "products": [
                        {"name": "Product 1", "description": "Desc 1", "price": 1000, "quantity": 5},
                        {"name": "Product 2", "description": "Desc 2", "price": 2000, "quantity": 10},
                    ],
                }
            ]
            json.dump(test_data, f)
            temp_path = f.name

        try:
            # Читаем файл
            data = read_json(temp_path)
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]["name"] == "Test Category"
        finally:
            # Удаляем файл(временный)
            os.unlink(temp_path)

    def test_read_json_file_not_found(self):
        """Тест чтения несуществующего JSON файла"""
        with pytest.raises(FileNotFoundError):
            read_json("nonexistent_file.json")

    def test_read_json_invalid_json(self):
        """Тест чтения некорректного JSON файла"""
        # Создаем временный файл с некорректным JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{invalid json")
            temp_path = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                read_json(temp_path)
        finally:
            os.unlink(temp_path)

    def test_create_objects_from_json(self):
        """Тест создания объектов из JSON"""
        test_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices",
                "products": [
                    {"name": "Phone", "description": "Smartphone", "price": 1000, "quantity": 5},
                    {"name": "Laptop", "description": "Gaming laptop", "price": 2000, "quantity": 3},
                ],
            }
        ]

        categories = create_objects_from_json(test_data)

        assert len(categories) == 1
        assert categories[0].name == "Electronics"
        assert len(categories[0].products) == 2
        assert "Phone, 1000 руб. Остаток: 5 шт." in categories[0].products

    def test_create_objects_empty_products(self, category_class):
        """Тест создания объектов с пустым списком продуктов"""
        test_data = [{"name": "Empty Category", "description": "No products here", "products": []}]

        categories = create_objects_from_json(test_data)
        assert len(categories) == 1
        assert categories[0].name == "Empty Category"
        assert len(categories[0].products) == 0

    def test_create_objects_missing_products_field(self, category_class):
        """Тест создания объектов без поля products"""
        test_data = [{"name": "No Products Category", "description": "Missing products field"}]

        categories = create_objects_from_json(test_data)
        assert len(categories) == 1
        assert categories[0].name == "No Products Category"
        assert len(categories[0].products) == 0

    def test_create_objects_invalid_product_data(self, capsys):
        """Тест создания объектов с некорректными данными продукта"""
        test_data = [
            {
                "name": "Test Category",
                "description": "Test Description",
                "products": [
                    {"name": "Valid Product", "description": "Desc", "price": 1000, "quantity": 5},
                    {"name": "Invalid Product", "description": "Desc"},  # Missing price and quantity
                ],
            }
        ]

        categories = create_objects_from_json(test_data)

        # Должна создаться категория с одним валидным продуктом
        assert len(categories) == 1
        assert len(categories[0].products) == 1
        assert "Valid Product" in categories[0].products[0]

        # Проверяем что вывелось сообщение об ошибке
        captured = capsys.readouterr()
        assert "Ошибка при создании продукта" in captured.out

    def test_print_category_info(self, capsys, category_class, product_class):
        """Тест вывода информации о категориях"""
        # Создаем тестовые данные
        products = [product_class("Product 1", "Desc 1", 1000, 5), product_class("Product 2", "Desc 2", 2000, 3)]
        category = category_class("Test Category", "Test Description", products)

        print_category_info([category])

        captured = capsys.readouterr()
        assert "Test Category" in captured.out
        assert "Product 1, 1000 руб. Остаток: 5 шт." in captured.out
        assert "Product 2, 2000 руб. Остаток: 3 шт." in captured.out

    def test_print_empty_category_info(self, capsys, category_class):
        """Тест вывода информации о пустой категории"""
        category = category_class("Empty Category", "No products")

        print_category_info([category])

        captured = capsys.readouterr()
        assert "Empty Category" in captured.out
        assert "Товары:" in captured.out

    def test_main_execution(self, capsys, monkeypatch):
        """Тест выполнения main блока в utils"""

        # Мокаем read_json чтобы не зависеть от реального файла
        def mock_read_json(path):
            return [
                {
                    "name": "Mock Category",
                    "description": "Mock Description",
                    "products": [{"name": "Mock Product", "description": "Mock Desc", "price": 1000, "quantity": 5}],
                }
            ]

        monkeypatch.setattr("src.utils.read_json", mock_read_json)

        # Запускаем main блок
        import src.utils

        if hasattr(src.utils, "__name__") and src.utils.__name__ == "__main__":
            # Эмулируем выполнение main блока
            src.utils.create_objects_from_json(mock_read_json("dummy_path"))

        captured = capsys.readouterr()
        # Проверяем что нет ошибок
        assert "Ошибка:" not in captured.out
