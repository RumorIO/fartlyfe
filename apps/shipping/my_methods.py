from django.utils.translation import ugettext_lazy as _

from oscar.apps.shipping.methods import (
    Free, 
    NoShippingRequired, 
    FixedPrice, 
    OfferDiscount,)


class TwoPer(FixedPrice):
    
    code = 'two-dollars-per'
    name = _('$2 Per Item')

    def __init__(self, charge_excl_tax, charge_incl_tax=None):
        self.charge_excl_tax = charge_excl_tax
        if charge_incl_tax is not None:
            self.charge_incl_tax = charge_incl_tax
            self.is_tax_known = True 

    def basket_charge_incl_tax(self):
        if self.charge_incl_tax:
            return self.charg_incl_tax
        return self.charge_excl_tax()

    def basket_charge_excl_tax(self):
        return self.charge_excl_tax



