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

		- Criando um sistema de comentários
