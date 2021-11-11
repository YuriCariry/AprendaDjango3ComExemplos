from django.urls import path
from . import views

# Definimos o namespace da aplicação.
# Permite organizar as urls por aplicação e usar o nome ao referenciá-los.
app_name = 'blog'

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
	# path('', views.post_list, name='post_list'),
	path('',                                              views.PostListView.as_view(),  name='post_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,             name='post_detail'),
	path('<int:post_id>/share/',                          views.post_share,              name='post_share'),
]

# Obs. Temos que incluir os padrões de URL da aplicação blognos padrões principais de URL de projeto.
#      Devemos editar urls.py do projeto mysite
# Você utilizará o get_absolute_url() em seus templates para fazer a ligação com postagens específicas.
# URLs canônicos para os modelos, é o URL preferencial para um recurso.
# O método reverse, permite criar URLs com base no nome e aceita parâmetros opcionais.
# def get_absolute_url(self):
#     return reverse('blog:post_detail',
#                     args=[self.publish.year,
#                           self.publish.month,
#                           self.publish.day,
#                           self.slug
#                          ])
