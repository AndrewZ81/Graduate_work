from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from todolist import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут панели администратора

    # Маршруты приложений
    path('core/', include(('core.urls', 'core'))),  # 'core'
    path('goals/', include(('goals.urls', 'goals'))),  # 'goals'
    path('bot/', include(('bot.urls', 'gbot'))),  # 'bot'

    # Маршруты для схем OpenAPI 3 приложения 'core'
    path('core/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('core/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('core/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Маршруты Simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Прочие маршруты
    path('oauth/', include('social_django.urls', namespace='social'))
]

# Создаём маршруты для облегчения тестирования
if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
    ]
