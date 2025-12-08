from django.urls import path
from .views import HomePageView, ArtigoListView, ArtigoDetailView, ArtigoSearchView, feedback_view

app_name = 'kb'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categoria/<int:categoria_id>/', ArtigoListView.as_view(), name='artigo-list'),
    path('artigo/<int:pk>/<slug:slug>/', ArtigoDetailView.as_view(), name='artigo-detail'),
    path('search/', ArtigoSearchView.as_view(), name='artigo-search'),
    path('feedback/', feedback_view, name='feedback'),
]