from django.contrib import admin
from .models import Aviso

@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'tipo_aviso', 'ativo')
    list_filter = ('tipo_aviso', 'ativo')
    search_fields = ('titulo', 'mensagem')
    readonly_fields = ('id',)
    
    fieldsets = (
        (None, {
            'fields': ('titulo', 'tipo_aviso', 'mensagem', 'ativo')
        }),
        ('Configurações do Botão (Apenas para Modo Janela)', {
            'fields': ('link_botao', 'texto_botao'),
        }),
    )

    class Media:
        js = ('sigecom_integration/js/notice_form.js',)
