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
		Usamos o atalho get_object_or_404 para obter a postagem com bvase no id e garantimos que a postagem obtida tenha um status igual a published
		Usamos a mesma view para exibir o formulário inicial e para processar os dados submetidos.
			Diferencia se o form foi submetido com base no método de request e submetemos o form com POST
			Se recebemos uma requisição GET, o form vazio será exibido,
			se recebemos uma requisição POST, o form foi submetido e deverá ser processado.
		Obs. Se o formulário for válido, obtemos os dados validados acessando form.cleaned_data. É um dicionário dos campos do formulário e seus valores.

	- Enviando emails com django
