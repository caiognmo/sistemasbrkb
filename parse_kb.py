import os
import re
import json
import codecs
from openpyxl import Workbook

def clean_html(raw_html):
    # Remove script and style elements
    clean_re = re.compile('<script[^>]*>.*?</script>|<style[^>]*>.*?</style>', re.DOTALL)
    clean_text = re.sub(clean_re, '', raw_html)
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', clean_text)
    # Remove HTML entities
    clean_text = re.sub(r'&[^;]+;', '', clean_text)
    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())
    return clean_text

def parse_kb():
    print("Starting knowledge base parsing...")
    base_dir = os.path.abspath(os.path.join(os.getcwd(), 'Base Definitiva'))
    main_html_path = os.path.join(base_dir, 'suporte.sistemasbr.com.br_443', 'kb', 'pt-br', 'article', '218788', 'boas-vindas-base-conhecimento.html')
    
    # 1. Build category map from the main menu
    url_to_category = {}
    try:
        with codecs.open(main_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        menu_match = re.search(r'<ul class="kb-menu-container">.*?</ul>', html_content, re.DOTALL)
        if menu_match:
            menu_html = menu_match.group(0)
            category_stack = []
            lines = menu_html.split('\n')
            for line in lines:
                indentation = len(line) - len(line.lstrip(' '))
                while category_stack and category_stack[-1]['indentation'] >= indentation:
                    category_stack.pop()

                category_match = re.search(r'<li class="Category.*?"><a href="(.*?)".*?>(.*?)</a>', line)
                if category_match:
                    category_name_raw = category_match.group(2).strip()
                    category_name = re.sub(r'^\d{2,}[\s.-]*', '', category_name_raw).strip()
                    if category_stack:
                        parent_name = category_stack[-1]['name']
                        full_category_name = f"{parent_name} / {category_name}"
                    else:
                        full_category_name = category_name
                    category_stack.append({'name': full_category_name, 'indentation': indentation})
                    continue

                article_match = re.search(r'<li class="Article.*?"><a href="(.*?)".*?>(.*?)</a>', line)
                if article_match:
                    article_url = article_match.group(1)
                    if category_stack:
                        category_name = category_stack[-1]['name']
                    else:
                        category_name = "Geral"
                    article_id_match = re.search(r'/article/(\d+)/', article_url)
                    if article_id_match:
                        article_id = article_id_match.group(1)
                        url_to_category[article_id] = category_name
    except Exception as e:
        print(f"Could not build category map: {e}")

    print(f"Category map built with {len(url_to_category)} entries.")

    # 2. Iterate through files and extract articles
    articles = []
    html_files_path = os.path.join(base_dir, 'suporte.sistemasbr.com.br_443')
    for root, _, files in os.walk(html_files_path):
        for file in files:
            if file.endswith('.html'):
                html_file_path = os.path.join(root, file)
                try:
                    with codecs.open(html_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with codecs.open(html_file_path, 'r', encoding='latin-1') as f:
                        content = f.read()

                title_match = re.search(r'<div class="md-article-title" id="article-title">(.*?)</div>', content, re.DOTALL)
                if not title_match:
                    continue
                
                title = clean_html(title_match.group(1))

                content_match = re.search(r'<div class="article-content fr-view">(.*?)</div>', content, re.DOTALL)
                article_body = clean_html(content_match.group(1)) if content_match else ""

                article_id_from_path_match = re.search(r'/article/(\d+)/', html_file_path)
                category = "Geral"
                if article_id_from_path_match:
                    article_id = article_id_from_path_match.group(1)
                    if article_id in url_to_category:
                        category = url_to_category[article_id]

                articles.append({
                    'titulo': title,
                    'conteudo': article_body,
                    'categoria_nome': category,
                    'autor_username': 'admin'
                })

    # 3. Create Excel file
    wb = Workbook()
    ws = wb.active
    ws.title = "Artigos"
    headers = ["titulo", "conteudo", "categoria_nome", "autor_username"]
    ws.append(headers)
    for article in articles:
        ws.append([article['titulo'], article['conteudo'], article['categoria_nome'], article['autor_username']])

    excel_filename = "artigos_importados_final.xlsx"
    wb.save(excel_filename)
    print(f"Arquivo Excel '{excel_filename}' gerado com sucesso com {len(articles)} artigos.")


if __name__ == "__main__":
    parse_kb()