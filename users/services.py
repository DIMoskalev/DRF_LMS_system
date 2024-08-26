import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(current_product):
    """ Создает продукт в страйпе """
    product = stripe.Product.create(name=current_product)
    return product.id


def create_stripe_price(product, product_id):
    """ Создает цену в страйпе """

    price = stripe.Price.create(
        product=product_id,
        currency="rub",
        unit_amount=int(product.price * 100),
    )
    return price.id


def create_stripe_session(price_id):
    """ Создает сессию на оплату в страйпе """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
