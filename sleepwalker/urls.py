"""
URL configuration for sleepwalker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("api/", include("sleepwalker.apps.core.urls")),
    path("api/auth/", include("sleepwalker.apps.authenticate.urls")),
    path("api/sessions/", include("sleepwalker.apps.logs_sessions.urls"))
]

if settings.DEBUG:
    from django.contrib import admin
    from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

    urlpatterns.append(path("admin/", admin.site.urls))

    urlpatterns.append(path("api/docs/schema/", SpectacularAPIView.as_view(), name="schema"))
    urlpatterns.append(path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"))
