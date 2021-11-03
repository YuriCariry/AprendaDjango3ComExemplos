from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

 # gerenciador personalizado, depois de alterar, deve reiniciar o servidor (comando: python manage.py shell).
    # o método get_queryset(self) devolve o QuerySet que será executado. Sobrescrevemos para incluir o filtro.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset()\
                    .filter(status='published')

class Post(models.Model):
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
    # ...
    objects = models.Manager() # gerenciador default
    published = PublishedManager() # gerenciador personalizado


    class Meta:
        ordering = ('-publish',)
        # default_manager_name = objects # pode alterar para o gerenciador personalizado.

        def __str__(self):
            return self.title
