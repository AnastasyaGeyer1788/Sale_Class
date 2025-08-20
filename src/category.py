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
    products: list

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.products = products if products else []

        Category.category_count += 1
        Category.product_count += len(products) if products else 0
