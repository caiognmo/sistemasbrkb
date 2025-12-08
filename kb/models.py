from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome da categoria.")
    descricao = models.TextField(blank=True, help_text="Descrição opcional da categoria.")
    icon = models.CharField(max_length=50, blank=True, help_text="Classe do ícone Font Awesome (ex: fa-solid fa-book).")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', help_text="Categoria pai, se for uma sub-categoria.")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição da categoria.")

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('kb:artigo-list', args=[self.id])

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def get_descendants(self, include_self=False):
        descendants = []
        if include_self:
            descendants.append(self)
        for child in self.children.all():
            descendants.extend(child.get_descendants(include_self=True))
        return descendants

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['ordem', 'nome']

from tinymce.models import HTMLField
from django.utils.text import slugify

class Artigo(models.Model):
    titulo = models.CharField(max_length=200, help_text="Título do artigo.")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, help_text="URL amigável gerada a partir do título.")
    conteudo = HTMLField(help_text="Conteúdo do artigo.")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="artigos", help_text="Categoria à qual o artigo pertence.")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="artigos_criados")
    data_publicacao = models.DateTimeField(auto_now_add=True, help_text="Data de publicação do artigo.")
    ultima_atualizacao = models.DateTimeField(auto_now=True, help_text="Data da última atualização do artigo.")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição do artigo.")
    show_new_in_title = models.BooleanField(default=False, help_text="Marque para exibir a tag 'Novo' no título do artigo.")
    show_new_in_category_list = models.BooleanField(default=False, help_text="Marque para exibir a tag 'Novo' na lista de categorias.")
    show_new_in_subcategory_list = models.BooleanField(default=False, help_text="Marque para exibir a tag 'Novo' na lista de subcategorias.")
    show_new_in_header = models.BooleanField(default=False, help_text="Marque para exibir a tag 'Novo' no cabeçalho do artigo.")
    highlight_in_menu = models.BooleanField(default=False, help_text="Marque para destacar este artigo nos menus.")

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('kb:artigo-detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
            # Garante que o slug seja único
            original_slug = self.slug
            queryset = Artigo.objects.all()
            if self.pk:
                queryset = queryset.exclude(pk=self.pk)
            
            counter = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['ordem', 'titulo']

class Feedback(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='feedback', verbose_name="Artigo")
    rating = models.BooleanField(help_text="True for like, False for dislike", verbose_name="Rating")
    reason = models.CharField(max_length=50, blank=True, null=True, help_text="Reason for dislike", verbose_name="Reason")
    comment = models.TextField(blank=True, null=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")

    def __str__(self):
        return f"Feedback for {self.artigo.titulo}"

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()