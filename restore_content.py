
import os
import re
from bs4 import BeautifulSoup
from kb.models import Artigo

print("--- INICIANDO MIGRAÇÃO FINAL DE CONTEÚDO E IMAGENS ---")

def clean_title(title):
    if not title:
        return ''
    return re.sub(r'^\s*\d+[\.\d]*\s*-\s*', '', title).strip()

db_articles = {clean_title(art.titulo): art for art in Artigo.objects.all()}
base_path = os.path.join(os.getcwd(), 'Base Definitiva')
article_files = []
for root, dirs, files in os.walk(base_path):
    if 'article' in root:
        for file in files:
            if file.endswith('.html'):
                article_files.append(os.path.join(root, file))

updated_count = 0

for file_path in article_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        title_tag = soup.find('div', class_='md-article-title')
        content_tag = soup.find('div', class_='article-content')

        if not title_tag or not content_tag:
            continue

        html_title = title_tag.get_text(strip=True)
        cleaned_html_title = clean_title(html_title)
        artigo_to_update = db_articles.get(cleaned_html_title)

        if artigo_to_update:
            images = content_tag.find_all('img')
            for img in images:
                old_src = img.get('src')
                if old_src and not old_src.startswith('/media/'):
                    filename = os.path.basename(old_src.split('?')[0])
                    if filename:
                        img['src'] = f'/media/{filename}'
            
            artigo_to_update.conteudo = str(content_tag)
            artigo_to_update.save(update_fields=['conteudo'])
            updated_count += 1
            print(f"[SUCESSO] Conteúdo e imagens do artigo '{artigo_to_update.titulo}' foram restaurados.")

    except Exception as e:
        print(f"[ERRO] Falha ao processar o arquivo {file_path}: {e}")

print(f"\n--- PROCESSO FINALIZADO ---")
print(f"{updated_count} artigos foram atualizados com sucesso.")
