import os
import re
import json

def map_categories():
    print("Starting category mapping...")
    main_html_path = 'C:\\Users\\Caio-SBR\\Documents\\projetos\\SistemasBr-KB\\Base Definitiva\\suporte.sistemasbr.com.br_443\\kb\\pt-br\\article\\218788\\boas-vindas-base-conhecimento.html'
    print(f"Attempting to open: {main_html_path}")

    with open(main_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    menu_match = re.search(r'<ul class="kb-menu-container">.*?</ul>', html_content, re.DOTALL)
    if not menu_match:
        print("Menu container not found.")
        return

    menu_html = menu_match.group(0)
    
    url_to_category = {}
    category_stack = []

    lines = menu_html.split('\n')
    
    for i, line in enumerate(lines):
        category_match = re.search(r'<li class="Category.*?>.*?<a href="(.*?)".*?>(.*?)</a>', line)
        if category_match:
            indentation = len(line) - len(line.lstrip())
            category_name = re.sub(r'^\d{2,}\s*-\s*', '', category_match.group(2).strip()).strip()
            
            while category_stack and category_stack[-1]['indentation'] >= indentation:
                category_stack.pop()
            
            if category_stack:
                parent_category = category_stack[-1]['name']
                full_category_name = f"{parent_category} / {category_name}"
            else:
                full_category_name = category_name
            
            category_stack.append({'name': full_category_name, 'indentation': indentation})
            continue

        article_match = re.search(r'<li class="Article.*?>.*?<a href="(.*?)".*?>(.*?)</a>', line)
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

    with open('category_map.json', 'w', encoding='utf-8') as f:
        json.dump(url_to_category, f, ensure_ascii=False, indent=4)
        
    print(f"Category map created with {len(url_to_category)} entries.")

if __name__ == "__main__":
    map_categories()