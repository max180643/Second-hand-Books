from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('<int:topic_id>/', views.topic, name='topic'),
    path('manage/', views.manage, name='manage'),
    path('hide/<int:id>/', views.hide_topic, name='hide'),
    path('show/<int:id>/', views.show_topic, name='show'),
    path('delete/<int:id>/', views.delete_topic, name='delete')
]
