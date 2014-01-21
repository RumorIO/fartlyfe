from django.conf.urls import patterns, include, url

from apps.this_shop.views import ShopFrontView, ProductByCategoryView, custom_paypal_success

urlpatterns = patterns('',

    url(r'^$', ShopFrontView.as_view(), name='shop_main'),
    url(r'^category/(?P<slug>[\d\w-]+)/$', ProductByCategoryView.as_view(), name='category_detail'),
    url(r'^cart/', include('shop_simplevariations.urls')),
    url(r'', include('shop.urls')),
    url(r'^payment/success/$',custom_paypal_success ,name='paypal_success'),
    
    )

