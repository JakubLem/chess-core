from django.conf.urls import url, include


urlpatterns = [
    # url(r"^api/", include("swagger.urls")),
    url(r"^api/", include("api.urls")),
    url(r"^auth/", include("authorization.urls")),
]
