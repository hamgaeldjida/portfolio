from django.contrib import admin
from .models import Contact, Visitor

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'device', 'browser', 'os', 'visited_at')
    search_fields = ('ip_address', 'device', 'browser', 'os')
    list_filter = ('visited_at', 'device', 'browser', 'os')
    readonly_fields = ('ip_address', 'user_agent', 'device', 'browser', 'os', 'visited_at')
