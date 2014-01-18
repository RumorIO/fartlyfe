from django.db import models

from shop.models import Product
from tinymce.models import HTMLField
from photologue.models import Gallery, Photo

class TangibleItem(Product):
    
    title = models.CharField(max_length=255, editable=False)
    description = HTMLField()
    cover = models.ForeignKey(Photo)
    gallery = models.ForeignKey(Gallery, blank=True, null=True, default=None)

    class Meta:
        ordering = ['name',]

    def save(self):
        self.title = self.name
        super(TangibleItem, self).save()


# Create your models here.
