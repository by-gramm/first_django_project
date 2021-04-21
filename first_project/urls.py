from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('introduce/', TemplateView.as_view(template_name='introduce.html'), name='introduce'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include("allauth.urls")),
    path('happy_birthday/', include('happy_birthday.urls')),
    path('', TemplateView.as_view(template_name='root.html'), name='root'),
    path('hidden/', login_required(TemplateView.as_view(template_name='etc.html')), name='etc'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
