import os
import json
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from kb.models import Categoria, Artigo
from bs4 import BeautifulSoup
import codecs
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Populates the database with categories and articles from full_structure.json.'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population from full_structure.json...')

        # 1. Create a map of article ID to HTML file path
        self.stdout.write('Mapping article files...')
        article_file_map = {}
        base_dir = os.path.abspath(os.path.join(os.getcwd(), 'Base Definitiva'))
        for root, _, files in os.walk(base_dir):
            parts = root.split(os.sep)
            if "article" in parts:
                try:
                    article_index = parts.index("article")
                    if article_index + 1 < len(parts):
                        article_id = parts[article_index + 1]
                        if article_id.isdigit():
                            for file in files:
                                if file.endswith('.html'):
                                    article_file_map[article_id] = os.path.join(root, file)
                except ValueError:
                    pass # 'article' not in the path
        self.stdout.write(f'{len(article_file_map)} article files mapped.')

        # 2. Clear Categoria and Artigo tables
        self.stdout.write('Clearing database...')
        Artigo.objects.all().delete()
        Categoria.objects.all().delete()

        # 3. Get or create a User
        user, created = User.objects.get_or_create(username='admin')
        if created:
            user.set_password('admin')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write('Admin user created.')

        # 4. Read full_structure.json and create categories and articles
        self.stdout.write('Creating categories and articles...')
        full_structure_file_path = os.path.join(os.getcwd(), 'full_structure.json')
        with open(full_structure_file_path, 'r', encoding='utf-8') as f:
            full_structure_data = json.load(f)

        with open(os.path.join(os.getcwd(), 'icon_map.json'), 'r', encoding='utf-8') as f:
            icon_map = json.load(f)
        
        order_map = {
            "Primeiros passos": 1,
            "Funcionalidades": 2,
            "Fiscal": 3,
            "Relatórios": 4,
            "Migrações": 5,
            "Integrações": 6,
            "Apps": 7,
            "Indicadores": 8,
            "PDVgo": 9
        }

        def clean_article_html(html_content):
            if not html_content:
                return ''
            soup = BeautifulSoup(html_content, 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    parsed_url = urlparse(src)
                    filename = os.path.basename(parsed_url.path)
                    filename = filename.split('?')[0]
                    img['src'] = f'/media/{filename}'
            return str(soup)

        def process_items(items, parent_category=None):
            article_counter = 1
            for item in items:
                if item['type'] == 'category':
                    ordem = order_map.get(item['name'], 0) if parent_category is None else 0
                    icon = icon_map.get(item['name'], '')
                    
                    category_obj, _ = Categoria.objects.get_or_create(
                        nome=item['name'],
                        parent=parent_category,
                        defaults={'ordem': ordem, 'icon': icon}
                    )
                    
                    process_items(item['subcategories'], category_obj)
                    process_items(item['articles'], category_obj)
                
                elif item['type'] == 'article':
                    article_id = item.get('id')
                    if not article_id:
                        continue

                    file_path = article_file_map.get(article_id)
                    if not file_path:
                        self.stderr.write(f'HTML file for article ID {article_id} not found.')
                        continue

                    try:
                        with codecs.open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        with codecs.open(file_path, 'r', encoding='latin-1') as f:
                            content = f.read()
                    
                    soup = BeautifulSoup(content, 'html.parser')
                    article_content_div = soup.find('div', class_='article-content')
                    article_content = str(article_content_div) if article_content_div else ''
                    cleaned_content = clean_article_html(article_content)

                    Artigo.objects.create(
                        titulo=item['title'],
                        conteudo=cleaned_content,
                        categoria=parent_category,
                        autor=user,
                        ordem=article_counter
                    )
                    article_counter += 1

        process_items(full_structure_data)

        self.stdout.write(self.style.SUCCESS('Database population complete.'))