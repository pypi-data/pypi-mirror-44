from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from telebaka_faq.models import FAQSection


@admin.register(FAQSection)
class FAQSectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = 'command', 'title', 'bot', 'hidden',
    list_filter = 'bot',

    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return FAQSection.objects.all()
        return FAQSection.objects.filter(bot__owners=user)

    def get_form(self, request, obj=None, **kwargs):
        form = super(FAQSectionAdmin, self).get_form(request, obj=None, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['bot'].queryset = form.base_fields['bot'].queryset.filter(owners=request.user)
        return form
