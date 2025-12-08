import os
import re
from bs4 import BeautifulSoup
from kb.models import Artigo

print("Iniciando script final para corrigir links de imagens...")

updated_count = 0
processed_images = 0

for artigo in Artigo.objects.all():
    if not artigo.conteudo:
        continue

    made_change = False
    soup = BeautifulSoup(artigo.conteudo, 'html.parser')
    images = soup.find_all('img')

    if not images:
        continue

    for img in images:
        old_src = img.get('src')
        if old_src and not old_src.startswith('/media/'):
            # Extrai o nome do arquivo da URL, removendo parâmetros
            file_name = os.path.basename(old_src.split('?')[0])
            if file_name:
                new_src = f'/media/{file_name}'
                img['src'] = new_src
                made_change = True
                processed_images += 1
    
    if made_change:
        artigo.conteudo = str(soup)
        artigo.save(update_fields=['conteudo'])
        updated_count += 1
        print(f"[SUCESSO] Artigo '{artigo.titulo}' atualizado.")

print(f"\n--- Correção de Imagens Finalizada ---")
print(f"{updated_count} artigos foram atualizados.")
print(f"{processed_images} links de imagem foram corrigidos no total.")