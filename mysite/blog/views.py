from django.shortcuts import render, get_object_or_404
from .models import Post

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
def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts':posts})

# View para exibir apenas uma única postagem. (detalhes da postagem)
# Recebe os argumentos: year, month, day e post.
#    Para obter uma postagem publicada com slug e a data especificados.
# Obs. quando criamos o modelo post, adicionamos o parâmetro unique_for_date no campo slug.
#      Isso garante que haverá apenas uma postagem com um slug para uma determinada data.
#      Desse modo, será possível obter postagens únicas usando o slug e a data.
def post_detail(request):
    post = get_object_or_404(Post, slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    return render(request,
                    'blog/post/detail.html',
                    {'post':post})
