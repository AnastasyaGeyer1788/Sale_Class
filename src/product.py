from typing import Union


class Product:
    """Конструктор класса Product
    :param name: Название продукта
    :param description: Описание продукта
    :param price: Цена продукта
    :param quantity: Количество доступных единиц продукта
    """

    name: str
    description: str
    price: Union[int, float]
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
