from django.contrib import admin
from main.models import UserProfile, MetaData

class ProfAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'role')

admin.site.register(UserProfile, ProfAdmin)

class MDAdmin(admin.ModelAdmin):
    list_display = ('xform', 'data_type', 'data_value', 'data_file_type')

admin.site.register(MetaData, MDAdmin)
