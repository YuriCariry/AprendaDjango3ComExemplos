Tentando aprender Django.
Livro Aprenda Django3 com Exemplos.

Objetivos:
1. Criando uma aplicação de Blog

Cap2. Blog - Recursos Avançados

- Compartilhamento de postagens via email
- Adição de comentários em uma postagem
- Marcação de postagens com tags (permitem classificar o conteúdo de forma não-hierárquica, utilizando palavras-chaves simples.)
- Recomendação de postagens similares (após a criação das tags, recomendar o conteúdo aos leitores)

Assuntos abordados no capítulo:
- envio de emails com django
- criação de formulários e seu tratamento nas views
- criação de formulários a partir de modelos
- integração de aplicações de terceiros
- criação de QuerySets complexos

- Compartilhamento de postagens via email
	Será necessário:
		- criar um formulário para que os usuários preencham com nome, email, destinatário do email e comentários opcionais
		- criar uma view em views.py que cuide dos dados postados e envie o no email
		- adicionar um padrão de URL para a nova view em urls.py a aplicação blog
		- criar um template para exibir o formulário
	- Criando formulários com Django
		- Usar framework de formulários embutido no django.
			- facilita definir os campos do formulário, especificar como devem ser exibidos e como os dados de entrada devem ser validados.
			- o framework fornece um modo flexível de renderizar os formulários e lidar com os dados.
		Há 2 classes padrão:
			- Form: permite criar formulários padrão
			- ModelForm: permite criar formulários associados a instâncias de modelos
		Crie forms.py na aplicação blog.
		Código:
			from django import forms
			class EmailPostForm(forms.Form):
				name     = forms.CharField(max_lengh=25)
				email    = forms.EmailField()
				to       = forms.EmailField()
				comments = forms.CharField(required=False, widget=forms.Textarea)

		Criamos um formulário por meio de herança da classe-base Form.
		Obs. Convenciona colocar os formulários no arquivo forms.py em cada aplicação.
		Obs. CharField é renderizado como um elemento HTML <input type='text'>. é possível alterar o widget default(input) para determinar como o campo será renderizado em HTML.

	- Lidando com os formulários nas views
		Criar uma view para lidar com o formulário e enviar email quando sua submissão for feita com sucesso.
		Editar views.py da aplicação blog, adicionar:
		Código:
			from .forms import EmailPostForm
			def post_share(request, post_id):
				# Obtém a postagem com base no id
				post = get_object_or_404(Post, id=post_id, status='published')
				if request.method == 'POST':
					# Formulário foi submetido
					form = EmailPostForm(request.POST)
					if form.is_valid():
						# Campos do formulário passaram pela validação
						cd = form.cleaned_data
						# ... envia o email
				else:
					form = EmailPostForm()
				return render (request, 'blog/post/share.html', {'post':post, 'form':form})
		Definimos a view post_share que recebe o objeto request e a variável post_id como parâmetros
		Usamos o atalho get_object_or_404 para obter a postagem com base no id e garantimos que a postagem obtida tenha um status igual a published
		Usamos a mesma view para exibir o formulário inicial e para processar os dados submetidos.
			Diferencia se o form foi submetido com base no método de request e submetemos o form com POST
			Se recebemos uma requisição GET, o form vazio será exibido,
			se recebemos uma requisição POST, o form foi submetido e deverá ser processado.
		Obs. Se o formulário for válido, obtemos os dados validados acessando form.cleaned_data. É um dicionário dos campos do formulário e seus valores.

	- Enviando emails com django
		Inicialmente, precisa de um servidor SMTP local, ou deve definir a configuração de um servidor SMTP externo,
			acrescentando as configurações abaixo no settings.py do projeto.
			- EMAIL_HOST           : o host do servidor smtp, o default é localhost
			- EMAIL_PORT           : a porta smtp, o default é 25
			- EMAIL_HOST_USER	   : o nome do usuário para o servidor smtp
			- EMAIL_HOST_PASSWORD  : a senha para o servidor smtp
			- EMAIL_USE_TLS        : informa se uma conexão tls segura deve ser usada
			- EMAIL_USE_SLL        : informa se uma conexão sll segura implícita deve ser usada

		Para definir a configuração de um servidor SMTP externo:
			- EMAIL_HOST = 'smtp.gmail.com'
			- EMAIL_PORT = 587
			- EMAIL_HOST_USER = 'youraccount@gmail.com'
			- EMAIL_HOST_PASSWORD ='your_password'
			- EMAIL_USE_TLS = True

		Se não for possível usar um servidor SMTP, pode dizer ao django que escreva emails no console, adicionando a configuração abaixo em settings.py do projeto.
			- EMAIL_BACKEND = 'django.core.mail.backend.console.EmailBackend

		Exemplo: Execute
			python manage.py shell
			from django.core.mail import send_mail
			send_mail('Django mail', 'This email was sent with Django.',
					  'youraccount@gmail.com', ['youraccount@gmail.com'], fail_silently=False)
		Obs.: send_mail requer: assunto, mensagem, remetente e lista de destinatários.
		Obs.: fail_silently=False significa que caso o email não possa ser enviado corretamente, uma exceção deverá ser gerada. Se retornar 1, o email foi enviado com sucesso.
		Obs.: Para o gmail, é preciso permitir o acesso para aplicações menos seguras em https://myaccount.google.com/lesssecureapps
		Obs.: Para o gmail, é preciso desativar o captcha em https://accounts.google.com/displayunlockcaptcha
		Código: altere a view post_share no arquivo views.py da aplicação blog
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
						post_url = request.build_absolute_url(post.get_absolute_url())
						subject = f"{cd['name']} recommends you read " \
								  f"{post_title}"
						message = f"Read {post_title} at {post_url}\n\n" \
								  f"{cd['name']}\'s comments: {cd['comments']}"
						send_mail(subject, message, 'admin@myblog.com', [cd['to']])
						sent = True
				else:
					form = EmailPostForm()
				return render (request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})

		No código anterior:
			Declaramos sent e definimos com True quando a postagem é enviada.
				Usaremos sent no template para exibir uma mensagem de sucesso se o formulário for submetido com sucesso.
			Como é necessário incluir um link para a postagem no email, deve obtar o path absoluto da postagem usando o método get_absolute_ur()
			Usamos esse path como entrada para request.build_absolute_url a fim de compor um url completo, incluindo o esquema http e o nome do host.
			Definimos o assunto e o corpo da mensagem do email usando os dados limpos do formulário validado e enviamos o email para o endereço contido em 'to' do formulário.

		Agora que a view está completa, acrescente um novo padrão de url para ela. Em urls.py da aplicação blog, adicione o padrão de url post_share
			urlpatterns = [
				# views de postagens
				# path('', views.post_list, name='post_list'),
				path('', views.PostListView.as_view() , name='post_list'),
				path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
				path('<int:post_id>/share/', views.post_share, name='post_share'),
			]

	- Renderizando formulários em templates
		Depois de criar o formulário, criar a view e adicionar o padrão de url, resta criar o template para essa view.
		Crie o arquivo share.html no diretório blog/temlpates/blog/post/
			{% extends 'blog/base.html' %}
				{% block title %} Share a post {% endblock %}
				{% block content %}
					{% if sent %}
						<h1> Emails successfully sent. </h1>
						<p>
							"{{ post.title }}" was successfully sent to {{ form.cleaned_data.to }}
						</p>
					{% else %}
						<h1> Share "{{ post.title }}" by email. </h1>
						<form method="post">
							{{ form.as_p }}
							{% csrf_token %}
							<input type ="submit" value="Send email.">
						</form>
					{% endif %}
				{% endblock %}
		Esse é o template para exibir o formulário ou uma mensagem de sucesso quando o email é enviado.
		Criamos o elemento do formulário HTML informando que ele deve ser submetido com o método POST. Ex.: <form method="post">
		Depois, incluímos a instância do formulário, pedimos que django renderize seus camplos em elementos html <p> de parágrafos com o método as_p.
		Também podemos renderizar o formulário como uma lista não ordenada as_ul, ou como uma tabela html com as_table.
		Se quiser renderizar cada campo, poderá iterar poi eles, em vez de usar {{ form.as_p }}.
		Código:
				{% for field in form %}
					<div>
						{{ field.errors }}
						{{ field.label_tag }} {{ field }}
					</div>
				{% endfor %}

		Obs. A tag de template {% csrf_token %} adiciona um campo oculto com um token gerado de modo automático
			 a fim de evitar ataques de CSRF(cross-site-request-form ou falsificação de requisições entre sites.)
			 Esses ataques são compostos de um site ou programa mal-intencionados que executam uma ação indesejada para um usuário de seu site.
			A tag anterior gera um campo oculto do tipo abaixo:
				<input type='hidden' name='csrfmiddlewaretoken' value='26Jjk...'>
		Obs. Por padrão, django verifica a presença do token CSRF em todas as requisições POST. Não se esqueça de incluir essa tag em todos os formulários submetidos com POST.
		Abra o template detail.html e adicione o link a seguir para o url de compartilhamento de postagem, depois da variável {{ post.body|linebreaks }}:
			<p>
				<a href="{% url "blog:post_share" post.id %}">
				Share this post.
				</a>
			</p>

		Código:
			{% extends "blog/base.html" %}

			{% block title %}{{ post.title }} {% endblock %}
			{% block content %}
			<h1> {{ post.title }} </h1>
			<p class="date">
				Published {{ post.publish }} por {{ post.author }}
			</p>
			{{ post.body|linebreaks }}
			<p>
				<a href="{% url "blog:post_share" post.id %}">
					Share this post.
				</a>
			</p>
			{% endblock %}

		Obs.: Você está criando o url dinamicamente com a tag de template {% url %} disponibilizada pod django.
			  Estamos usando o namespace chamado blog e o url chamado post_share, e passando o ID da postagem como parâmetro para compor o url absoluto.

		Inicie o servidor (manage.py runserver ) e acesse http://127.0.0.1:8000/blog/
		Clique no título de uma postagem para visualizar a sua página de detalhes. Abaixo do corpo da mensagem, verá o link que acabamos de acrescentar.
		Clique me share this post, e verá a página com o formulário para compartilhar essa postgem por email.

		Seu formulário para compartilhar postagens por email está completo.
		A seguir, vamos criar um sistema de comentários para o blog.

		- Criando um sistema de comentários    11/11/2021
				Para os usuários comentarem as postagens.
				Será necessário:
					1. Criar um modelo para salvar os comentários
					2. Criar um formulário para submeter comentários e validar os dados de entrada.
					3. Adicionar uma view que processe o formulário e salve um novo comentário no banco de dados.
					4. Modificar o template de detalhes da postagem, para que exiba a lista de comentários e o formulário para adicionar um novo comentário.

				1. Criando um modelo
					Edite o arquivo models.py da aplicação blog.
					Código:
						class Comment(models.Model):
							post 	= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
							name 	= models.CharField(max_lengh=80)
							email 	= models.EmailField()
							body 	= models.TextField()
							created = models.DateTimeField(auto_now_add=True)
							updated = models.DateTimeField(auto_now=True)
							active	= models.BooleanField(default=True)

						class Meta:
							ordering = ('created',)

						def __str__(self):
							return f'Comentado por {self.name} no {self.post}'

					O modelo Comment, possui uma ForeignKey para associar um comentário a uma única postagem. (Relacionamento Muitos-para-Um).
					Cada comentário será feito para uma única postagem, e cada postagem pode ter vários comentários.
					O atributo related_name permite nomear o atributo utilizado no relacionamento entre o objeto relacionado de volta para esse objeto.
						Com ele, podemos obter a postaggem de um objeto comentário usando comment.post e obter todos os comentários de uma postagem com post.comments.all()
						Se ele não for definido, django usará o nome do modelo com letras minúsculas, seguido de _set (ex: comment_set)
							para nomear o relacionamento entre o objeto relacionado e o objeto modelo no qual esse relacionamento foi definido.

					O campo booleano active, serve para desativar manualmente comentários inadequados.
					O campo created, é usado para ordenar os comentários em ordem cronológica, por padrão.
					Obs.: O novo modelo Comment ainda não está sincronizado com o banco de dados.
						  Execute o comando para gerar uma nova migração que reflita a criação do novo modelo.
						  Código:
						    # Criará o modelo Comment
							python manage.py makemigrations blog

							# Criar o esquema relacionado no banco de dados e aplicar as migrações existentes.
							python manage.py migrate

					Em seguida, deve adicionar o novo modelo no site de administração para gerenciar os comentários por meio de uma interface simples.
					Edite o admin.py da aplicação blog, importe o modelo Comment e acrescente a classe CommentAdmin,
					Código:
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

				2. Criando formulários a partir de modelos
					Para permitir que os usuários façam comentários nas postagens do blog.
					Obs. Django inclui 2 classes-base para criar formulários: Form e ModelForm.
						Usamos Form para permitir que os usuários compartilhassem postagens por email.
						Agora, vamos usar ModelForm para criar um formulário dinamicamente, a partir do modelo Comment.
						Edite forms.py da aplicação blog, adicione as linhas abaixo.
							from .models import Comment
							class CommentForm(forms.ModelForm):
								class Meta:
									model = Comment
									fields = ('name','email','body')  # São os únicos campos que os usuários poderão preencher.

						Para criar um formulário a partir de um modelo, basta informar qual modelo deve ser usado para criar o formulário na classe Meta do formulário.
							Django faz uma instrospecção do modelo e cria o formulário dinamicamente para você.
						Cada tipo de campo do modelo tem um tipo de campo default correspondente no formulário.
						O modo como definimos os campos do modelo é levado em consideração na validação do formulário.
						Podemos informar explicitamente ao framework, quais campos queremos que sejam incluídos no formulário, através da lista fields.
						Ou podemos excluir os campos, atravpes de uma lista de campos exclude.


				3. Lidando com ModelForms nas views ( Adicionar uma view que processe o formulário e salve um novo comentário no banco de dados.)
					Usaremos a view de detalhes da postagem para instanciar o formulário e processá-lo, a fim de manter a simplicidade.
					Edite views.py, adicione as exceções para o modelo Comment e o formulário CommentForm, e modifique a view post_detail.
						def post_detail(request, year, month, day, post):
							post = get_object_or_404(Post, slug=post,
													 status='published',
													 publish__year=year,
													 publish__month=month,
													 publish__day=day)
							# Lista dos comentários ativos para esta postagem
							comments = post.comments.filter(active=True)
							new_comment = None

							if request.method=='POST':
								# Um comentário foi postado
								comment_form = CommentForm(data=request.POST)
								if comment_form.is_valid():
									# Cria o objeto Comment, mas ainda não salva no banco de dados.
									new_comment = comment_form.save(commit=False)
									# Atribui a postagem atual ao comentário.
									new_comment.post = post
									# Salva o comentário no banco de dados.
									new_comment.save()
								else:
									comment_form = CommentForm()
							return render(request,
										  'blog/post/detail.html',
										  {'post' : post,
										   'comments': comments,
										   'new_comment': new_comment,
										   'comment_form': comment_form})

					Usamos post_detail para exibir a postagem e seus comentários,
						adicionamos um QuerySet para obter todos os comentários ativos para essa postagem. (ex: comments = post.comments.filter(active=True))
					Criamos a partir de Post ao invés de Comment, pois aproveitamos que o post possui objetos comment relacionados a ele.
					Usamos o gerenciador de objetos comments no atributo related_name do relacionamento, no modelo comment.
					Usamos a mesma view para permitir que usuários adicionem um novo comentário.
					A variável new_comment foi inicializada com o valor none, mas será usada quando um novo comentário for criado.
					Criamos uma instância do formulário com comment_form = CommentForm(), se a view for chamada com uma requisição GET.
					Se a requisição for feita com POST, instanciamos o formulário usando os dados submetidos e os validamos com o método is_valid().
					Se o formulário for inválido, renderizamos o template com os erros de validação.
					Se o formulário for válido, serão executadas as seguintes ações:
						1. Criamos um objeto Comment chamando o método save() do formulário e o atribuímos à variável new_comment. (Ex: new_comment = comment_form.save(commit=False))
							Obs. O método save() cria uma instância do modelo ao qual o formulário está ligado e a salva no banco de dados,
							     mas se chamar com commit=False, a instância do modelo será criada, mas não será salva ainda no banco de dados. Pois, modificaremos o objeto antes de salvá-lo.
								 save() está disponível apenas para ModelForm, pois está ligada a um modelo. save() não está disponível para Form.
						2. Atribuímos a postagem atual ao comentário que acabamos de criar. (ex: new_comment.post = post )
							Ao fazer isso, especificamos que o novo comentário pertence a essa postagem.
						3. Por fim, salvamos o novo comentário no banco de dados chamando o método save().  (ex: new_comment.save())
					Sua view agora, está pronta para exibir e processar novos comentários.

			4. Adicionando comentários no template de detalhes da postagem
			(Modificar o template de detalhes da postagem, para que exiba a lista de comentários e o formulário para adicionar um novo comentário.)
				Editar o template post/detail.html para que ele faça:
					- exiba o número total de comentários para uma postagem
					- exiba a lista de comentários
					- exiba um formulário para que os usuários possam acrescentar um novo comentário
				Código:
					{% extends "blog/base.html" %}

					{% block title %} {{ post.title }} {% endblock %}
					{% block content %}
						<h1> {{ post.title }} </h1>
						<p class="date">
							Published {{ post.publish }} por {{ post.author }}
						</p>
						{{ post.body|linebreaks }}
						<p>
							<a href="{% url "blog:post_share" post.id %}">
								Share this post.
							</a>
						</p>

						{% with comments.count as total_comments %}
							<h2>
								{{ total_comments }} comment {{ total_comments|pluralize }}
							</h2>
						{% endwith %}

					{% endblock %}

				Estamos usando o ORM de django no template, executando o QuerySet comments.count()
				Observe que a linguagem de template de django não utiliza parênteses para chamar os métodos.
				A tag {% with %} permite que você atribua um valor a uma nova variável que estará disponível para ser usada até a tag {%endwith%}
				A tag {% with %} é conveniente para evitar que o banco de dados ou que métodos custosos sejam acessados várias vezes.
				O filtro de template pluralize, exibe um sufixo de plural na palavra 'comment', dependendo do valor de total_comments,
				O filtro de template pluralize, devolverá uma string com a letra 's' se o valor for diferente de 1. (ex: 0 comments, 1  comment, 2 comments)

				Agora, vamos incluir a lista de comentários.
				Edite post/detail.html
					{% extends "blog/base.html" %}

					{% block title %} {{ post.title }} {% endblock %}
					{% block content %}
						<h1> {{ post.title }} </h1>
						<p class="date">
							Published {{ post.publish }} por {{ post.author }}
						</p>
						{{ post.body|linebreaks }}
						<p>
							<a href="{% url "blog:post_share" post.id %}">
								Share this post.
							</a>
						</p>

						{% with comments.count as total_comments %}
							<h2>
								{{ total_comments }} comment {{ total_comments|pluralize }}
							</h2>
						{% endwith %}

						{% for comment in comments %}
							<div class="comment">
								<p class="info">
									Comment {{ forloop.counter }} by {{ comment.name }}
									{{ comment.created }}
								</p>
								{{ comment.body|linebreaks }}
							</div>
							{% empty %}
							<p> Ainda não há comentários. </p>
						{% endfor %}

					{% endblock %}

				Usamos a tag template {% for %} para percorrer os comentários em um laço.
				Se a lista comments estiver vazia, exibimos uma mensagem default.
				Enumeramos os comentários com a variável {{ forloop.counter }}, que contém o contador do laço de cada iteração.
				Depois, exibimos o nome do usuário que postou o comentário, a data e o corpo do comentário.

				Por fim, devemos renderizar o formulário ou exibir uma mensagem de sucesso se ele foi submetido com sucesso.
				Adicione as linhas:
						{% if new_comment %}
							<h2> Seu comentário foi adicionado. </h2>
						{% else %}
							<h2> Adicione um novo comentário. </h2>
							<form method="post">
								{{ comment_form.as_p }}
								{% csrf_token %}
								<p> <input type="submit" value="Adicione comentário"> </p>
							</form>
						{% endif %}
				Se o objeto new_comment existir, exibirá uma mensagem informando que houve sucesso, pois o comentário foi devidamente criado.
				Se não, renderizamos o formulário com um elemento de parágrafo <p> para cada campo e incluímos o token csrf necessário para requisição post.
				Acesse http://127.0.0.1:8080/blog e clique no título de uma postagem para ver a sua página de detalhes.
				Acesse http://127.0.0.1:8080/admin/blog/comment e desative algum comentário. Para verificar que não será mais exibido e nem contabilizado.

			- Adicionando a funcionalidade de marcação com tags 
