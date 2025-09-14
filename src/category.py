from typing import List, Optional
from src.product import Product


class Category:
    """Класс для представления категории товаров."""

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
        # Обновляем общее количество товаров для начальных продуктов
        for product in self.__products:
            Category.product_count += product.quantity

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

        # Проверяем, что количество товара не равно нулю
        if product.quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.__products.append(product)
        Category.product_count += product.quantity

    @property
    def products(self) -> List[str]:
        """Геттер для вывода списка товаров."""
        return [str(product) for product in self.__products]

    @property
    def total_products_quantity(self) -> int:
        """
        Геттер для получения общего количества товаров в категории.

        :return: Сумма quantity всех продуктов в категории
        """
        return sum(product.quantity for product in self.__products)

    def get_average_price(self) -> float:
        """
        Метод для подсчета среднего ценника всех товаров в категории.

        :return: Средняя цена товаров в категории или 0, если товаров нет
        """
        try:
            # Пытаемся вычислить среднюю цену
            total_price = sum(product.price * product.quantity for product in self.__products)
            total_quantity = self.total_products_quantity

            # Проверяем, что общее количество не равно нулю
            if total_quantity == 0:
                return 0.0

            average_price = total_price / total_quantity
            return round(average_price, 2)

        except ZeroDivisionError:
            # Обрабатываем случай деления на ноль
            return 0.0
        except Exception as e:
            # Обрабатываем любые другие исключения
            print(f"Произошла ошибка при вычислении средней цены: {e}")
            return 0.0

    def middle_price(self) -> float:
        """
        Для совместимости с тестовым файлом.

        Вызывает get_average_price().
        """
        return self.get_average_price()
