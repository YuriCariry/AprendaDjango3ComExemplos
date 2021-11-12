from django.contrib import admin
from .models import Post, Comment

# Register your models here.
# admin.site.register(Post)
# Decorador que tem o mesmo propósito da função admin.site.register(Post) e registra a classe, ModelAdmin, decorada por ele.
# Classe personalizada que herda ModelAdmin, permite alterar como exibir o modelo e interagir com ele.
# Permite definir os campos do seu modelo que você quer que sejam exibidos na página de lista de objetos do site de administração.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status')
    list_filter = ('status','created','publish','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy ='publish'
    ordering = ('status','publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')
