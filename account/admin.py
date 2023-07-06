from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OtpCode, Professor, Profile, Editor, Student, Message
from .forms import UserCreationForm, UserChangeForm

# Register your models here.


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Main', {'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin',
                                    'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email',
         'full_name', 'password1', 'password2')}),
    )

    search_fields = ('email', 'full_name')
    ordering = ('full_name',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'location',)
    raw_id_fields = ('user',)
    search_fields = ('name', 'location', 'university',)


class EditorAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


class ProfessorAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


class StudentAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('sender', 'recipient',)
    list_display = ('sender', 'recipient', 'is_read')
    list_filter = ('is_read',)


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Editor, EditorAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Message, MessageAdmin)
