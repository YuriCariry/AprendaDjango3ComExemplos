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

- Design de Modelos e geração de migrações para os modelos


- Criação de um site de administração para os modelos


- QuerySets e gerenciadores (managers)


- Criação de views, templates e urls


- Adição de paginação e views com lista


- Uso de views baseadas em classe de Django
