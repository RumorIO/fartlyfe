from django.contrib import admin
from shop_simplecategories.admin import ProductWithCategoryForm

from apps.this_shop.models import TangibleItem

class TangibleItemForm(ProductWithCategoryForm):
    class Meta(object):
        model = TangibleItem

class TangibleItemAdmin(admin.ModelAdmin):
    form = TangibleItemForm

admin.site.register(TangibleItem, TangibleItemAdmin)
