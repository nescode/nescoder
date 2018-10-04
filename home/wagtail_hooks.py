from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from enquiry.models import Enquiry

class EnquiryAdmin(ModelAdmin):
    model = Enquiry
    menu_label = 'Enquiry List'
    menu_icon = 'fa-list'

modeladmin_register(EnquiryAdmin)
