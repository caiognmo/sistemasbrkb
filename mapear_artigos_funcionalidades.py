import os
import re
import json
import codecs
from bs4 import BeautifulSoup

def extract_id_from_url(url):
    match = re.search(r'/article/(\d+)/', url)
    if match:
        return match.group(1)
    return None

def clean_category_name(name):
    return re.sub(r'^\d{2,}[\s.-]*', '', name).strip()

def process_li(li_element, category_list):
    # Check for a category
    category_link = li_element.find("a", recursive=False)
    if category_link and "Category" in li_element.get("class", []):
        category_name = clean_category_name(category_link.text)
        new_category = {
            "name": category_name,
            "subcategories": [],
            "articles": []
        }
        category_list.append(new_category)
        
        # Process nested lists
        nested_ul = li_element.find("ul")
        if nested_ul:
            process_ul(nested_ul, new_category["subcategories"], new_category["articles"])

    # Check for an article
    article_link = li_element.find("a", recursive=False)
    if article_link and "Article" in li_element.get("class", []):
        article_title = clean_category_name(article_link.text)
        article_url = article_link.get("href")
        article_id = extract_id_from_url(article_url)
        if not article_id:
            # Try to get from li id
            li_id = li_element.get("id", "")
            match = re.search(r'-(\d+)$', li_id)
            if match:
                article_id = match.group(1)

        new_article = {
            "id": article_id,
            "title": article_title,
            "url": article_url
        }
        category_list.append(new_article)


def process_ul(ul_element, subcategories, articles):
    for li in ul_element.find_all("li", recursive=False):
        process_li(li, subcategories if "Category" in li.get("class", []) else articles)


def mapear_artigos_funcionalidades():
    print("Iniciando o mapeamento de artigos da categoria 'Funcionalidades'...")
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

    funcionalidades_li = None
    for li in menu_container.find_all('li', class_='Category', recursive=False):
        a = li.find('a', recursive=False)
        if a and 'Funcionalidades' in a.text:
            funcionalidades_li = li
            break
    
    if not funcionalidades_li:
        print("Categoria 'Funcionalidades' não encontrada no menu.")
        return

    funcionalidades_ul = funcionalidades_li.find('ul')
    if not funcionalidades_ul:
        print("Nenhuma subcategoria ou artigo encontrado em 'Funcionalidades'.")
        return

    funcionalidades_structure = {
        "name": "Funcionalidades",
        "subcategories": [],
        "articles": []
    }

    process_ul(funcionalidades_ul, funcionalidades_structure["subcategories"], funcionalidades_structure["articles"])

    with open('funcionalidades_structure.json', 'w', encoding='utf-8') as f:
        json.dump(funcionalidades_structure, f, ensure_ascii=False, indent=4)

    print(f"Mapeamento de artigos de 'Funcionalidades' concluído. Estrutura salva em 'funcionalidades_structure.json'.")

if __name__ == "__main__":
    mapear_artigos_funcionalidades()