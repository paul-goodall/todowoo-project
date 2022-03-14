from django.urls import path
from . import views

my_urls = [
    path('current/', views.currenttodos,  name='currenttodos'),
    path('create/',  views.createtodo,    name='createtodo'),
    path('todo/<int:todo_pk>',  views.viewtodo,    name='viewtodo'),
    path('edit/<int:todo_pk>',  views.edittodo,    name='edittodo'),
]
