from django.urls import path
from news_article import views

app_name = 'article'

urlpatterns = [
    path('article/new/', views.article_new, name="article_new"),
    path('article/<int:pk>', views.article_detail, name='article_detail'),
    path('article/<int:pk>/edit', views.article_edit, name='article_edit'),
    path('article/<int:pk>/delete', views.article_delete, name='article_delete'),
]
