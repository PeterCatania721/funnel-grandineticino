"""URL principali del progetto.

Le pagine pubbliche usano i18n_patterns: ogni URL è prefissato dalla lingua
(es. /it/, /de/, /fr/, /en/). L'admin resta fuori dai prefissi lingua.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

_site_urls = "core.funnel_urls" if settings.FUNNEL_MODE else "core.urls"

urlpatterns += i18n_patterns(
    path("", include(_site_urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
