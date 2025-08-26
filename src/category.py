from typing import List, Optional
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
        # Обновляем общее количество товаров

    def __str__(self) -> str:
        """
        Магический метод для строкового представления объекта Category.
        :return: Строка в формате "Название категории, количество продуктов: X шт."
        """
        total_products = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_products} шт."

    def add_product(self, product: "Product") -> None:
        """
        Добавляет товар в категорию с проверкой типа.
        :param product: Объект класса Product для добавления
        """
        # Проверяем, что объект является экземпляром Product или его подклассов
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        # Дополнительная проверка с помощью issubclass
        if not issubclass(type(product), Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        self.__products.append(product)
        Category.product_count += product.quantity

    @property
    def products(self) -> List[str]:
        """
        Геттер для вывода списка товаров.
        Теперь использует строковое представление объектов Product.
        """
        return [str(product) for product in self.__products]

    @property
    def total_products_quantity(self) -> int:
        """
        Геттер для получения общего количества товаров в категории.
        :return: Сумма quantity всех продуктов в категории
        """
        return sum(product.quantity for product in self.__products)
