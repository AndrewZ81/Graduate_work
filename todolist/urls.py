from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from todolist import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'))),  # Маршруты приложения 'core'
    path('goals/', include(('goals.urls', 'goals'))),  # Маршруты приложения 'goals'

    # Маршруты для схем OpenAPI 3 приложения 'core'
    path('core/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('core/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('core/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('oauth/', include('social_django.urls', namespace='social'))
]

# Создаём маршруты для облегчения тестирования
if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
    ]
