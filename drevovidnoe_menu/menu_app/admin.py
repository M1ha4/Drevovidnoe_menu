from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0
    fields = ('title', 'parent', 'order', 'url', 'named_url', 'named_url_kwargs')
    show_change_link = True


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'order', 'named_url', 'url')
    list_filter = ('menu',)
    ordering = ('menu', 'order', 'id')
    search_fields = ('title', 'url', 'named_url')
