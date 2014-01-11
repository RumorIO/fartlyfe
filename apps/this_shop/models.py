from django.db import models

from shop.models import Product
from tinymce.models import HTMLField
from photologue.models import Photo

class TangibleItem(Product):
    
    description = HTMLField()
    photo = models.ForeignKey(Photo)

    class Meta:
        ordering = ['name',]


# Create your models here.
