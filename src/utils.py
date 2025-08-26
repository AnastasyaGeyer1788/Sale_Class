import json
import os
from typing import List, Dict, Any

from src.category import Category
from src.product import Product


def read_json(path: str) -> List[Dict[str, Any]]:
    """Считывает данные из json файла"""
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def create_objects_from_json(data: List[Dict[str, Any]]) -> List[Category]:
    """Создает объекты Category и Product из данных JSON"""
    categories = []

    for category_data in data:
        # Создаем продукты для этой категории
        products = []
        for product_data in category_data.get("products", []):
            try:
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    quantity=product_data["quantity"],
                )
                products.append(product)
            except KeyError as e:
                print(f"Ошибка при создании продукта: отсутствует поле {e}")
                continue
            except ValueError as e:
                print(f"Ошибка при создании продукта: {e}")
                continue

        # Создаем категорию и добавляем продукты через add_product
        category = Category(name=category_data["name"], description=category_data["description"])

        # Добавляем продукты в категорию
        for product in products:
            category.add_product(product)

        categories.append(category)

    return categories


def print_category_info(categories: List[Category]) -> None:
    """Выводит информацию о категориях и товарах"""
    for i, category in enumerate(categories, 1):
        print(f"\n--- Категория {i}: {category.name} ---")
        print(f"Описание: {category.description}")
        print("Товары:")

        for product_info in category.products:
            print(f"  - {product_info}")


if __name__ == "__main__":
    try:
        data = read_json("../data/products.json")

        # Создаем объекты
        categories = create_objects_from_json(data)

        # Выводим информацию
        print_category_info(categories)

        # Дополнительные проверки
        if categories:
            print(f"Всего категорий: {Category.category_count}")
            print(f"Всего товаров: {Category.product_count}")

            # Пример доступа к конкретному товару
            first_category = categories[0]
            if first_category.products:
                first_product = first_category.products[0]
                print(f"Первый товар: {first_product}")

    except FileNotFoundError:
        print("Ошибка: Файл products.json не найден!")
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON файла!")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
