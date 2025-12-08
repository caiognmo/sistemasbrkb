from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm
from .models import OperationalSettings

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    def dispatch(self, *args, **kwargs):
        operational_settings = OperationalSettings.objects.first()

        if operational_settings:
            self.from_email = operational_settings.sender_email
            self.extra_email_context = {'company_name': operational_settings.company_name}
        else:
            self.from_email = 'webmaster@localhost'
            self.extra_email_context = {'company_name': 'Sua Empresa'}

        return super().dispatch(*args, **kwargs)
