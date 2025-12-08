from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import SiteAppearance, AdminAppearance

@admin.register(SiteAppearance)
class SiteAppearanceAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {'fields': ('site_name', 'site_logo', 'favicon')}),
        ('Colors', {'fields': ('primary_color', 'secondary_color', 'background_color', 'text_color', 'heading_color', 'link_color', 'link_hover_color')}),
        ('Typography', {'fields': ('font_family_base', 'font_family_headings', 'font_size_base', 'font_size_h1', 'font_size_h2', 'font_size_h3')}),
        ('Header', {'fields': ('header_background_color', 'header_text_color')}),
        ('Footer', {'fields': ('footer_background_color', 'footer_text_color', 'footer_support_title', 'footer_whatsapp_link', 'footer_whatsapp_text', 'footer_facebook_link', 'footer_instagram_link', 'footer_linkedin_link', 'footer_youtube_link')}),
        ('Buttons', {'fields': ('button_primary_bg_color', 'button_primary_text_color', 'button_secondary_bg_color', 'button_secondary_text_color')}),
        ('Custom CSS', {'fields': ('custom_css',), 'classes': ('collapse',)}),
    )

    def changelist_view(self, request, extra_context=None):
        obj, created = self.model.objects.get_or_create(pk=1)
        return redirect(reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=(obj.pk,)))

@admin.register(AdminAppearance)
class AdminAppearanceAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        obj, created = self.model.objects.get_or_create(pk=1)
        return redirect(reverse(f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change', args=(obj.pk,)))
