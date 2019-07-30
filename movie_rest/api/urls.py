from . import views
from django.urls import path, include
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('movies', views.MovieView)
routers.register('comments', views.CommentView, base_name='comment')

urlpatterns = [
    path('', include(routers.urls)),
    path(r'top/', views.TopMovies.as_view(), name='top'),
]
