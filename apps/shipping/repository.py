from decimal import Decimal as D
from oscar.core.loading import get_class
from oscar.apps.shipping import methods as core_methods

from apps.shipping.models import OrderAndItemCharges

OriginalRepository = get_class('shipping.repository', 'Repository')


class Repository(OriginalRepository):
    
    methods = [core_methods.FixedPrice(D(2)),]
 
    def get_shipping_methods(self, user, basket, shipping_addr=None,
                             request=None, **kwargs):
        """
        Return a list of all applicable shipping method objects
        for a given basket, address etc.

        We default to returning the ``Method`` models that have been defined
        but this behaviour can easily be overridden by subclassing this class
        and overriding this method.
        """
        for method in OrderAndItemCharges.objects.all():
            method.set_basket(basket)
            if method.charge_incl_tax:
                method.is_tax_known = True
                self.methods.append(method)

        return self.prime_methods(basket, self.methods) 




