from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from catalog.views import logout_view, logged_out_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/log_out/', logout_view, name="logout"),
    path('accounts/logged_out/', logged_out_view, name="logged_out"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
