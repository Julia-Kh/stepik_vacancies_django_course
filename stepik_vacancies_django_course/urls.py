from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include
from django.urls import path

from vacancies.views import LogInView
from vacancies.views import SignupView


urlpatterns = [
    path('login/', LogInView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', SignupView.as_view(), name='sign_up'),
    path('admin/', admin.site.urls),

    path('', include('vacancies.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
