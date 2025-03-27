from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from food.api import bueno_webhook
from food.api import router as food_router
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from users.api import router as users_router
from users.serializers import TokenObtainResponseSerializser

schema_view = get_schema_view(
    openapi.Info(
        title="Hillel Catering API",
        default_version="v1",
        description="Catering API. Only for internal usage",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hillel@support.ua"),
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
        path(
            "auth/token/",
            swagger_auto_schema(
                method="post", responses={201: TokenObtainResponseSerializser}
            )(
                TokenObtainPairView.as_view(),
            ),
        ),
        path("webhooks/bueno/", bueno_webhook),
        # OPEN API DOCUMENTATIONS
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


# if settings.DEBUG is True:
#     urlpatterns += static(
#         settings.STATIC_URL,
#         document_root=settings.STATIC_ROOT,
#     )
