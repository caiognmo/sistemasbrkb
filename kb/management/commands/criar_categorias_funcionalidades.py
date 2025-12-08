import os
import re
from django.core.management.base import BaseCommand
from kb.models import Categoria

class Command(BaseCommand):
    help = 'Cria as categorias da seção "Funcionalidades"'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando a criação das categorias de "Funcionalidades"...')

        funcionalidades_cat, _ = Categoria.objects.get_or_create(nome='02 - Funcionalidades')
        funcionalidades_cat.icon = 'fa-solid fa-cogs'
        funcionalidades_cat.save()

        sub_categories = [
            '01 - Clientes',
            '02 - Fornecedores',
            '03 - Transportadoras',
            '04 - Produtos e Serviços',
            '05 - Estoque',
            '06 - Etiquetas',
            '07 - Compras',
            '08 - Cotação',
            '09 - Ordem de Serviço',
            '10 - Orçamento',
            '11 - Pedidos',
            '12 - Condicional',
            '13 - Devolução',
            '14 - Comissão',
            '15 - Bonificação',
            '16 - Financeiro',
            '17 - Notificações',
            '18 - Pré venda',
            '19 - Entrega',
            '20 - Delivery Sigecom',
            '21 - Boletos',
            '22 - Solicitação de compra',
            '23 - Controle de promoções',
            '24 - Kit de produtos',
        ]

        for sub_cat_name in sub_categories:
            Categoria.objects.get_or_create(nome=sub_cat_name, parent=funcionalidades_cat)
            self.stdout.write(f"Categoria criada: {sub_cat_name}")

        self.stdout.write(self.style.SUCCESS('Categorias de "Funcionalidades" criadas com sucesso.'))