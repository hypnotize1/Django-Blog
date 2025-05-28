import profile

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from accounts.models import Profile


# Register your models here.
@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'bio', 'profile_pic_preview')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('profile_pic_preview',)

    def profile_pic_preview(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%; />', obj.profile_pic.url)
        else:
            return "-"
    profile_pic_preview.short_description = 'Profile picture'