from django.contrib import admin

from events.models import Event


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('user', 'name', 'created', 'updated')
    ordering = ('name', 'created')
    search_fields = ('name', 'user')
    date_hierarchy = 'created'
