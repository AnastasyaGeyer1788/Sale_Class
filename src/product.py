# src/product.py
from abc import ABC, abstractmethod
from typing import Union, List, Optional, TypeVar, Type

# Создаем TypeVar для гибких аннотаций типов
T = TypeVar("T", bound="BaseProduct")


class CreationLoggerMixin:
    """Миксин для логирования создания объектов."""

    def __init__(self, *args, **kwargs):
        """Инициализация миксина.

        Сохраняет переданные аргументы для последующего использования
         и выводит информацию о создании объекта.

        Args:
        *args: Позиционные аргументы
        **kwargs: Именованные аргументы
        """
        # Сохраняем аргументы для последующего использования
        self._init_args = args
        self._init_kwargs = kwargs

        # Формируем информацию о параметрах
        params_info = []

        # Добавляем позиционные аргументы
        if args:
            params_info.append(f"args={args}")

        # Добавляем именованные аргументы
        if kwargs:
            params_info.append(f"kwargs={kwargs}")

        # Формируем полное сообщение
        params_str = ", ".join(params_info) if params_info else "без параметров"

        # Выводим информацию о создании объекта
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: {params_str}")

        # Вызываем __init__ следующего класса в MRO
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        """
        Магический метод для официального строкового представления объекта.

        :return: Строка в формате для воссоздания объекта
        """
        # Формируем список аргументов для repr
        args_repr = []

        # Добавляем позиционные аргументы
        for arg in self._init_args:
            if isinstance(arg, str):
                args_repr.append(f"'{arg}'")
            else:
                args_repr.append(repr(arg))

        # Добавляем именованные аргументы
        for key, value in self._init_kwargs.items():
            if isinstance(value, str):
                args_repr.append(f"{key}='{value}'")
            else:
                args_repr.append(f"{key}={repr(value)}")

        return f"{self.__class__.__name__}({', '.join(args_repr)})"


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    def __init__(self, name: str, description: str, price: Union[int, float], quantity: int):
        """Инициализирует продукт с именем и ценой."""
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены в базовом классе
        self.quantity = quantity

        if price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод для строкового представления объекта."""
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> Union[int, float]:
        """Абстрактный метод для сложения продуктов."""
        pass

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
    @abstractmethod
    def new_product(cls: Type[T], product_data: dict, products_list: Optional[List[T]] = None) -> T:
        """Абстрактный класс-метод для создания нового товара."""
        pass


class Product(CreationLoggerMixin, BaseProduct):
    """Класс Product представляет товар в магазине."""

    def __init__(self, name: str, description: str, price: Union[int, float], quantity: int):
        """Вызываем инициализацию миксина и базового класса"""
        super().__init__(name=name, description=description, price=price, quantity=quantity)

    def __str__(self) -> str:
        """
        Магический метод для строкового представления объекта.

        :return: Строка в формате "Название продукта, цена руб. Остаток: количество шт."
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> Union[int, float]:
        """
        Магический метод для сложения продуктов.

        :param other: Другой объект класса Product
        :return: Сумма (цена * количество) для обоих продуктов
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        # Проверяем, что объекты одного типа
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных категорий")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[List["Product"]] = None) -> "Product":
        """Класс-метод для создания нового товара или обновления существующего."""
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


class Smartphone(Product):
    """Класс для представления смартфонов, наследник Product."""

    def __init__(
        self,
            name: str,
            description: str,
            price: Union[int, float],
            quantity: int,
            efficiency: str,
            model: str,
            memory: int,
            color: str,
    ) -> object:
        """:rtype: object"""
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

        # Вызываем __init__ родительского класса
        super().__init__(name=name, description=description, price=price, quantity=quantity)

    def __str__(self) -> str:
        """Переопределение строкового представления для смартфона."""
        base_str = super().__str__()
        return (
            f"{base_str}\nПроизводительность: {self.efficiency}, Модель: {self.model},\n"
            f" Память: {self.memory}GB, Цвет: {self.color}"
        )

    def __repr__(self) -> str:
        """Переопределение repr для смартфона."""
        base_repr = super().__repr__()[:-1]  # Убираем закрывающую скобку
        return (
            f"{base_repr}, efficiency='{self.efficiency}', model='{self.model}', "
            f"memory={self.memory}, color='{self.color}')"
        )

    def __add__(self, other: "Smartphone") -> Union[int, float]:
        """Переопределение метода сложения для смартфонов."""
        if not isinstance(other, Smartphone):
            raise TypeError("Можно складывать только объекты класса Smartphone")

        return super().__add__(other)


class LawnGrass(Product):
    """Класс для представления газонной травы, наследник Product."""

    def __init__(
        self,
        name: str,
        description: str,
        price: Union[int, float],
        quantity: int,
        country: str,
        germination_period: int,
        color: str,
    ):
        """Инициализирует экземпляр газонной травы.

        Args:
            name (str): Название газонной травы
            description (str): Описание газонной травы
            price (Union[int, float]): Цена газонной травы
            quantity (int): Количество доступного товара
            country (str): Страна-производитель
            germination_period (int): Срок прорастания в днях
            color (str): Цвет газонной травы
        """
        self.country = country
        self.germination_period = germination_period
        self.color = color

        # Вызываем __init__ родительского класса
        super().__init__(name=name, description=description, price=price, quantity=quantity)

    def __str__(self) -> str:
        """Переопределение строкового представления для газонной травы."""
        base_str = super().__str__()
        return (
            f"{base_str}\nСтрана: {self.country}, Срок прорастания: {self.germination_period} дней, Цвет: {self.color}"
        )

    def __repr__(self) -> str:
        """Переопределение repr для газонной травы."""
        base_repr = super().__repr__()[:-1]  # Убираем закрывающую скобку
        return (
            f"{base_repr}, country='{self.country}', germination_period={self.germination_period}, "
            f"color='{self.color}')"
        )

    def __add__(self, other: "LawnGrass") -> Union[int, float]:
        """Переопределение метода сложения для газонной травы."""
        if not isinstance(other, LawnGrass):
            raise TypeError("Можно складывать только объекты класса LawnGrass")

        return super().__add__(other)
