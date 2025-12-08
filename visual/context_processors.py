from .models import SiteAppearance

def site_appearance(request):
    try:
        appearance = SiteAppearance.objects.first()
    except SiteAppearance.DoesNotExist:
        appearance = None
    return {'site_appearance': appearance}