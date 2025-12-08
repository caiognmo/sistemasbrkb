from django.contrib import admin

# Register your models here.

from django import forms
from .models import OperationalSettings

class OperationalSettingsForm(forms.ModelForm):
    class Meta:
        model = OperationalSettings
        fields = '__all__'
        widgets = {
            'email_host_password': forms.PasswordInput(render_value=False),
        }

@admin.register(OperationalSettings)
class OperationalSettingsAdmin(admin.ModelAdmin):
    form = OperationalSettingsForm
    fieldsets = (
        ('Branding e Identidade', {
            'fields': ('company_name', 'company_logo', 'favicon', 'footer_text')
        }),
        ('Contato e Links Legais', {
            'fields': ('contact_email', 'privacy_policy_url', 'terms_of_service_url')
        }),
        ('Funcionalidades', {
            'fields': ('enable_public_registration', 'enable_feedback_system')
        }),
        ('Integrações', {
            'fields': ('google_analytics_id',)
        }),
        ('Configurações de E-mail', {
            'description': "Configurações para o envio de e-mails transacionais do sistema.",
            'fields': ('sender_email', 'email_host', 'email_port', 'email_host_user', 'email_host_password', 'email_use_tls', 'email_use_ssl')
        }),
    )

    def has_add_permission(self, request):
        return not OperationalSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False