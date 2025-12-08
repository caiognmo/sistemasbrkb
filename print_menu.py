
import os
import re
import codecs

def print_menu():
    main_html_path = os.path.abspath(os.path.join(os.getcwd(), 'Base Definitiva', 'suporte.sistemasbr.com.br_443', 'kb', 'pt-br', 'article', '219538', 'comece-por-aqui80c0.html'))

    if not os.path.exists(main_html_path):
        print(f"Arquivo HTML principal não encontrado: {main_html_path}")
        return

    with open(main_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    menu_match = re.search(r'<ul class="kb-menu-container">.*?</ul>', html_content, re.DOTALL)
    if not menu_match:
        print("Menu container não encontrado.")
        return

    menu_html = menu_match.group(0)
    print(menu_html)

if __name__ == "__main__":
    print_menu()
