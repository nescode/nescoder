from django.db import models

from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel

# Create your models here.
@register_snippet
class Enquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    message = models.TextField()

    panels = [
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('phone'),
        FieldPanel('message')
    ]

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Enquiries'
