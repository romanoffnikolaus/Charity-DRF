from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'user_type', 'verified_account', 'phone_number') 
    search_fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'user_type', 'verified_account']
    fields = [
        'last_login',
        'groups',
        ('username', 'email', 'user_photo'),
        ('first_name', 'last_name'),
        'user_type',
        'phone_number',
        ('is_active', 'is_staff', 'verified_account', 'is_superuser'),
        ('facebook_url', 'twitter_url', 'telegram_url' ),
        ('region', 'category', 'adress', 'requisites')
    ]