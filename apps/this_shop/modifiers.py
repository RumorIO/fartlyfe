import decimal
 
from django.conf import settings
  
from shop.cart.cart_modifiers_base import BaseCartModifier


class FixedShippingCosts(BaseCartModifier):
    """
    This will add a fixed amount of money for shipping costs.
    """
    def add_extra_cart_price_field(self, cart):
        cart.extra_price_fields.append(
            ('Shipping costs', decimal.Decimal(
                settings.SHOP_SHIPPING_FLAT_RATE)))
        return cart

