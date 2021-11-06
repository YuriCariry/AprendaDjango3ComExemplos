Tentando aprender Django.
Livro Aprenda Django3 com Exemplos.

Objetivos:
1. Criando uma aplicação de Blog

Cap1. Blog
- Instalação do Django
- Criação e configuração de um projeto Django
- Criação de uma aplicação Django
- Design de Modelos e geração de migrações para os modelos
- Criação de um site de administração para os modelos
- QuerySets e gerenciadores (managers)
- Criação de views, templates e urls
- Adição de paginação e views com lista
- Uso de views baseadas em classe de Django

Detalhes:
- Instalação do Django
  - Download e instalação do Python: https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    - obs. a versão 3 contém um BD SQLite, não precisa instalar outro.
  - Criação de um ambiente python isolado (permite utilizar versões diferentes de pacotes em projetos distintos.)
      python -m venv my_env
      C:\Users\yuric\workspace\my_env\Scripts\activate.bat
  - Instalando Django com pip (ficará instalado na pasta site-packages/ do ambiente python)
      pip install "Django=3.0.*"
      obs. para testar:
        cmd python.exe
        import django
        django.get_version()
        (retornará: '3.0.4')

- Criação e configuração de um projeto Django
  - Comando para criar estrutura de arquivos inicial para um projeto.
      django-admin startproject mysite
    Estrutura de arquivos:
      mysite/
        manage.py (é um utilitário utilizado para interagir com o projeto.)
        mysite/   (é o diretório do seu projeto.)
          __init__.py (é um arquivo vazio, que indica ao python para tratar mysite como um projeto python.)
          wsgi.py     (é a configuração para executar o projeto como aplicação WSGI(Interface de Porta de Entrada para Servidor Web.) )
          asgi.py     (é a configuração para executar o projeto como aplicação ASGI(é o padrão emergente de python para aplicações e servidores web assíncronos.))
          settings.py (contém parâmetros e a configuração de seu projeto e informa os parâmetros iniciais default. Contém a configuração para usar o banco SQLite e uma lista de INSTALLED_APPS(aplicações padrão django)).
          urls.py     (é o local onde estão os padrões de URL. cada url definido é mapeado para uma view.)

  - Para concluir a criação do projeto, é necessário criar as tabelas associadas aos modelos das aplicações 'INSTALLED_APPS'.
      models.py (é onde os modelos de dados são definidos, cada modelo é mapeado para uma tabela do banco de dados.)
      Django tem um sistema de migração que cuida disso. (cria esse arquivo models.py)
      Abra o shell e execute:
        cd mysite
        python manage.py migrate

  - Executando o servidor de desenvolvimento. (servidor web leve incluído no django. obs: em caso de adição de arquivos no projeto, é necessário reiniciar o servidor.)
      python manage.py runserver
        Site disponível em: http://127.0.0.1:8080
        obs. o servidor pode ser executado em um host e porta personalizados.
          python manage.py runserver 127.0.0.1:8080 \--settings=mysite.settings
        obs. Esse servidor é apenas para desenvolvimento, para produção deve-se executar como uma aplicação wsgi usando um servidor web como o apache ou como uma aplicação asgi usango um servidor como o Uvicorn ou Daphne.
  - Configurações do projeto
    settings.py (https://docs.djangoproject.com/en/3.0/ref/settings)
      - DEBUG ativa ou desativa o modo de depuração do projeto.
        Se estiver como true, exibirá páginas de erro detalhadas quando ocorrer exceções.
        Ao passar para o ambiente de produção, deve-se passar para False. por questões de segurança.
      - ALLOWED_HOSTS não se aplica caso debug=true ou quando os testes forem executados. quando o site for para produção, deve-se definir o domínio/host nesse parâmetro, para permitir que ele atenda ao site django.
      - INSTALLED_APPS diz quais aplicações ativas no site, por padrão:
          admin (um site de administração)
          auth  (um framework de autenticação)
          contenttypes (um framework para lidar com tipos de conteúdo.)
          sessions (um framework de sessão)
          messages (um framework de mensagens)
          staticfiles  (um framework para gerenciar arquivos estáticos)
      - MIDDLEWARE é uma lista com os middleware a serem executados
      - ROOT_URLCONF informa o módulo python no qual os padrões de url raiz de sua aplicação estão definidos.
      - DATABASES é um dicionário que contém as configurações de todos os bds a serem usados no projeto.
      - LANGUAGE_CODE define o código da linguagem default desse site django.
      - USE_TZ ativa/desativa suporte a fusos horários.

      Projetos x Aplicações:
        - Projeto é uma instalação django com algumas configurações.
        - Aplicação:
                    - é um grupo de modelos, views, templates e urls.
                    - interagem com o framework para oferecer funcionalidades específicas e podem ser reutilizadas em outros projetos.
        - Um projeto é o seu site, que contém várias aplicações como blog, wiki ou fórum.

- Criação de uma aplicação Django
  No diretório raiz do projeto, execute:
    python manage.py startapp blog
  Esse comando cria a estrutura básica da aplicação:
    blog/
      _init_.py
      admin.py  (é o local onde você registra seus modelos, a fim de incluir no site(opcional) de administração de Django.)
      apps.py   (inclui a configuração principal da aplicação blog.)
      migration/ (conterá as migrações de banco de dados para sua aplicação.Permite que o django monitore as mudanças nos modelos e faça a sincronização com o banco de dados.)
        _init_.py
      models.py (inclui os modelos de dados da aplicação, toda aplicação tem que ter esse arquivo, mas pode estar vazio.)
      testes.py (é o local para adicionar os testes para a aplicação.)
      views.py (a lógica da aplicação deve estar nesse arquivo. cada view recebe uma requisição http, processa essa requisição e devolve uma resposta.)

- Design de Modelos(esquema de dados) e geração de migrações para os modelos
  1. Definir os modelos de dados.
    Os modelos são classes python, subclasses de django.db.model.Model
    Cada atributo representa um campo do banco de dados.
    Django criará uma tabela para cada modelo definido no models.py
    Ao criar um modelo, django criará uma api para consultar os objetos no banco de dados.
    Exemplo: Arquivo models.py da aplicação blog. (é o modelo de dados para postagens do blog.)
    obs.: campo slug:
                    - tem o propósito de ser utilizado para compor urls elegantes
                    - slug é um pequeno rótulo, contém apenas letras, números, _ ou hífens.
                    - convenientes para SEO (otimização de pesquisa do google)
    tipos de campos, estão em https://docs.djangoproject.com/en/3.0/models/fields
  2. Ativando a aplicação
      Para que o django mantenha o controle da aplicação e seja capaz de criar as tabelas de banco de dados para seus modelos.
      Abra o arquivo settings.py e acrescente no parâmetro INSTALLED_APPS:
        blog.apps.BlogConfig
        (é a configuração de sua aplicação.)
  3. Criando e aplicando Migrações
    Primeiro, deve-se criar uma migração inicial para o seu modelo Post.
    No diretório raiz do projeto execute:
      python manage.py makemigrations blog
      (criará o arquivo 0001_initial_py no diretório migrations da aplicação blog.)
    Uma migração especifica as dependências de outras migrações e as operações a serem executadas no banco de dados para sincronizá-lo com as alterações do modelo.

    Para analizar o código sql que o django e xecutará no bd a fim de criar a tabela para seu modelo.
    Execute (não é necessário, apenas para entendimento.):
      python manage.py sqlmigrate blog 0001
    obs. django gera os nomes das tabelas combinando o nome da aplicação e o nome do modelo. Ex: blog_post (é possível alterar, na classe Meta do modelo, usando o atributo db_table)
    obs. django cria uma chave primária automatimente para cada modelo, mas pode sobrescrever especificando primary_key=true emm um dos campos do modelo.

    Para sincronizar o banco de dados com o novo modelo, executar o comando abaixo para aplicar as migrações existentes.
      python manage.py migrate

    obs. se editar models.py e adicionar, remover ou modificar os campos dos modelos existentes, ou se adicionar um novo modelo, será necessário criar outra migração através do comando:
      python manage.py makemigrations blog
    E, em seguida, deve aplicá-la com o comando migrate.
      python manage.py migrate

- Criação de um site de administração para os modelos
  Para gerenciar as postagens de blog.
  django disponibiliza uma interface de administração pronta.
  é possível configurar o modo como queremos que osmodelos sejam exibidos.
    django.contrib.admin (já está contida em INSTALLED_APPS).

    Criando um superusuário: (é necessário criar um usuário para gerenciar o site de administração)
      python manage.py createsuperuser
        username:admin
        email: admin@admin.comm
        password: **
        password(again): **
   Exemplo:
    (my_env) C:\Users\yuric\workspace\my_env\mysite>python manage.py createsuperuser
  Site de administração django (após iniciar o servidor:   python manage.py runserver)
    http://127.0.0.1:8000/admin
  Após login (admin admin), serão exibidos: groups e users (fazem parte do framework de autenticação(django.contrib.auth)).
  Adicionando modelos no site de administração:
    - Adicionar os modelos do blog no site de administração.
      Altere o arquivo admin.py da aplicação blog.
        from django.contrib import admin
        from .models import Post

  Personalizando o modo como os modelos são exibidos.
    Editar o arquivo admin.py da aplicação blog
    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
      list_display = ('title','slug','author','publish','status')
      list_filter = ('status','created','publish','author')
      search_fields = ('title','body')
      prepopulated_fields = {'slug': ('title',)}
      raw_id_fields = ('author',)
      date_hierarchy ='publish'
      ordering = ('status','publish')


- QuerySets e gerenciadores (managers) - 03/11/2021
	É hora de aprender a acessar informações no banco de dados e interagir com ele.
	Django possui uma API, ORM (Mapeador Objeto-Relacional); pode trabalhar com vários bds ao mesmo tempo, pode programar roteadores de bds para criar esquemas de roteamento personalizados.
	Obs. Pode definir o banco de dados para o projeto com o parâmetro DATABASES no settings.py do projeto.
	Após criar os modelos de dados, django disponibilizará automaticamente uma API para interagir com eles. https://docs.djangoproject.com/en/3.0/ref/models/
	O ORM de django se baseia em QuerySets.
		- Um QuerySet é um conjunto de queries(consultas) para ler objetos do banco de dados.
		- Você pode aplicar filtros nos QuerySets para restringir os resultados da consulta com base em determinados parâmetros.
	Criando objetos
		python manage.py shell
		from django.contrib.auth.models import User
		from blog.models import Post
		user = User.objects.get(username='admin')
		post = Post(title='Another post',
					slug='another-post',
					body='body post',
					author=user)
					post.save()
		- A ação anterior executa uma instrução SQL INSERT nos bastidores.
		- Vimos como criar um objeto na memória antes e fazer sua persistência no banco de dados.

		- Abaixo veremos como criar o objeto e fazer a persistência no banco de dados em uma única operação usando o método create().
		python manage.py shell
		from django.contrib.auth.models import User
		from blog.models import Post
		user = User.objects.get(username='admin')
		Post.objects.create(title='one more post',slug='one-more-post',body='post body.',author=user)


	Atualizando objetos
		- Modifique o título da postagem para algo diferente e salve o objeto novamente.
			post.title = 'New title'
			post.save()
		- Dessa vez, o método save() executa uma instrução SQL UPDATE.

	Lendo objetos
		- Para ler um único objeto do banco de dados, usamos o método get();
		- Acessamos esse método usando Post.objects.get()
		- Todo modelo django tem pelo menos um gerenciador(manager), e o gerenciador default se chama objects.
		- Um objeto QuerySet é obtido usando o gerenciador de seu modelo.
		- Para ler todos os objetos de uma tabela, basta usar o método all() no gerenciador de objetos. Ex.:
			all_posts = Post.objects.all()
		- É assim que criamos um QuerySet que devolve todos os objetos do banco de dados.
		- Obs. Esse QuerySet ainda não foi executado.
		- Os QuerySets de django são preguiçosos(lazy), o que significa que serão avaliados apenas qunado forem forçados a sê-lo.
		- Esse comportamento faz com que os QuerySets sejam muito eficientes.
		- Obs. Se, ao invés de atribuir o QuerySet a uma variável, você escrevê-lo diretamente no shell python,
			   a instrução QuerySet será executada porque você forçará a sua execução para que os resultados sejam exibidos. Ex.:
				all_posts

	Usando o método filter()
		- Para filtrar um QuerySet
		Ex: Obter todas as postagens publicadas em 2021.
			Post.objects.filter(publish__year=2021)
		Ex: Obter todas as postagens publicadas em 2021 do autor 'admin'.
			Post.objects.filter(publish__year=2021, author__username='admin')
		Esse comando equivale a criar o mesmo QuerySet encadeando vários filtros.
			Post.objects.filter(publish__year=2021) \
						.filter(author__username='admin')
		Obs. Queries com métodos de pesquisa de campos são criados usando dois undescores (ex: publish__year),
			mas a mesma anotação é usada para acessar campos de modelos relacionados (ex: author__username).

	Usando exclude()
		- Podemos excluir determinados resultados do QuerySet usando o método exclude() do gerenciador.
		- Ex: Obter todas as postagens publicadas em 2021 cujos títulos não começem com Why.
			Post.objects.filter(publish__year=2021) \
						.exclude(title__startswith='Why')

	Usando order_by()
		- Podemos ordenar o resultado com base em campos distintos usando o método order_by() do gerenciador.
		- Ex: Obter todos os objetos ordenados de acordo com title.
			Post.objects.order_by('title')
		- Na ordem decrescente, ficaria:
			Post.objects.order_by('-title')

	Removendo objetos
		- Pode fazer usando a instância do objeto, usando o método delete(). ex:
			post = Post.objects.get(id=1)
			post.delete()
		- obs: a remoção do objeto causará a remoção de quaisquer relacionamentos dependentes para objetos ForeignKey com on_delete definido como CASCADE.

	Quando os Queries são avaliados
		- Criar um QuerySet não envolverá nenhuma atividade no banco de dados até que ele seja avaliado.
		- Os QuerySets em geral devolvem outro QuerySet não avaliado.
		- Você pode concatenar quantos filtros quiser em um QuerySet, e o banco de dados não será acessado até que o QuerySet seja avaliado.
		- Quando um QuerySet é avaliado, ele é traduzido para uma query SQL no banco de dados.
		- Os QuerySets são avaliados nos seguintes casos:
			- na primeira vez que você iterar por eles;
			- ao fatiá-los, por exemplo, usando Post.objects.all()[:3] ;
			- ao serializá-los ou colocá-los em cache;
			- ao chamar repr() ou len() neles;
			- ao chamar list() neles, de modo explícito;
			- ao testá-los em uma instrução, ex: bool(), or, and ou if.

	Criando gerenciadores de modelo
		- Podemos definir gerenciadores personalizados para os modelos.
		- Ex: Gerenciador personalizado para obter todas as postagens cujo status seja 'published'.
		- Há duas formas:
			- acrescentar métodos extras em um gerenciador existente;
				- fornece uma API de QuerySet.
				- ex: Post.objects.my_manager()
			- criar outro gerenciador modificado o QuerySet inicial devolvido pelo gerenciador default.
				- oferece um Post.my_manager.all()
		- O gerenciador permitirá obter as postagens usando Post.published.all().

		- Modifique models.py da aplicação blog de modo a acrescentar um gerenciador personalizado.

			class PublishedManager(models.Manager):
				def get_queryset(self):
					return super(PublishedManager,
								self).get_queryset()\
								.filter(status='published')
			...
			 # ...
			objects = models.Manager() # gerenciador default
			published = PublishedManager() # gerenciador personalizado
			...
		- Depois de alterar, deve reiniciar o servidor de desenvolvimento:
			python manage.py shell
		- Agora, você pode importar o modelo Post e obter todas as postagens publicadas cujo título começe com 'Who', executando o QuerySet a seguir:
			python manage.py shell
			from blog.models import Post
			Post.published.filter(title__startswith='test')
		-Obs.: Para testar, o servidor deve estar rodando, e outro cmd deve abrir o shell do python.

- Criação de views, templates e urls
    - Implementando as views de lista e de Detalhes
      - Uma view é uma função python que recebe uma requisição web e devolve uma resposta.
      - Toda a lógica para devolver a resposta desejada estará na view.
      1. Criar as views da aplicação.
      2. Definir um padrão de URL para cada view.
      3. Criar templates html para renderizar os dados gerados pelas views.
          - cada view renderizará um template, passando variáveis para ele,
            e devolverá uma resposta http com uma saída renderizada.

    - 1. Criando as views de lista e de detalhes
      - altere views.py da aplicação blog (view para exibir uma lista de postagens)
          from django.shortcuts import render, get_object_or_404
          from .models import Port

          # Create your views here.
          # Uma view é uma função python que recebe uma requisição web e devolve uma resposta.
          def post_list(request):
              post = Post.published.all()
              return render(request,
                            'blog/post/list.html',
                            {'posts':posts})
      - from django.shortcuts import render, get_object_or_404
      from .models import Port

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
          post = Post.published.all()
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

    - 2. Adicionando padrões de URL às suas views  (2. Definir um padrão de URL para cada view.)
      - Os padrões de URL permitem mapear URLs às views.
      - É composto de um padrão de string, uma view e, opcionalmente, um nome que permite nomear a URL.
      - Django:
          - percorre cada um dos padrões de url e para no primeiro que corresponder ao url requisitado.
          - importa a view associada ao padrão de url identificado
          - executa a view, passando uma instância da classe HttpRequest e os argumentos nomeados ou posicionais.
      - criar arquivo urls.py na aplicação blog e acrescente:
          from django.urls import path
          from . import views

          # Definimos o namespace da aplicação.
          # Permite organizar as urls por aplicação e usar o nome ao referenciá-los.
          app_name = blog

          # Os padrões de URL permitem mapear URLs às views.
          # É composto de um padrão de string, uma view e, opcionalmente, um nome que permite nomear a URL.
          # Definimos dois padrões.
          # O primeiro padrão de url não recebe nenhum argumento e é mapeado para a view post_list.
          # O segundo padrão aceita 4 argumentos e é mapeado para a view post_detail.
          # Sinais de <> para capturar os valores da url.
          #   O padrão é string, por isso utilizamos conversores de path. ex: <int:year>
          #   Exemplos de conversores de path. https://docs.djangoproject.com/en/3.0/topics/http/urls/#path-converters
          # Se o uso do path e dos conversores não for suficiente,
          #   utilizamos re_path() para definir padrões complexos de url, usando expressões regulares de python.
          # Obs. Criar um arquivo urls.py para cada aplicação é a melhor maneira de tornar suas aplicações reutilizáveis para outros projetos.
          urlpatterns = [
              # views de postagens
              path('',views.post_list, name='post_list'),
              path('<int:year>/<int:month>/<int:day>/<slug:post>/',
                    views.post_detail, name='post_detail'),
          ]

      - Incluir os padrões de url da aplicação blog nos padrões principais de url do projeto.
        Editar arquivo urls.py do diretório da aplicação. ex: mysite
          from django.contrib import admin
          from django.urls import path, include
          urlpatterns = [
              path('admin/', admin.site.urls),
              path('blog/',include('blogs.urls', namespace='blog')),
          ]

      - URLs canônicos para os modelos
        - URL canônico é um url preferencial para um recurso.
          É possível que haja diferentes páginas em seu site para exibir as postagens,
          mas haverá um único url que será usado como url principal para uma postagem do blog.
        - Pela convenção django, um método get_absolute_url() é adicionado no modelo,
            o qual devolve o URL canônico para o objeto.
            - o url post_detail pode ser usado para criar o url canônico dos objetos post.
              - nesse método, usaremos o método reverse(), que permite criar urls com base no nome
              - e aceita parâmetros opcionais.
        - Edite o arquivo models.py da aplicação blog. acrescentando:
        # Você utilizará o get_absolute_url() em seus templates para fazer a ligação com postagens específicas.
          from django.urls import reverse
          def get_absolute_url(self):
              return reverse('blog:post_detail',
                              args:[self.publish.year,
                                    self.publish.month,
                                    self.publish.day,
                                    self.slug
                              ])

   -3. Criando templates para suas views (3. Criar templates html para renderizar os dados gerados pelas views.)
      - Os padrões de url mapeiam urls às views, e as views decidem quais dados são devolvidos ao usuário.
      - Os templates definem como os dados são exibidos, em geral (em html, junto com a linguagem de template de django).
      - Adicionar templates a fim de exibir as postagens aos usuários de uma maneira agradável.
        - crie os diretórios e arquivos a seguir na aplicação blog.
          templates/
            blog/
              base.html        # terá a estrutura html principal do site e dividirá o conteúdo em uma área principal e uma caixa lateral.
              post/
                list.html     # herdará da base.html para renderizar as views da lista das postagens do blog.
                detail.html   # herdará da base.html para renderizar as views de detalhe da postagem do blog.

        - Django tem uma linguagem de template eficaz que permite especificar como os dados serão exibidos.
          - É baseada em tags de template, variáveis de template e filtros de template.
            - tags de template       : controlam a renderização do template. ex: {% tag %}
            - variáveis de template  : são substituídas por valores quando o temlpate é renderizado. ex: {(variable)}
            - filtros de template    : permitem modificar variáveis a serem exibidas. ex: {{ variable|filter }}
        - base.html
              {% load static %}
              <!DOCTYPE html>
              <html lang="en" dir="ltr">
                <head>
                  <meta charset="utf-8">
                  <title>{% block title%} {% endblock%}</title>
                  <link href="{% static "css/blog.css" %}" rel="stylesheet">
                </head>
                <body>
                  <div id="content">
                    {% block content %}
                    {% endblock %}
                  </div>
                  <div id="sidebar">
                      <h2>Meu blog</h2>
                      <p>Esse é o meu blog. </p>
                  </div>
                </body>
              </html>

        - {% load static %}
            - diz ao django para carregar as tags de template static disponibilizadas pela aplicação django.contrib.staticfiles, está no parâmetro INSTALLED_APPS.
            - depois, você poderá usar a tag de template {% static %} em qualquer ponto desse template.
            - pode incluir arquivos estáticos, ex. blog.css
              - https://github.com/PacktPublishing/Django-3-by-Example/tree/master/Chapter01/mysite/blog/static
        - Há duas tags {% block %}:
            - diz ao django que você quer definir um bloco nessa área.
            - templates que herdarem desse template poderão preencher os blocos com algum conteúdo.
            - definimos um bloco chamado title e outro chamado content.

        - editar post/list.html
              {% extends "blog/base.html" %}

              {% block title %}Meu blog.{% endblock %}
              {%block content %}
                <h1>Meu Blog.</h1>
                {% for post in posts %}
                  <h2>
                    <a href="{{ post.get_absolute_url }}">
                      {{ post.title }}
                    </a>
                  </h2>
                  <p class="date">
                      Published {{ post.publish }} por {{ post.author }}
                  </p>
                  {{ post.body|truncatewords:30|linebreaks }}
                {% endfor %}
              {% endblock %}

        - editar post/detail.html
              {% extends "blog/base.html" %}

              {% block title %}{% post.title %} {% endblock %}
              {%block content %}
                <h1> {% post.title %} </h1>
                <p class="date">
                      Published {{ post.publish }} por {{ post.author }}
                </p>
                  {{ post.body|linebreaks }}
              {% endblock %}



- Adição de paginação e views com lista - 05/11/2021
	Ao adicionar conteúdo no blog, centenas de postagens serão armazenadas no banco de dados.
	Em vez de exibir todas em uma única página, pode dividiar a lista de postagens em várias páginas.
	Isso pode ser feito com Paginação.
	Pode definir o número de postagens por página
	e obter as postagens que correspondam a página solicitada pelo usuário.
	Django tem uma classe de paginação embutida, que permite gerenciar facilmente os dados nas páginas.
	Edite o views.py da aplicação blog,
		de modo a importar as classes de paginação de django;
		e edite a view post_list.
	Código:
		from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
		...
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
	Como a paginação funciona:
		1. Instanciamos a classe Paginator com a quantidade de objetos que queremos exibir em cada página.
		2. Lemos o parâmetro page de GET, que informa o número da página atual.
		3. Acessamos os objetos da página desejada chamado o método page() de paginator.
		4. Passamos o número da página e os objetos obtidos para o template.

	Agora, devemos criar um template para exibir o paginator,
	de modo que ele possa ser incluído em qualquer template que utilize paginação.
	Crie o arquivo pagination.html e salve em templates/
	Código:
			<div class='pagination'>
				<span class='step-links'>
					{% if page.has_previous %}
						<a href="?page={{ page.previous_page_number }}"> Previous </a>
					{% endif %}
					<span class='current'>
						Page {{ page.number }} of {{ page.paginator.num_pages }}.
					</span>
					{% if page.has_next %}
						<a href="?page={{ page.next_page_number }}"> Next </a>
					{% endif %}
				</span>
			</div>

	O template de paginação espera um objeto Page para renderizar os links para a próxima página e para a anterior,
	e para exibir a página atual e o total e páginas do resultado.
	Edite o template blog/post/list.html para incluir o temlplate pagination.html no final do bloco {% content %}
	Código:
			...
		   {% include "pagination.html" with page=posts %}
		{% endblock %}
	Como o objeto Page que você está passando para o template se chama posts,
	deve incluir o template na lista de postagens, passando os parâmetros para renderizá-los.

	Esse método pode ser utilizado para reutilizar o template de paginação nas views paginadas de diferentes modelos.
	Acesse: http://127.0.0.1:8000/blog/ para verificar a paginação.


- Uso de views baseadas em classe de Django - 05/11/2021
	Views em forma de classe são um modo alternativo de implementar views na forma de objetos Python em vez de funções.
	Como uma view é um callable que recebe uma requisição web e devolve uma resposta,
	suas views também podem ser vdefinidas como métodos de classe.
	Django disponibiliza classes-base de views para isso.
	Herdam da classe view, que cuida do dispatching de métodos http e de outras funcionalidades comuns.
	Recursos:
		- organizam códigos relacionados a métodos http (como get,post ou put) em métodos separados, em vez de usar ramos de condicionais.
		- usam herança múltipla para criar classes de view reutilizáveis (chamado de mixins).

	Edite a view post_list da aplicação blog,
	para quie seja uma view baseada em classe a fim de usar ListView genérica oferecida por django. (permite listar objetos de qualquer tipo.)
	Código:
		from django.views.generic import ListView
		# View baseada em classe.
		# Faz a mesma coisa que a view post_list
		class PostListView(ListView):
			queryset = Post.published.all()
			context_object_name = 'posts'
			paginate_by = 3
			template_name = 'blog/post/list.html'

	Dizemos a ListView para fazer:
		- use um queryset específico em vez de obter todos os objetos. obs. poderia ser feito através de model = Post, e django teria criado o queryset Post.objects.all() genérico para você;
		- use a variável de contexto posts para os resultados da consulta. obs. caso não especifique, a default seria objects_list
		- faça a paginação do resultado, exibindo 3 objetos por página;
		- use um template personalizado para renderizar a página. se não definir, a listView usará blog/post_list.html

	Edite urls.py da aplicação blog, comente o padrão URL post_list e adicione o novo padrão de url utilizando a classe PostListView.
	Código:
		urlpatterns = [
			# views de postagens
			# path('', views.post_list, name='post_list'),
			path('', views.PostListView.as_view() , name='post_list'),
			path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
		]
	obs. Para manter a paginação funcionando, deve usar o objeto de página correto que é passado para o template.
	A view genérica ListView passa a página selecionada em uma variável chamada page_obj,
	logo, deve editar o template post/list.html, a fim de incluir o paginador e usar a variável correta.
	Código:
		#{% include "pagination.html" with page=posts %}
		{% include "pagination.html" with page=page_obj %}

	Acesse: http://127.0.0.1:8000/blog/ para verificar a paginação.

	Resumo: Vimos o básico sobre o framework web django, por meio da criação de uma aplicação simples de blog.
			Fizemos o design dos modelos de dados e aplicamos migrações ao projeto.
			Também criamos views, templates e URLs para o blog e incluímos a paginação de objetos.
			No próximo capítulo, veremos como aprimorar a aplicação de blog com um sistema de comentários e a funcionalidade de marcação com tags,
			e como permitir que usuários compartilhem postagens por email.
