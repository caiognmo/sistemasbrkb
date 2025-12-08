from django import template
from kb.models import Categoria, Artigo
from django.utils.html import format_html, strip_tags
from django.db.models import Case, When, Value, IntegerField
from kb.ordering import TOP_LEVEL_ORDER, CATEGORY_ORDER

register = template.Library()

def get_ordered_children(categoria):
    order_list = CATEGORY_ORDER.get(categoria.nome, [])
    
    # Mapeia nomes de artigos e categorias para sua posição na lista de ordem
    ordering_case = Case(*[When(nome=name, then=Value(i)) for i, name in enumerate(order_list)],
                         default=Value(len(order_list)), output_field=IntegerField())
    
    children_qs = categoria.children.all().annotate(custom_order=ordering_case).order_by('custom_order', 'nome')
    for child in children_qs:
        child.type = 'category'
        child.ordered_children = get_ordered_children(child)

    # Artigos também precisam ser ordenados se estiverem na lista
    article_ordering_case = Case(*[When(titulo=name, then=Value(i)) for i, name in enumerate(order_list)],
                                 default=Value(len(order_list)), output_field=IntegerField())

    articles_qs = categoria.artigos.all().annotate(custom_order=article_ordering_case).order_by('custom_order', 'titulo')
    for article in articles_qs:
        article.type = 'artigo'

    # A ordenação final deve considerar a ordem original do banco de dados como fallback
    # No entanto, a lógica aqui já os separa, então combinamos e re-ordenamos
    combined_list = sorted(list(children_qs) + list(articles_qs), key=lambda x: x.custom_order)
    
    return combined_list

@register.inclusion_tag('kb/includes/category_sidebar.html')
def category_sidebar():
    """
    Renderiza a lista de categorias para a barra lateral, com ordenação customizada.
    """
    # Define a ordem para as categorias de nível superior
    ordering = Case(*[When(nome=name, then=Value(i)) for i, name in enumerate(TOP_LEVEL_ORDER)],
                    default=Value(len(TOP_LEVEL_ORDER)), output_field=IntegerField())
    
    categorias_principais = Categoria.objects.filter(parent__isnull=True).annotate(
        custom_order=ordering
    ).order_by('custom_order', 'nome')

    # Para cada categoria principal, busca e ordena seus descendentes
    for cat in categorias_principais:
        cat.ordered_children = get_ordered_children(cat)
        cat.type = 'category'

    return {'categories': categorias_principais}

@register.simple_tag
def breadcrumbs(category):
    """
    Renders breadcrumbs for a given category.
    """
    if not category:
        return ""

    crumbs = []
    current = category
    while current:
        crumbs.append(f'<a href="{current.get_absolute_url()}">{strip_tags(current.nome)}</a>')
        current = current.parent
    
    crumbs.reverse()
    return format_html(" &gt; ".join(crumbs))
