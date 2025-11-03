from django.conf import settings
from django.contrib import admin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt import views
from django.contrib.auth import views as auth_views, logout


schema_view = get_schema_view(
    openapi.Info(
        title="SHOP Service API",
        default_version='v1',
        description="For shop Service Rest API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="azamat@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

def logout_view(request):
    logout(request)
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.v1.urls.user')),
    path('api/', include('api.v1.urls.product')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('accounts/logout/', logout_view, name='logout'),

    re_path(r"^api/auth/user/sign_in/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^api/auth/token/refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^api/auth/token/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<str:format>.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
    path("__debug__/", include("debug_toolbar.urls")),
]
