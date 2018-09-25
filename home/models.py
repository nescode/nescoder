from django.db import models

from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from modelcluster.fields import ParentalKey

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from wagtail.contrib.forms.views import SubmissionsListView

from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel,FieldRowPanel,)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.snippets.models import register_snippet
from wagtail.search import index

from .blocks import BaseStreamBlock
from blog.models import BlogPage

class HomePage(Page):
    full_name = models.CharField(max_length=50, blank=True)
    intro = models.CharField(max_length=300, blank=True, help_text='Small intro about yourself')
    work_intro = models.CharField(max_length=300, blank=True, help_text='Some words about your work profile')

    left_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Left Column Logo'
    )
    left_heading = models.CharField(max_length=20, blank=True, help_text = 'Left Column Heading')
    left_text = models.CharField(max_length=50, blank=True, help_text = 'Left Column Text')

    center_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Center Column Logo'
    )
    center_heading = models.CharField(max_length=20, blank=True, help_text='Center Column Heading')
    center_text = models.CharField(max_length=50, blank=True, help_text='Center Column Text')

    right_logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Right Column Logo'
    )
    right_heading = models.CharField(max_length=20, blank=True, help_text='Right Column Heading')
    right_text = models.CharField(max_length=50, blank=True, help_text='Right Column Text')

    content_panels = Page.content_panels + [
        FieldPanel('full_name'),
        FieldPanel('intro'),
        FieldPanel('work_intro'),

        ImageChooserPanel('left_logo'),
        FieldPanel('left_heading'),
        FieldPanel('left_text'),

        ImageChooserPanel('center_logo'),
        FieldPanel('center_heading'),
        FieldPanel('center_text'),

        ImageChooserPanel('right_logo'),
        FieldPanel('right_heading'),
        FieldPanel('right_text'),
    ]

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        context['posts'] = BlogPage.objects.live().order_by('-date_published')[:2]
        return context
