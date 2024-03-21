from django.urls import path

from . import views

urlpatterns = [
    path('template/<uuid:id>/', views.template_detail, name="template_detail"),
]
