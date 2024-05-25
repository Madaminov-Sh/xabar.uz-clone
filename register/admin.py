from django.contrib import admin
from register.models import Profile, User, SocialNetwork, VerificationCode
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'full_name', 'email', 'date_of_brith')


admin.site.register(Profile, ProfileAdmin)


class CustomUserAdmin(UserAdmin):
    list_filter = ()
    list_display = ('email', 'id', 'name', 'is_admin', 'is_superuser')
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        # (("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    filter_horizontal = ()
    ordering = ()


admin.site.register(User, CustomUserAdmin)


class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'url')


admin.site.register(SocialNetwork, SocialNetworkAdmin)
admin.site.register(VerificationCode)