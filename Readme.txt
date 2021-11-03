Tentando aprender Django.
Livro Aprenda Django3 com Exemplos.

Objetivos:
1. Criando uma aplicação de Blog
2. Criando uma Rede Social
3. Criando uma Loja Online
4. Criando uma plataforma de Ensino à Distância

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

- QuerySets e gerenciadores (managers)

- Criação de views, templates e urls

- Adição de paginação e views com lista

- Uso de views baseadas em classe de Django
