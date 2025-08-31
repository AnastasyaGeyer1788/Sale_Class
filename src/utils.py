import json
import os
from typing import List, Dict, Any, Tuple

from src.category import Category
from src.product import Product


def read_json(path: str) -> List[Dict[str, Any]]:
    """Считывает данные из json файла"""
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def create_objects_from_json(data: List[Dict[str, Any]]) -> Tuple[List[Category], List[Product]]:
    """Создает объекты Category и Product из данных JSON"""
    categories = []
    all_products = []

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
                all_products.append(product)
            except KeyError as e:
                print(f"Ошибка при создании продукта: отсутствует поле {e}")
                continue
            except ValueError as e:
                print(f"Ошибка при создании продукта: {e}")
                continue

        # Создаем категорию
        try:
            category = Category(
                name=category_data["name"], description=category_data["description"], products=products
            )
            categories.append(category)
        except KeyError as e:
            print(f"Ошибка при создании категории: отсутствует поле {e}")
            continue

    return categories, all_products


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
        categories, products = create_objects_from_json(data)

        # Выводим информацию
        print_category_info(categories)

        # Дополнительные проверки
        if categories:
            print(f"\nВсего категорий: {Category.category_count}")
            print(f"Всего товаров: {Category.product_count}")

            # Пример доступа к конкретному товару
            first_category = categories[0]
            if first_category.products:
                print(f"Первый товар в первой категории: {first_category.products[0]}")

    except FileNotFoundError:
        print("Ошибка: Файл products.json не найден!")
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON файла!")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
