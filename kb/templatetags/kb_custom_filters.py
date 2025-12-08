from django import template
from kb.models import Artigo, Categoria

register = template.Library()

@register.filter
def has_new_articles_in_subcategory(artigos):
    return artigos.filter(show_new_in_subcategory_list=True).exists()

@register.filter
def has_new_articles_in_category(category_obj):
    # Obter todos os IDs de categorias descendentes, incluindo a selecionada
    descendant_categories = category_obj.get_descendants(include_self=True)
    descendant_category_ids = [cat.id for cat in descendant_categories]
    
    # Verificar se existe algum artigo novo em qualquer uma dessas categorias
    return Artigo.objects.filter(
        categoria__id__in=descendant_category_ids,
        show_new_in_category_list=True
    ).exists()

@register.filter(name='strip_prefix')
def strip_prefix(value):
    if value and isinstance(value, str) and '.' in value:
        return value.split('.', 1)[-1].strip()
    return value