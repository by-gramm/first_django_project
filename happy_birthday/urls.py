from django.urls import path
from happy_birthday import views

app_name = 'happy_birthday'

urlpatterns = [
    path('post/new/', views.post_new, name="post_new"),
]
