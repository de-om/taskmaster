"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from tasks import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("lab/", views.lab_view),
    path("examples/", views.examples),
    path("añadir/", views.add_task),
    path("tareas/", views.list_tasks, name="list_tasks"),
    path("tareas/<int:pk>/", views.task_detail),
    path("tareas/<int:pk>/editar/", views.edit_task, name="edit_task"),
    path("tareas/calendar/<int:year>/", views.list_tasks_per_year),
    path("search/", views.search_task),
    re_path(r"^tareas/([lnh])/$", views.list_tasks_by_priority),
    re_path(r"^tareas/(low|normal|high)/$", views.list_tasks_by_priority),
    path("temas/", views.list_subjects),
    path("temas/<int:pk>/", views.subject_detail),
    path("admin/", admin.site.urls),
]
