from django.conf import settings
from django.urls import include
from django.urls import path


urlpatterns = [
    path('', include('vacancies.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
