from typing import Union, List, Optional


class Product:
    """Класс Product представляет товар в магазине.
    :param name: Название продукта
    :param description: Описание продукта
    :param price: Цена продукта
    :param quantity: Количество доступных единиц продукта
    """

    def __init__(self, name: str, description: str, price: Union[int, float], quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

        # Проверяем цену при инициализации
        if price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")

    def __str__(self) -> str:
        """
        Магический метод для строкового представления объекта.
        :return: Строка в формате "Название продукта, цена руб. Остаток: количество шт."
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> Union[int, float]:
        """
        Магический метод для сложения продуктов.
        Возвращает суммарную стоимость всех товаров на складе.
        :param other: Другой объект класса Product
        :return: Сумма (цена * количество) для обоих продуктов
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @property
    def price(self) -> Union[int, float]:
        """
        Геттер для получения цены товара.
        :return: Цена товара
        """
        return self.__price

    @price.setter
    def price(self, new_price: Union[int, float]) -> None:
        """
        Сеттер для установки цены товара с проверкой.
        :param new_price: Новая цена товара
        """
        if new_price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[List["Product"]] = None) -> "Product":
        """
        Класс-метод для создания нового товара или обновления существующего.
        """
        name = product_data.get("name")
        description = product_data.get("description", "")
        price = product_data.get("price", 0)
        quantity = product_data.get("quantity", 0)

        if not name:
            raise ValueError("Название товара должно быть указано")

        if price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")

        if products_list:
            for existing_product in products_list:
                if existing_product.name.lower() == name.lower():
                    existing_product.quantity += quantity
                    # Используем сеттер для установки цены
                    if price > existing_product.price:
                        existing_product.price = price
                    if description:
                        existing_product.description = description
                    return existing_product

        return cls(name, description, price, quantity)
