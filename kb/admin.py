from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path, reverse
from .models import Categoria, Artigo, Feedback, Profile
from .forms import ExcelUploadForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
import openpyxl
from django.utils.html import format_html, strip_tags
from django.db import models
from django.forms import TextInput, Textarea

# --- Custom User Admin ---

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    readonly_fields = ('last_login', 'date_joined')

    def get_fieldsets(self, request, obj=None):
        if not obj:  # Add form
            return self.add_fieldsets
        
        # Change form
        return (
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
            ('Important dates', {'fields': ('last_login', 'date_joined')}),
        )

    def get_form(self, request, obj=None, **kwargs):
        # On the change form, make the password field non-editable and show the help text.
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['password'].widget.attrs['readonly'] = True
            form.base_fields['password'].help_text = (
                'As senhas brutas não são armazenadas, então não há como ver a senha deste usuário, mas você pode alterar a senha usando <a href="../password/">este formulário</a>.'
            )
        return form

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Unregister the original User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'parent', 'ordem')
    search_fields = ('nome',)
    list_filter = ('parent',)
    ordering = ('ordem', 'nome',)
    fields = ('nome', 'descricao', 'icon', 'parent', 'ordem')

    def nome_hierarquico(self, obj):
        level = obj.get_level()
        if level > 0:
            return format_html(f'<span style="padding-left: {level * 20}px;">&mdash; {obj.nome}</span>')
        return obj.nome
    nome_hierarquico.short_description = 'Nome da Categoria'

from django.contrib.admin import SimpleListFilter

class CategoriaDescendenteFilter(SimpleListFilter):
    title = 'Categoria (incluindo subcategorias)'
    parameter_name = 'categoria_descendente'

    def lookups(self, request, model_admin):
        categorias = Categoria.objects.filter(parent__isnull=True).order_by('nome')
        lookups = []
        for cat in categorias:
            lookups.append((str(cat.id), cat.nome))
            for child in cat.children.all().order_by('nome'):
                lookups.append((str(child.id), f'-- {child.nome}'))
        return lookups

    def queryset(self, request, queryset):
        if self.value():
            categoria_id = int(self.value())
            categoria_selecionada = Categoria.objects.get(id=categoria_id)
            
            descendant_ids = [c.id for c in categoria_selecionada.get_descendants(include_self=True)]
            
            return queryset.filter(categoria__id__in=descendant_ids)
        return queryset

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'data_publicacao', 'ultima_atualizacao', 'ordem', 'show_new_in_title', 'show_new_in_category_list', 'show_new_in_subcategory_list', 'show_new_in_header')
    search_fields = ('titulo', 'conteudo')
    list_filter = (CategoriaDescendenteFilter, 'autor', 'data_publicacao')
    date_hierarchy = 'data_publicacao'
    ordering = ('ordem', 'titulo',)
    prepopulated_fields = {'slug': ('titulo',)}
    fieldsets = (
        (None, {
            'fields': ('titulo', 'slug', 'conteudo', 'categoria', 'autor', 'ordem')
        }),
        ('Destaque', {
            'fields': ('show_new_in_title', 'show_new_in_category_list', 'show_new_in_subcategory_list', 'show_new_in_header', 'highlight_in_menu')
        }),
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('artigo', 'rating_icon', 'reason', 'short_comment', 'created_at')
    list_filter = ('rating', 'reason', 'created_at')
    search_fields = ('artigo__titulo', 'comment')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    change_form_template = 'admin/feedback_detail.html'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def rating_icon(self, obj):
        if obj.rating:
            return format_html('<i class="fas fa-thumbs-up" style="color: green;"></i>')
        else:
            return format_html('<i class="fas fa-thumbs-down" style="color: red;"></i>')
    rating_icon.short_description = 'Rating'

    def short_comment(self, obj):
        if obj.comment and len(obj.comment) > 50:
            return obj.comment[:50] + '...'
        return obj.comment
    short_comment.short_description = 'Comment'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['chart_data'] = self.get_chart_data()
        return super().changelist_view(request, extra_context=extra_context)

    def get_chart_data(self):
        likes = Feedback.objects.filter(rating=True).count()
        dislikes = Feedback.objects.filter(rating=False).count()
        return {
            'labels': ['Likes', 'Dislikes'],
            'data': [likes, dislikes],
        }
