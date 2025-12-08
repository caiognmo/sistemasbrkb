from django.core.management.base import BaseCommand
from kb.models import Artigo, Categoria

class Command(BaseCommand):
    help = 'Deleta todos os artigos e categorias do banco de dados'

    def handle(self, *args, **options):
        self.stdout.write('Deletando todos os artigos e categorias...')
        Artigo.objects.all().delete()
        Categoria.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Banco de dados limpo com sucesso!'))
