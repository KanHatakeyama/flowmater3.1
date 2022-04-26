from django.contrib import admin
from .models import Graph, MediaFile, Tag
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from django.conf import settings

# Register your models here.


class GraphAdmin(ImportExportModelAdmin):
    list_display = ('pk', 'title',
                    "edit",
                    "tag_names",
                    'created_at', 'updated_at',
                    )
    save_as = True
    search_fields = ['title', ]
    readonly_fields = ("edit", "p_tags",)
    ordering = ["-updated_at", "pk"]

    list_filter = ["p_tags__name",
                   "created_at", "updated_at"]

    def edit(self, obj):
        #html = f'<a href={settings.REACT_URL}/?gid={obj.pk} target="_blank">edit</a>'
        html = f'<a href=/?gid={obj.pk} target="_blank">edit</a>'
        return mark_safe(html)

    def tag_names(self, obj):
        return " : ".join([p.name for p in obj.p_tags.all()])


class MedieFileAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    "filename",
                    "view",
                    'created_at', 'updated_at',
                    )

    def view(self, obj):
        html = f'<a href={settings.REACT_URL}/uploaded/{obj.pk} target="_blank">view</a>'
        html = f'<a href=/uploaded/{obj.filename()} target="_blank">view</a>'
        # return html
        return mark_safe(html)

    def name(self, obj):
        return obj.filename()


admin.site.register(Graph, GraphAdmin)
admin.site.register(MediaFile, MedieFileAdmin)
admin.site.register(Tag)
