
import os
import json
import re

def extract_categories_from_dirs():
    print("Starting category extraction from directories...")
    base_path = os.path.abspath(os.path.join(os.getcwd(), 'Base Definitiva', 'suporte.sistemasbr.com.br_443', 'kb', 'pt-br', 'category'))
    
    categories = []
    found_categories = set()

    if os.path.exists(base_path):
        for item in os.listdir(base_path):
            if os.path.isdir(os.path.join(base_path, item)):
                category_name = re.sub(r'^\d{2,}[\s.-]*', '', item).replace('-', ' ').strip()
                if category_name and category_name not in found_categories:
                    categories.append({
                        'name': category_name,
                        'parent': None
                    })
                    found_categories.add(category_name)

    with open('categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=4)
        
    print(f"Category extraction complete. Found {len(categories)} categories.")

if __name__ == "__main__":
    extract_categories_from_dirs()
