from bs4 import BeautifulSoup
import re

from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from .models import Categoria, Artigo
from django.db.models import Q, Case, When, Value, IntegerField
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import FeedbackForm
from .ordering import TOP_LEVEL_ORDER, CATEGORY_ORDER

class HomePageView(ListView):
    """
    View para a página inicial, mostrando as categorias principais com ordem customizada.
    """
    model = Categoria
    template_name = 'kb/home.html'
    context_object_name = 'categorias_principais'

    def get_queryset(self):
        ordering = Case(*[When(nome=name, then=Value(i)) for i, name in enumerate(TOP_LEVEL_ORDER)],
                        default=Value(len(TOP_LEVEL_ORDER)), output_field=IntegerField())
        
        return Categoria.objects.filter(parent__isnull=True).annotate(
            custom_order=ordering
        ).order_by('custom_order', 'nome')

class ArtigoListView(ListView):
    """
    View para listar os artigos de uma categoria específica com ordem customizada.
    """
    model = Artigo
    context_object_name = 'artigos'

    def get_template_names(self):
        return ['kb/subcategory_list.html']

    def dispatch(self, request, *args, **kwargs):
        try:
            Categoria.objects.get(id=self.kwargs['categoria_id'])
        except Categoria.DoesNotExist:
            return redirect('kb:artigo-detail', pk=self.kwargs['categoria_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categoria = Categoria.objects.get(id=self.kwargs['categoria_id'])
        context['categoria'] = categoria

        order_list = CATEGORY_ORDER.get(categoria.nome, [])

        # Get all descendant categories
        descendant_categories = categoria.get_descendants(include_self=True)
        descendant_category_ids = [cat.id for cat in descendant_categories]

        # Ordenação para subcategorias
        subcat_ordering = Case(*[When(nome=name, then=Value(i)) for i, name in enumerate(order_list)],
                               default=Value(len(order_list)), output_field=IntegerField())
        subcategorias_qs = categoria.children.all().annotate(custom_order=subcat_ordering).order_by('custom_order', 'nome')
        for sub in subcategorias_qs:
            sub.type = 'category'

        # Ordenação para artigos
        art_ordering = Case(*[When(titulo=name, then=Value(i)) for i, name in enumerate(order_list)],
                            default=Value(len(order_list)), output_field=IntegerField())
        
        # Get articles from current category and all descendants
        artigos_qs = Artigo.objects.filter(categoria_id__in=descendant_category_ids).annotate(custom_order=art_ordering).order_by('custom_order', 'titulo')
        for art in artigos_qs:
            art.type = 'artigo'

        # Combina e ordena a lista final pela ordem customizada
        combined_list = sorted(list(subcategorias_qs) + list(artigos_qs), key=lambda x: x.custom_order)

        # Verifica se há artigos na lista combinada
        has_articles = any(item.type == 'artigo' for item in combined_list)

        context['subcategorias'] = combined_list
        context['has_articles'] = has_articles
        return context

class ArtigoSearchView(ListView):
    """
    View para buscar artigos.
    """
    model = Artigo
    template_name = 'kb/artigo_list.html'
    context_object_name = 'artigos'

    def get_queryset(self):
        """Filtra os artigos pelo termo de busca."""
        query = self.request.GET.get('q')
        if query:
            return Artigo.objects.filter(
                Q(titulo__icontains=query) | Q(conteudo__icontains=query)
            )
        return Artigo.objects.none()

    def get_context_data(self, **kwargs):
        """Adiciona o termo de busca ao contexto."""
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

class ArtigoDetailView(DetailView):
    """
    View para exibir os detalhes de um artigo.
    """
    model = Artigo
    template_name = 'kb/artigo_detail.html'
    context_object_name = 'artigo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artigo = context['artigo']
        
        # Processar o conteúdo do artigo para substituir iframes do YouTube por thumbnails e links
        soup = BeautifulSoup(artigo.conteudo, 'html.parser')
        youtube_iframes = soup.find_all('iframe', src=re.compile(r'(youtube\.com|youtu\.be)'))

        for iframe in youtube_iframes:
            original_src = iframe['src']
            video_id_match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', original_src)
            
            if video_id_match:
                video_id = video_id_match.group(1)
                new_src = f"https://www.youtube-nocookie.com/embed/{video_id}?enablejsapi=1&origin={self.request.build_absolute_uri('/')}&rel=0"
                
                video_id = video_id_match.group(1)
                # Usar youtube-nocookie.com para tentar contornar bloqueios
                new_src = f"https://www.youtube-nocookie.com/embed/{video_id}?enablejsapi=1&origin={self.request.build_absolute_uri('/')}&rel=0"
                
                # Limpar todos os atributos existentes
                iframe.attrs = {}
                
                # Adicionar apenas os atributos essenciais
                iframe['src'] = new_src
                iframe['frameborder'] = '0'
                iframe['allow'] = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
                iframe['allowfullscreen'] = ''
                iframe['width'] = '560' # Definir um padrão, ou usar o original se existir
                iframe['height'] = '315' # Definir um padrão, ou usar o original se existir
            else:
                # Se não encontrar um video_id válido, o iframe original permanece inalterado
                print(f"Aviso: Não foi possível extrair o ID do vídeo do YouTube para o iframe com src: {original_src}")
        
        artigo.conteudo = str(soup)
        context['artigo'] = artigo
        return context

@require_POST
def feedback_view(request):
    form = FeedbackForm(request.POST)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.artigo = Artigo.objects.get(id=request.POST.get('artigo'))
        feedback.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})