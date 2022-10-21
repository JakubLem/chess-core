from django.conf.urls import include, url
from rest_framework import routers
from authorization import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet, basename="users")

urlpatterns = [
    url(r"^", include(router.urls)),
]
