"""URL del funnel Grandineticino.ch (solo quando FUNNEL_MODE è attivo)."""
from django.urls import path

from core import funnel_views

urlpatterns = [
    path("", funnel_views.funnel_grandine, name="funnel_home"),
    path("grazie/", funnel_views.funnel_grazie, name="funnel_grazie"),
]
