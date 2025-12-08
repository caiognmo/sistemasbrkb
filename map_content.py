
import os
import re
from bs4 import BeautifulSoup
from kb.models import Artigo

print("--- INICIANDO MAPEAMENTO (MODO DE LEITURA) ---")

# Função para limpar o título
def clean_title(title):
    if not title:
        return ''
    return re.sub(r'^\s*\d+[\.\d]*\s*-\s*', '', title).strip()

# 1. Mapear todos os artigos do banco de dados por título limpo
db_articles = {clean_title(art.titulo): art for art in Artigo.objects.all()}
print(f"{len(db_articles)} artigos encontrados no banco de dados.")

# 2. Encontrar todos os arquivos HTML de artigos no backup
base_path = os.path.join(os.getcwd(), 'Base Definitiva')
article_files = []
for root, dirs, files in os.walk(base_path):
    if 'article' in root:
        for file in files:
            if file.endswith('.html'):
                article_files.append(os.path.join(root, file))

print(f"{len(article_files)} arquivos de artigos encontrados no backup.")

# 3. Iterar e criar o mapa
found_count = 0
print("\n--- MAPA DE MIGRAÇÃO PROPOSTO ---")
for file_path in article_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        title_tag = soup.find('div', class_='md-article-title')
        if not title_tag:
            continue

        html_title = title_tag.get_text(strip=True)
        cleaned_html_title = clean_title(html_title)

        # Encontra o artigo correspondente no DB
        artigo_obj = db_articles.get(cleaned_html_title)

        if artigo_obj:
            found_count += 1
            print(f"\n[CORRESPONDÊNCIA ENCONTRADA]")
            print(f"  - Título no DB: {artigo_obj.titulo} (ID: {artigo_obj.id})")
            print(f"  - Título no Backup: {html_title}")
            
            images = soup.find_all('img')
            if images:
                print("  - Imagens a serem migradas:")
                for img in images:
                    src = img.get('src')
                    if src:
                        filename = os.path.basename(src.split('?')[0])
                        print(f"    - {filename}")
            else:
                print("  - Nenhuma imagem encontrada neste artigo.")

    except Exception as e:
        print(f"[ERRO] Falha ao processar o arquivo {file_path}: {e}")

print(f"\n--- FIM DO MAPEAMENTO ---")
print(f"{found_count} artigos do backup foram mapeados com sucesso para artigos no banco de dados.")

