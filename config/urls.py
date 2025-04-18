"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static

from food.api import bueno_webhook
from food.api import router as food_router
from users.api import CustomTokenObtainPairView
from users.api import router as users_router

urlpatterns = (
    [
        # USERS MANAGEMENT
        # ==================
        path("grappelli/", include("grappelli.urls")),
        path("admin/", admin.site.urls),
        path("api/token/", CustomTokenObtainPairView.as_view()),
        path("webhooks/bueno/", bueno_webhook),
    ]
    + users_router.urls
    + food_router.urls

)

if settings.DEBUG is True:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
     )