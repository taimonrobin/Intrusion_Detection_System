from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('source-address/<str:address>', views.source_address, name="source_address"),
    path('change_tolerence_level/<str:address>', views.change_tolerence_level, name="change_tolerence_level"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)