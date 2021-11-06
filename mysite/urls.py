"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

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

# O novo padrão de url definido com include, faz referência aos padroes de url definidos na aplicação blog.
# de modo que sejam incluídos no path blog/.
# Incluímos esses padrões no namespace blog.
# Os namespaces devem ser únicos no âmbito do projeto.
# É possível referenciar os urls do blog usando namespace seguido de :nome do url. Ex. blog:post_list e blog:post_detail
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
]
