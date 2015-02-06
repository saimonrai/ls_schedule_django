from django.contrib import admin

from .models import Group, Substation, Area


class AreaInline(admin.TabularInline):
    model = Area


class SubstationAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_nep', 'in_ktm')
    list_filter = ('in_ktm',)
    inlines = [AreaInline,]


class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_nep', 'group', 'substation', 'in_ktm')


class GroupAdmin(admin.ModelAdmin):
    inlines = [AreaInline]


admin.site.register(Substation, SubstationAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Group, GroupAdmin)
