from typing import Union, List, Optional
from src.product import Product


class Category:
    # Атрибуты класса
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List["Product"]] = None):
        """
        Конструктор класса Category.
        :param name: Название категории
        :param description: Описание категории
        :param products: Список товаров в категории
        """
        self.name = name
        self.description = description
        self.__products = products if products else []  # Приватный атрибут

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: "Product") -> None:
        """
        Добавляет товар в категорию с проверкой типа.
        :param product: Объект класса Product для добавления
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        """
        Геттер для вывода списка товаров в формате:
        Название продукта, цена руб. Остаток: количество шт.
        """
        products_list = []
        for product in self.__products:
            products_list.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return products_list
