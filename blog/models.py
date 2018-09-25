from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import ( FieldPanel,
                                          InlinePanel,
                                          StreamFieldPanel,
                                          )
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.search import index

from home.blocks import BaseStreamBlock

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your models here.
class BlogPage(Page):
    """
    Blog Details Page
    """
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Banner Image'
    )
    banner_intro = models.CharField(max_length=50, blank=True)
    introduction = models.TextField(blank=True,
        help_text='Text to Describe the Page'
        )
    blog_introduction = models.CharField(max_length=500, blank=True)
    blog_title = models.CharField(blank=True,
        max_length=255
        )
    blog_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name='Page Body',
        blank=True
    )
    date_published = models.DateField("Date Article Published",
        blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('banner_image'),
        FieldPanel('banner_intro'),
        FieldPanel('introduction', classname='full'),
        FieldPanel('blog_introduction'),
        FieldPanel('blog_title', classname='full'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('body'),
        FieldPanel('date_published'),
        # InlinePanel('blog_person_relationship',
        #             label='Author',
        #             panels=None,
        #             min_num=1)
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    # def author(self):
    #     authors = [
    #         n.people for n in self.blog_person_relationship
    #     ]
    #     return authors

    # Specifies parent to BlogPage as being BlogIndexPages
    parent_page_types = ['BlogIndex']

class BlogIndex(Page):
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Banner Image'
    )
    banner_intro = models.CharField(max_length=50, blank=True)
    introduction = models.CharField(
        max_length=200,
        help_text='Text to Describe the Page',
        blank=True,
    )
    index_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Image for Blog'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('banner_image'),
        FieldPanel('banner_intro'),
        FieldPanel('introduction'),
        ImageChooserPanel('index_image'),
    ]

    # Speficies that only BlogPage objects can live under this index page
    subpage_types = ['BlogPage']

    def children(self):
        return self.get_children().specific().live()

    def get_context(self,request):
        context = super(BlogIndex, self).get_context(request)
        context['posts'] = BlogPage.objects.descendant_of(
            self).live().order_by('-date_published')

        all_pages = BlogPage.objects.live()
        paginator = Paginator(all_pages,5) # 5 index per page
        page = request.GET.get('page')

        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pages = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pages = paginator.page(paginator.num_pages)

        context['pages'] = pages

        return context
