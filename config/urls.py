from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from food.api import bueno_webhook
from food.api import router as food_router
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from users.api import router as users_router

schema_view = get_schema_view(
    openapi.Info(
        title="Hillel Catering APi",
        default_version="v1",
        description="Catering API. Only for internal usage",
        contact=openapi.Contact(email="catering@support.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = (
    [
        # USERS MANAGEMENT
        # ==================
        path("admin/", admin.site.urls),
        path("auth/token/", TokenObtainPairView.as_view()),
        path("webhooks/bueno/", bueno_webhook),
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
    + users_router.urls
    + food_router.urls
)


# if you need to reject the access to Swagger on production
# if settings.LIVE is False:
#     urlpatterns += [...]


if settings.DEBUG is True:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
