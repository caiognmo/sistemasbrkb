from django.core.management.base import BaseCommand
from kb.models import Categoria, Artigo

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados de teste para a Base de Conhecimento.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando dados de teste...')

        # Limpa dados existentes para evitar duplicatas
        Artigo.objects.all().delete()
        Categoria.objects.all().delete()

        # Create Categories
        cat_financeiro, _ = Categoria.objects.update_or_create(
            nome='Financeiro',
            defaults={'descricao': 'Artigos sobre o módulo financeiro.', 'icon': 'fa-solid fa-piggy-bank'}
        )
        cat_vendas, _ = Categoria.objects.update_or_create(
            nome='Vendas',
            defaults={'descricao': 'Tudo sobre o processo de vendas.', 'icon': 'fa-solid fa-tags'}
        )
        cat_config, _ = Categoria.objects.update_or_create(
            nome='Configurações Gerais',
            defaults={'descricao': 'Configurações do sistema e permissões.', 'icon': 'fa-solid fa-gears'}
        )

        # Create Sub-categories
        Categoria.objects.update_or_create(
            nome='Contas a Pagar',
            parent=cat_financeiro,
            defaults={'descricao': 'Artigos sobre contas a pagar.', 'icon': 'fa-solid fa-file-invoice-dollar'}
        )
        Categoria.objects.update_or_create(
            nome='Contas a Receber',
            parent=cat_financeiro,
            defaults={'descricao': 'Artigos sobre contas a receber.', 'icon': 'fa-solid fa-hand-holding-dollar'}
        )

        # Create Articles
        Artigo.objects.create(
            titulo='Como emitir uma Nota Fiscal',
            categoria=cat_financeiro,
            conteudo='Passo 1: Abra o menu Fiscal.\nPasso 2: Selecione a opção "Emitir NF-e".\nPasso 3: Preencha os dados e clique em "Transmitir".'
        )
        Artigo.objects.create(
            titulo='Configurando Contas a Pagar',
            categoria=cat_financeiro,
            conteudo='Para configurar as contas a pagar, acesse o menu Financeiro > Configurações e defina os padrões de pagamento.'
        )
        Artigo.objects.create(
            titulo='Criando um Novo Pedido de Venda',
            categoria=cat_vendas,
            conteudo='O processo de criação de um novo pedido é simples. Vá em Vendas > Pedidos e clique em "Novo".'
        )
        Artigo.objects.create(
            titulo='Ajustando as Permissões de Usuário',
            categoria=cat_config,
            conteudo='Apenas administradores podem ajustar permissões. Acesse Configurações > Usuários, selecione o usuário e edite seu perfil de permissão.'
        )
        Artigo.objects.create(
            titulo='Relatório de Vendas por Período',
            categoria=cat_vendas,
            conteudo='Para gerar um relatório de vendas, acesse o menu Relatórios > Vendas e escolha o período desejado.'
        )

        self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso!'))
