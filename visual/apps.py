from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError

class VisualConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visual'
    verbose_name = 'Visual'

    def ready(self):
        pass
        # try:
        #     from .models import AdminAppearance
        #     admin_appearance = AdminAppearance.objects.first()
        #     if admin_appearance:
        #         # Basic settings
        #         settings.JAZZMIN_SETTINGS["site_title"] = admin_appearance.site_title
        #         settings.JAZZMIN_SETTINGS["site_header"] = admin_appearance.site_header
        #         settings.JAZZMIN_SETTINGS["site_brand"] = admin_appearance.site_brand
        #         settings.JAZZMIN_SETTINGS["welcome_sign"] = admin_appearance.welcome_sign
        #         settings.JAZZMIN_SETTINGS["copyright"] = admin_appearance.copyright

        #         # Logo settings
        #         if admin_appearance.site_logo:
        #             settings.JAZZMIN_SETTINGS["site_logo"] = admin_appearance.site_logo.url
        #         if admin_appearance.login_logo:
        #             settings.JAZZMIN_SETTINGS["login_logo"] = admin_appearance.login_logo.url

        # except (OperationalError, ProgrammingError):
        #     # This happens when the database is not yet migrated. We can safely ignore it.
        #     pass
