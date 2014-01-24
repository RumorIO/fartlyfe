import decimal

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404

from shop.models.productmodel import Product
from shop.models.ordermodel import OrderPayment
from shop.util.order import get_order_from_request
from shop_simplecategories.models import Category
from endless_pagination.views import AjaxListView
 

class ShopFrontView(AjaxListView):
    model = Category
    template_name = 'shop/front.html'
    page_template = 'shop/front_page.html'
    paginate_by = 3
    queryset = Category.objects.filter(products__tangibleitem__active=True).distinct()

    def get_context_data(self, **kwargs):
        context = super(ShopFrontView, self).get_context_data( **kwargs)
        context['cover'] = Product.objects.all()[0]
        return context


class ProductByCategoryView(AjaxListView):
    model = Product
    template_name = 'shop/product_list.html'
    page_template = 'shop/product_list_page.html'

    def get_context_data(self, **kwargs):
        context = super(ProductByCategoryView, self).get_context_data( **kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
        return context

@csrf_exempt
def custom_paypal_success(request):
    context = RequestContext(request, {})
    data = request.POST
    #if 'Completed' in data['payment_status']:
    #    order = get_order_from_request(self.request)
    #    amount = decimal.Decimal(data['mc_gross'])
    #    transaction_id = data['txn_id']
    #    payment_method = 'paypal'
    return HttpResponseRedirect(reverse('thank_you_for_your_order'))
    #else:
    #    return render_to_response('shop/problems.html', context)


