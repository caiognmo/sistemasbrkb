
from django.core.management.base import BaseCommand
from kb.models import Categoria

class Command(BaseCommand):
    help = 'Lista todas as categorias e seus IDs'

    def handle(self, *args, **options):
        self.stdout.write('Categorias no banco de dados:')
        for categoria in Categoria.objects.all():
            self.stdout.write(f"  ID: {categoria.id}, Nome: {categoria.nome}")
