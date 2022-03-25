"""BankAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view = get_schema_view(
   openapi.Info(
      title="Bank API",
      default_version='v1',
      description="""
      This is a dummy description.""",
      terms_of_service="",
      contact=openapi.Contact(email="gloryglow99@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/account/', include('account.urls')),
    path("",schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

# from django.contrib import admin
# from django.urls import path, include
# from . import views
# from rest_framework_simplejwt import views as jwt_views



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('v1/', include('main.urls')),
#     # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
# ]
