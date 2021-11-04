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

# O novo padrão de url definido com include, faz referência aos padroes de url definidos na aplicação blog.
# de modo que sejam incluídos no path blog/.
# Incluímos esses padrões no namespace blog.
# Os namespaces devem ser únicos no âmbito do projeto.
# É possível referenciar os urls do blog usando namespace seguido de :nome do url. Ex. blog:post_list e blog:post_detail
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/',include('blogs.urls', namespace='blog')),
]
