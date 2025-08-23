import json
import os

from src.category import Category
from src.product import Product


def read_json(path: str) -> dict:
    """Считывает данные из json файла"""
    full_path = os.path.abspath(path)
    with open(full_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def create_objects_from_json(data):
    """Создает объекты Category и Product из данных JSON"""
    categories = []
    for category_data in data:
        products = []
        for product_data in category_data["products"]:
            # Создаем Product используя распаковку словаря
            products.append(Product(**product_data))

        # Создаем Category используя распаковку словаря
        category_data["products"] = products
        categories.append(Category(**category_data))

    return categories


if __name__ == "__main__":
    data = read_json("../data/products.json")

    # Создаем объекты
    categories = create_objects_from_json(data)

    print(categories[0].name)  # Название категории
    print(categories[0].description)  # Описание категории
    print(categories[0].products)  # Список продуктов

    print(categories[0].products[0].name)  # Название продукта
    print(categories[0].products[0].price)  # Цена продукта
    print(categories[0].products[0].quantity)  # Количество продукта
