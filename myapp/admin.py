from django.contrib import admin

from myapp.models import User, LearningEnglish


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'fullname', 'phone', 'level')

@admin.register(LearningEnglish)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['level']
