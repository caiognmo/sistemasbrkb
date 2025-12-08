
from django.core.management.base import BaseCommand
from kb.models import Categoria

class Command(BaseCommand):
    help = 'Define o ícone para uma categoria'

    def add_arguments(self, parser):
        parser.add_argument('category_name', type=str, help='O nome da categoria a ser atualizada')
        parser.add_argument('icon_class', type=str, help='A classe do ícone Font Awesome (ex: fa-solid fa-book)')

    def handle(self, *args, **options):
        category_name = options['category_name']
        icon_class = options['icon_class']

        try:
            categoria = Categoria.objects.get(nome=category_name)
            categoria.icon = icon_class
            categoria.save()
            self.stdout.write(self.style.SUCCESS(f'Ícone para a categoria "{category_name}" atualizado com sucesso para "{icon_class}".'))
        except Categoria.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Categoria "{category_name}" não encontrada.'))
