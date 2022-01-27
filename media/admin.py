from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from media.models import Page, Content, Video, Audio, Text

#admin.site.register(Page)
#admin.site.register(Content)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(Text)

class ContentAdmin(admin.TabularInline):
    model = Content
    list_display = ('id', 'title')
    search_fields = ('title__startswith',)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [
        ContentAdmin,
    ]
    list_display = ('id', 'title')#, 'view_contents_link')
    search_fields = ('title__startswith',)
#
#    def view_contents_link(self, obj):
#        from django.utils.html import format_html
#        count = Content.objects.filter(page=obj).count()
#        url = (
#            reverse('admin:media_content_changelist')
#            + '?'
#            + urlencode({'page__id': f"{obj.id}"})
#        )
#        return format_html('<a href="{}">{} Contents</a>', url, count)

#    view_contents_link.short_description = "Contents"

