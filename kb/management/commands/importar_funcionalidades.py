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
    clean_text = html.unescape(raw_text)
    clean_text = ' '.join(clean_text.split())
    return clean_text

def fix_media_tags(raw_html):
    img_tags = re.findall(r'<img[^>]+src=["\\](.*?)[\"\][^>]*>', raw_html)
    for img_src in img_tags:
        filename = os.path.basename(img_src)
        new_src = os.path.join(settings.MEDIA_URL, filename)
        raw_html = raw_html.replace(img_src, new_src)

    iframe_tags = re.findall(r'<iframe.*?</iframe>', raw_html, re.DOTALL)
    for iframe_tag in iframe_tags:
        cleaned_iframe = re.sub(r'\s+(height|width)=".*?"', '', iframe_tag)
        raw_html = raw_html.replace(iframe_tag, cleaned_iframe)
        
    raw_html = re.sub(r'\s+style=".*?"', '', raw_html)
        
    return raw_html

class Command(BaseCommand):
    help = 'Importa os artigos da categoria "Funcionalidades"'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando a importação da categoria "Funcionalidades"...')

        # 1. Manually define the category and article structure
        funcionalidades_cat, _ = Categoria.objects.get_or_create(nome='Funcionalidades')
        funcionalidades_cat.icon = 'fa-solid fa-cogs'
        funcionalidades_cat.save()

        categories_and_articles = {
            'Clientes': {
                'icon': 'fa-solid fa-users',
                'articles': {
                    '218899': '01 - Cadastro de clientes',
                    '220052': '02 - Desconto padrão e tabela de preço',
                    '118861': '03 - Controle de aniversariantes',
                    '120781': '04 - Contratando a utilização de SMS e compra de crédito',
                }
            },
            'Fornecedores': {
                'icon': 'fa-solid fa-truck-field',
                'articles': {
                    '220020': '01 - Cadastro de fornecedores',
                }
            },
            'Transportadoras': {
                'icon': 'fa-solid fa-truck-fast',
                'articles': {
                    '221594': '01 - Cadastro de transportadoras',
                }
            },
            'Produtos e Serviços': {
                'icon': 'fa-solid fa-box-open',
                'articles': {
                    '219535': '01 - Cadastro de produtos',
                    '218840': '02 - Cadastro de categorias',
                    '218851': '03 - Cadastro de marcas',
                    '220277': '04 - Balança',
                    '221591': '05 - Tabelas de preço',
                    '224753': '05.1 - Permissões na tabela de preço',
                    '225461': '06 - Grade de itens',
                    '221918': '07 - Cadastro unidades de medida',
                    '240669': '08 - Função repetir',
                    '275020': '09 - Cadastro de serviços',
                    '367165': '10 - Pesquisa de produtos',
                },
                'sub_categories': {
                    'Gestão de validade': {
                        'icon': 'fa-solid fa-calendar-times',
                        'articles': {
                            '533683': '01 - Gestão de validade',
                            '533617': '02 - Cadastro de validade',
                            '533653': '03 - Controle de validade',
                        }
                    }
                }
            },
            'Estoque': {
                'icon': 'fa-solid fa-boxes-stacked',
                'articles': {
                    '227362': '02 - Análise de estoque',
                    '227364': '03 - Manutenção de estoque',
                    '227366': '04 - Entradas e saídas gerais',
                },
                'sub_categories': {
                    'Registros (IMEI, Série)': {
                        'icon': 'fa-solid fa-barcode',
                        'articles': {
                            '299002': '01 - Introdução e configuração de registros de estoque (IMEI, Série)',
                            '301505': '02 - Manutenção no cadastro de produtos (IMEI, Série)',
                            '301506': '03 - Fluxos de saída de registros (IMEI, Série)',
                            '301507': '04 - Fluxo de troca de produtos com registros (IMEI, Série)',
                            '301508': '05 - Emissão de NF-e de produtos com registros (IMEI, Série)',
                            '301509': '06 - Fluxo de entrada de registros por compras (IMEI, Série)',
                            '301510': '07 - Manutenção do estoque com registros (IMEI, Série)',
                            '301511': '08 - Logs de movimentação de registros (IMEI, Série)',
                        }
                    }
                }
            },
            # ... and so on
        }

        base_dir = os.path.abspath(os.path.join(os.getcwd(), 'Base Definitiva'))

        for cat_name, cat_data in categories_and_articles.items():
            parent_cat, _ = Categoria.objects.get_or_create(nome=cat_name, parent=funcionalidades_cat)
            parent_cat.icon = cat_data.get('icon', 'fa-solid fa-folder')
            parent_cat.save()

            for article_id, article_title in cat_data.get('articles', {}).items():
                article_path = None
                for root, _, files in os.walk(os.path.join(base_dir, 'suporte.sistemasbr.com.br_443')):
                    if article_id in root:
                        for file in files:
                            if file.endswith('.html'):
                                article_path = os.path.join(root, file)
                                break
                    if article_path:
                        break
                
                if not article_path:
                    self.stdout.write(self.style.ERROR(f"Arquivo para o artigo ID {article_id} não encontrado."))
                    continue

                try:
                    with codecs.open(article_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with codecs.open(article_path, 'r', encoding='latin-1') as f:
                        content = f.read()

                content_match = re.search(r'<div class="article-content fr-view">(.*?)</div>', content, re.DOTALL)
                article_body = content_match.group(1) if content_match else ""
                article_body = fix_media_tags(article_body)

                try:
                    author = User.objects.get(username='admin')
                except User.DoesNotExist:
                    author = User.objects.first()

                Artigo.objects.update_or_create(
                    titulo=clean_text(article_title),
                    defaults={
                        'conteudo': article_body,
                        'categoria': parent_cat,
                        'autor': author
                    }
                )
                self.stdout.write(f"Artigo importado/atualizado: {article_title}")

            if 'sub_categories' in cat_data:
                for sub_cat_name, sub_cat_data in cat_data['sub_categories'].items():
                    sub_cat, _ = Categoria.objects.get_or_create(nome=sub_cat_name, parent=parent_cat)
                    sub_cat.icon = sub_cat_data.get('icon', 'fa-solid fa-folder')
                    sub_cat.save()

                    for article_id, article_title in sub_cat_data.get('articles', {}).items():
                        article_path = None
                        for root, _, files in os.walk(os.path.join(base_dir, 'suporte.sistemasbr.com.br_443')):
                            if article_id in root:
                                for file in files:
                                    if file.endswith('.html'):
                                        article_path = os.path.join(root, file)
                                        break
                            if article_path:
                                break
                        
                        if not article_path:
                            self.stdout.write(self.style.ERROR(f"Arquivo para o artigo ID {article_id} não encontrado."))
                            continue

                        try:
                            with codecs.open(article_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                        except UnicodeDecodeError:
                            with codecs.open(article_path, 'r', encoding='latin-1') as f:
                                content = f.read()

                        content_match = re.search(r'<div class="article-content fr-view">(.*?)</div>', content, re.DOTALL)
                        article_body = content_match.group(1) if content_match else ""
                        article_body = fix_media_tags(article_body)

                        try:
                            author = User.objects.get(username='admin')
                        except User.DoesNotExist:
                            author = User.objects.first()

                        Artigo.objects.update_or_create(
                            titulo=clean_text(article_title),
                            defaults={
                                'conteudo': article_body,
                                'categoria': sub_cat,
                                'autor': author
                            }
                        )
                        self.stdout.write(f"Artigo importado/atualizado: {article_title}")

        self.stdout.write(self.style.SUCCESS("Importação da categoria 'Funcionalidades' concluída."))