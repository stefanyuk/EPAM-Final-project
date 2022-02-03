from rest_app.models import Category


def get_products_by_category(category_name):
    """
    Select all records for the products that are under provided category

    :param category_name: name of the searched category
    """
    category = Category.query.filter_by(name=category_name).first()

    return category.products
