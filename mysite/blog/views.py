from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core,mail import send_mail
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

# Definimos a view post_share que recebe o objeto request e a variável post_id como parâmetros
#	Usamos o atalho get_object_or_404 para obter a postagem com base no id e garantimos que a postagem obtida tenha um status igual a published
#	Usamos a mesma view para exibir o formulário inicial e para processar os dados submetidos.
#		Diferencia se o form foi submetido com base no método de request e submetemos o form com POST
#		Se recebemos uma requisição GET, o form vazio será exibido,
#		se recebemos uma requisição POST, o form foi submetido e deverá ser processado.
#	Obs. Se o formulário for válido, obtemos os dados validados acessando form.cleaned_data. É um dicionário dos campos do formulário e seus valores.

def post_share(request, post_id):
	# Obtém a postagem com base no id
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False

	if request.method == 'POST':
		# Formulário foi submetido
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Campos do formulário passaram pela validação
			cd = form.cleaned_data
			# ... envia o email
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = f"{cd['name']} recommends you read " \
					  f"{post.title}"
			message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render (request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
