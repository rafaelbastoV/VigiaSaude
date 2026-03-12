from django.contrib import admin
from django.urls import path, include
from dengue import views
from dengue.views import estatisticas_estados

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "api/estados/<int:ano>/",
        estatisticas_estados,
        name="estatisticas_estados"
    ),
    path('', views.index),
    path('ultima_atualizacao/', views.ultima_atualizacao)
]
