import os
import re
import codecs
import shutil
import html
from django.core.management.base import BaseCommand
from django.conf import settings
from kb.models import Artigo, Categoria
from django.contrib.auth.models import User

def clean_text(raw_text):
    # Unescape HTML entities
    clean_text = html.unescape(raw_text)
    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())
    return clean_text

def fix_media_tags(raw_html):
    # Fix image paths
    img_tags = re.findall(r'<img[^>]+src=["\"](.*?)["\"][^>]*>', raw_html)
    for img_src in img_tags:
        filename = os.path.basename(img_src)
        new_src = os.path.join(settings.MEDIA_URL, filename)
        raw_html = raw_html.replace(img_src, new_src)

    # Remove height and width from iframes
    iframe_tags = re.findall(r'<iframe.*?</iframe>', raw_html, re.DOTALL)
    for iframe_tag in iframe_tags:
        cleaned_iframe = re.sub(r'\s+(height|width)=["\"].*?["\"]', '', iframe_tag)
        raw_html = raw_html.replace(iframe_tag, cleaned_iframe)
        
    # Remove style attributes from all tags
    raw_html = re.sub(r'\s+style=["\"].*?["\"]', '', raw_html)
        
    return raw_html

class Command(BaseCommand):
    help = 'Importa os artigos da categoria "Primeiros passos"'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando a importação da categoria "Primeiros passos"...')

        base_dir = os.path.abspath(os.path.join(os.getcwd(), 'Base Definitiva'))
        media_dir = settings.MEDIA_ROOT

        # 1. Copy all image files to the media directory
        self.stdout.write("Copiando arquivos de imagem para o diretório de mídia...")
        image_count = 0
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    source_path = os.path.join(root, file)
                    dest_path = os.path.join(media_dir, file)
                    shutil.copy2(source_path, dest_path)
                    image_count += 1
        self.stdout.write(self.style.SUCCESS(f"{image_count} imagens copiadas."))

        # 2. Create the main category
        primeiros_passos_cat, created = Categoria.objects.get_or_create(nome='Primeiros passos')
        if created:
            self.stdout.write(self.style.SUCCESS('Categoria "Primeiros passos" criada com sucesso.'))

        # 3. Define the articles to import
        articles_to_import = {
            '219538': 'comece-por-aqui80c0.html',
            '224760': '01-instalacao-e-parametros-inciais244b.html',
            '218697': 'cadastro-estacao-sigecom02cb.html',
            '219714': 'cadastro-de-colaboradores2930.html',
            '219851': '05-cadastro-de-usuariosc59c.html',
            '221899': '01-permissoes-de-usuario6794.html',
            '224752': 'importar-exportar-permissaoe90a.html',
            '218804': 'cadastro-de-taxas-do-cartao2bb5.html',
            '224778': 'tipos-de-documento7c36.html',
            '225343': 'compensacao-automatica-dos-cartoes28fc.html',
            '225346': 'assistente-formas-de-pagamentod7e4.html',
            '225385': '11-assistente-de-fluxo-de-operacoesecfd.html',
            '225374': 'cadastro-de-caixas7c47.html',
            '227453': 'planos-de-contad90d.html',
            '237176': '14-backup-do-banco-de-dados67fd.html',
            '240696': 'configuracoes-do-tefc51f.html',
        }

        imported_count = 0
        for article_id, file_name in articles_to_import.items():
            article_path = os.path.join(base_dir, 'suporte.sistemasbr.com.br_443', 'kb', 'pt-br', 'article', article_id, file_name)
            
            if not os.path.exists(article_path):
                self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {article_path}"))
                continue

            try:
                with codecs.open(article_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with codecs.open(article_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao ler o arquivo {article_path} com latin-1: {e}"))
                    continue

            title_match = re.search(r'<div class="md-article-title" id="article-title">(.*?)</div>', content, re.DOTALL)
            if not title_match:
                self.stdout.write(self.style.WARNING(f"Título não encontrado em: {article_path}"))
                continue
            
            title = clean_text(title_match.group(1).strip())

            content_match = re.search(r'<div class="article-content fr-view">(.*?)</div>', content, re.DOTALL)
            article_body = content_match.group(1) if content_match else ""
            
            article_body = fix_media_tags(article_body)

            try:
                author = User.objects.get(username='admin')
            except User.DoesNotExist:
                author = User.objects.first()

            Artigo.objects.update_or_create(
                titulo=title,
                defaults={
                    'conteudo': article_body,
                    'categoria': primeiros_passos_cat,
                    'autor': author
                }
            )
            imported_count += 1
            self.stdout.write(f"Artigo importado/atualizado: {title}")

        self.stdout.write(self.style.SUCCESS(f'{imported_count} artigos importados/atualizados com sucesso na categoria "Primeiros passos".'))
