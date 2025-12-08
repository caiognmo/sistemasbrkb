
import os
import re
import json
import codecs
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_id_from_url(url):
    if not url:
        return None
    match = re.search(r'/article/(\d+)/', url)
    if match:
        return match.group(1)
    return None

def clean_category_name(name):
    return re.sub(r'^\d{2,}[\s.-]*', '', name).strip()

def process_li(li_element):
    category_link = li_element.find("a", recursive=False)
    if not category_link:
        return None

    class_name = li_element.get("class", [])
    
    if "Category" in class_name:
        category_name = clean_category_name(category_link.text)
        item = {
            "type": "category",
            "name": category_name,
            "subcategories": [],
            "articles": []
        }
        nested_ul = li_element.find("ul")
        if nested_ul:
            for sub_li in nested_ul.find_all('li', recursive=False):
                processed_item = process_li(sub_li)
                if processed_item:
                    if processed_item['type'] == 'category':
                        item["subcategories"].append(processed_item)
                    else:
                        item["articles"].append(processed_item)
        return item

    elif "Article" in class_name:
        article_title = clean_category_name(category_link.text)
        article_url = category_link.get("href")
        article_id = extract_id_from_url(article_url)
        if not article_id:
            li_id = li_element.get("id", "")
            match = re.search(r'-(\d+)$', li_id)
            if match:
                article_id = match.group(1)

        return {
            "type": "article",
            "id": article_id,
            "title": article_title,
            "url": article_url
        }
    return None

def generate_full_structure():
    print("Iniciando a geração da estrutura completa da base de conhecimento...")
    main_html_path = os.path.abspath(os.path.join(os.getcwd(), 'Base Definitiva', 'suporte.sistemasbr.com.br', 'kb', 'article', '218788', 'boas-vindas-base-conhecimento.html'))

    if not os.path.exists(main_html_path):
        print(f"Arquivo HTML principal não encontrado: {main_html_path}")
        return

    with open(main_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    
    menu_container = soup.find('ul', class_='kb-menu-container')
    if not menu_container:
        print("Menu container não encontrado.")
        return

    full_structure = []
    for li in menu_container.find_all('li', recursive=False):
        item = process_li(li)
        if item:
            full_structure.append(item)

    with open('full_structure.json', 'w', encoding='utf-8') as f:
        json.dump(full_structure, f, ensure_ascii=False, indent=4)

    print(f"Estrutura completa da base de conhecimento salva em 'full_structure.json'.")

if __name__ == "__main__":
    generate_full_structure()
