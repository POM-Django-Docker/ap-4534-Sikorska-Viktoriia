from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count')
    list_filter = ('id', 'name', 'authors') 
    
    fieldsets = (
        ('Static Data', {
            'fields': ('name', 'description') 
        }),
        ('Dynamic Data', {
            'fields': ('count', 'issue_date') 
        }),
    )