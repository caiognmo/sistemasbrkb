from django.http import JsonResponse
from .models import Aviso
import json

def export_avisos_json(request):
    """
    Gera um JSON com os avisos ativos, seguindo a estrutura especificada.
    Ordem dos campos: id, titulo, mensagem, link_botao, texto_botao, tipo_aviso.
    """
    avisos_ativos = Aviso.objects.filter(ativo=True)
    
    lista_de_avisos = []
    for aviso in avisos_ativos:
        aviso_data = {
            "id": aviso.get_export_id(),
            "titulo": aviso.titulo,
            "mensagem": aviso.mensagem_rtf,
            "link_botao": aviso.link_botao if aviso.tipo_aviso == 'card' else "",
            "texto_botao": aviso.texto_botao if aviso.tipo_aviso == 'card' else "",
            "tipo_aviso": aviso.get_tipo_aviso_display()
        }
        lista_de_avisos.append(aviso_data)
        
    return JsonResponse(lista_de_avisos, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})
