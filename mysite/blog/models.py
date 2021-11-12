from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

 # gerenciador personalizado, depois de alterar, deve reiniciar o servidor (comando: python manage.py shell).
    # o método get_queryset(self) devolve o QuerySet que será executado. Sobrescrevemos para incluir o filtro.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset()\
                    .filter(status='published')

class Post(models.Model):
    # Gerenciadores
    objects = models.Manager() # gerenciador default
    published = PublishedManager() # gerenciador personalizado

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default='draft')

    # Você utilizará o get_absolute_url() em seus templates para fazer a ligação com postagens específicas.
    # URLs canônicos para os modelos, é o URL preferencial para um recurso.
    # O método reverse, permite criar URLs com base no nome e aceita parâmetros opcionais.
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug
                        ])

    class Meta:
        ordering = ('-publish',)
        # default_manager_name = objects # pode alterar para o gerenciador personalizado.

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Comentado por {self.name} no {self.post}'
