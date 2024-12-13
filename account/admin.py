from django.contrib import admin
from account.models import User, UserProfile

# Customize User admin panel
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active', 'is_staff', 'is_admin')
    list_filter = ('role', 'is_active', 'is_staff', 'is_admin')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

# Customize UserProfile admin panel
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'address', 'created_at', 'modified_at')
    search_fields = ('user__email', 'user__username', 'city')
    ordering = ('user',)

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
