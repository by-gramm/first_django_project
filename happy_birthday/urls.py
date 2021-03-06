from django.urls import path
from happy_birthday import views

app_name = 'happy_birthday'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/new/', views.post_new, name="post_new"),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/new', views.comment_new, name="comment_new"),
    path('post/<int:pk>/comment/<int:comment_pk>/delete', views.comment_delete, name="comment_delete"),
]
