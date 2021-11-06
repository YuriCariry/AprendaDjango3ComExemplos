from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# Create your views here.
# Uma view é uma função python que recebe uma requisição web e devolve uma resposta.

# Recebe o objeto request como único parâmetro.(é necessário a todas as views)
# Obtém todas as postagens cujo status seja published,
# usando o gerenciador published que criamos em models.py.
# Por fim, usamos o atalho render, que renderiza a lista de postagens com o template especificado.
#    essa função recebe o objeto request, o path do template e as variáveis de contexto para renderizar o template.
#    Ela devolve um objeto HtmlResponse com o texto renderizado (ex: código html)
# O atalho render leva o contexto da requisição em consideração,
# logo, qualquer variável definida pelos códigos de processamento de contexto do template estarão acessíveis ao template definido.
# códigos de processamento de contexto do template  = callable que definem variáveis no contexto.
#def post_list(request):
#    posts = Post.published.all()
#    return render(request,
#                  'blog/post/list.html',
#                  {'posts' : posts})

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # três postagens em cada página.
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:         # Se a página não for um inteiro, exibe a primeira
        posts = paginator.page(1)
    except EmptyPage:                # Se a página estiver fora do intervalo, exibe a última.
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'page': page, 'posts': posts})

# View baseada em classe.
# Faz a mesma coisa que a view post_list
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# View para exibir apenas uma única postagem. (detalhes da postagem)
# Recebe os argumentos: year, month, day e post.
#    Para obter uma postagem publicada com slug e a data especificados.
# Obs. quando criamos o modelo post, adicionamos o parâmetro unique_for_date no campo slug.
#      Isso garante que haverá apenas uma postagem com um slug para uma determinada data.
#      Desse modo, será possível obter postagens únicas usando o slug e a data.
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post' : post})
