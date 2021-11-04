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
urlpatterns = [
    # views de postagens
    path('',views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
          views.post_detail, name='post_detail'),
]
