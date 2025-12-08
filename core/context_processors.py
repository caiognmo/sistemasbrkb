from kb.models import Categoria, Artigo, Feedback
from django.db.models import Count
from django.db.models.functions import TruncDay

def categories_context(request):
    categories = Categoria.objects.prefetch_related('children').all()
    
    # Get IDs of categories directly containing new articles
    new_article_category_ids = set(Artigo.objects.filter(show_new_in_category_list=True).values_list('categoria_id', flat=True))

    category_map = {cat.id: cat for cat in categories}

    # Annotate all categories with a default 'has_new' of False
    for cat in categories:
        cat.has_new_articles = False

    # Propagate the 'new' status up the hierarchy
    processed_ids = set()
    for cat_id in new_article_category_ids:
        if cat_id and cat_id not in processed_ids:
            current = category_map.get(cat_id)
            while current:
                if current.id in processed_ids:
                    # If we reach a branch that has already been processed, we can stop
                    break
                current.has_new_articles = True
                processed_ids.add(current.id)
                current = category_map.get(current.parent_id) if current.parent_id else None

    # The main list of categories for rendering
    root_categories = [cat for cat in categories if cat.parent_id is None]
    
    return {'menu_categories': root_categories}


def dashboard_charts(request):
    # Feedbacks per day chart
    feedbacks_per_day = Feedback.objects.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')
    feedbacks_per_day_labels = [f['day'].strftime('%Y-%m-%d') for f in feedbacks_per_day]
    feedbacks_per_day_data = [f['count'] for f in feedbacks_per_day]

    return {
        'feedbacks_per_day_labels': feedbacks_per_day_labels,
        'feedbacks_per_day_data': feedbacks_per_day_data,
    }