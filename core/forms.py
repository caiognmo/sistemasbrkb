from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import get_connection
from .models import OperationalSettings

class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        settings = OperationalSettings.objects.first()
        
        if settings and settings.email_host:
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=settings.email_host,
                port=settings.email_port,
                username=settings.email_host_user,
                password=settings.email_host_password,
                use_tls=settings.email_use_tls,
                use_ssl=settings.email_use_ssl
            )
        else:
            # Fallback para o backend padr\u00e3o (console)
            connection = get_connection()

        # O assunto \u00e9 renderizado de forma diferente, ent\u00e3o o adicionamos ao contexto
        context['subject'] = context['email_template_name'].render(context)
        
        super().send_mail(
            subject_template_name, 
            email_template_name, 
            context, 
            from_email, 
            to_email, 
            html_email_template_name=html_email_template_name,
            connection=connection # Passa a conex\u00e3o customizada
        )
