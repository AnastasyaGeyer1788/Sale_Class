class Category:
    # Атрибуты класса
    category_count = 0
    product_count = 0
    """
    Конструктор класса Category.
    :param name: Название категории
    :param description: Описание категории
    :param products: Список товаров в категории
    """
    name: str
    description: str
    __products: list  # Приватный атрибут

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = products if products else []

        Category.category_count += 1
        Category.product_count += len(products) if products else 0

    def add_product(self, product):
        """
        Добавляет товар в категорию.
        :param product: Объект класса Product для добавления
        """
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """
        Геттер для вывода списка товаров в формате:
        Название продукта, цена руб. Остаток: количество шт.
        """
        products_list = []
        for product in self.__products:
            products_list.append(
                f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
            )
        return products_list
