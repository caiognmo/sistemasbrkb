from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import gettext_lazy as _

class SiteAppearance(models.Model):
    """
    Model to control the visual appearance of the main site.
    """
    # General
    site_name = models.CharField(_("Site Name"), max_length=255, default='SistemasBr KB')
    site_logo = models.ImageField(_("Site Logo"), upload_to='visual/', blank=True, null=True)
    favicon = models.ImageField(_("Favicon"), upload_to='visual/', blank=True, null=True)

    # Colors
    primary_color = ColorField(_("Primary Color"), default='#1C85E8')
    secondary_color = ColorField(_("Secondary Color"), default='#FFFFFF')
    background_color = ColorField(_("Background Color"), default='#F4F4F4')
    text_color = ColorField(_("Body Text Color"), default='#333333')
    heading_color = ColorField(_("Heading Color"), default='#000000')
    link_color = ColorField(_("Link Color"), default='#1C85E8')
    link_hover_color = ColorField(_("Link Hover Color"), default='#1565C0')

    # Typography
    font_family_base = models.CharField(_("Base Font Family"), max_length=255, default='Helvetica Neue, Helvetica, Arial, sans-serif')
    font_family_headings = models.CharField(_("Headings Font Family"), max_length=255, default='Helvetica Neue, Helvetica, Arial, sans-serif')
    font_size_base = models.CharField(_("Base Font Size"), max_length=10, default='16px')
    font_size_h1 = models.CharField(_("H1 Font Size"), max_length=10, default='2.5rem')
    font_size_h2 = models.CharField(_("H2 Font Size"), max_length=10, default='2rem')
    font_size_h3 = models.CharField(_("H3 Font Size"), max_length=10, default='1.75rem')

    # Header
    header_background_color = ColorField(_("Header Background Color"), default='#FFFFFF')
    header_text_color = ColorField(_("Header Text Color"), default='#333333')

    # Footer
    footer_background_color = ColorField(_("Footer Background Color"), default='#343a40')
    footer_text_color = ColorField(_("Footer Text Color"), default='#FFFFFF')

    # Buttons
    button_primary_bg_color = ColorField(_("Primary Button BG Color"), default='#1C85E8')
    button_primary_text_color = ColorField(_("Primary Button Text Color"), default='#FFFFFF')
    button_secondary_bg_color = ColorField(_("Secondary Button BG Color"), default='#6c757d')
    button_secondary_text_color = ColorField(_("Secondary Button Text Color"), default='#FFFFFF')
    # Custom CSS
    custom_css = models.TextField(_("Custom CSS"), blank=True, null=True)

    # Footer Content
    footer_support_title = models.CharField(_("Footer Support Title"), max_length=100, blank=True, default="Suporte Técnico")
    footer_whatsapp_link = models.URLField(_("Footer WhatsApp Link"), blank=True, default="https://wa.me/1736223222")
    footer_whatsapp_text = models.CharField(_("Footer WhatsApp Text"), max_length=50, blank=True, default="17 3622-3222")
    footer_facebook_link = models.URLField(_("Footer Facebook Link"), blank=True, default="https://www.facebook.com/sistemasbr.net/?locale=pt_BR")
    footer_instagram_link = models.URLField(_("Footer Instagram Link"), blank=True, default="https://www.instagram.com/sistemasBR/")
    footer_linkedin_link = models.URLField(_("Footer LinkedIn Link"), blank=True, default="https://br.linkedin.com/company/sistemasbr")
    footer_youtube_link = models.URLField(_("Footer YouTube Link"), blank=True, default="https://www.youtube.com/user/sistemasbr")

    class Meta:
        verbose_name = _('Site Appearance')
        verbose_name_plural = _('Site Appearance')

    def __str__(self):
        return self.site_name

class AdminAppearance(models.Model):
    """
    Model to control the visual appearance of the Django admin panel (Jazzmin).
    """
    # General
    site_title = models.CharField(_("Site Title"), max_length=255, default='Admin da KB SistemasBr')
    site_header = models.CharField(_("Site Header"), max_length=255, default='KB SistemasBr')
    site_brand = models.CharField(_("Site Brand"), max_length=255, default='KB SistemasBr')
    site_logo = models.ImageField(_("Site Logo"), upload_to='visual/admin/', blank=True, null=True, help_text=_("Must be 40px in height"))
    login_logo = models.ImageField(_("Login Logo"), upload_to='visual/admin/', blank=True, null=True)
    welcome_sign = models.CharField(_("Welcome Sign"), max_length=255, default='Bem-vindo ao painel de administração')
    copyright = models.CharField(_("Copyright"), max_length=255, default='SistemasBr')

    # Colors
    primary_color = ColorField(_("Primary Color"), default='#007bff')
    secondary_color = ColorField(_("Secondary Color"), default='#6c757d')
    accent_color = ColorField(_("Accent Color"), default='#17a2b8')
    sidebar_color = ColorField(_("Sidebar Color"), default='#343a40')
    sidebar_text_color = ColorField(_("Sidebar Text Color"), default='#adb5bd')
    sidebar_link_color = ColorField(_("Sidebar Link Color"), default='#ced4da')
    # Custom CSS
    custom_css = models.TextField(_("Custom CSS"), blank=True, null=True)

    # Contact
    admin_email = models.EmailField(_("Admin Contact Email"), max_length=255, default='admin@sistemasbr.com', help_text=_("Email for users to contact in case of issues."))

    class Meta:
        verbose_name = _('Admin Panel Appearance')
        verbose_name_plural = _('Admin Panel Appearance')

    def __str__(self):
        return self.site_title