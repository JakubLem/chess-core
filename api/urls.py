# from django.conf.urls import include, url
# from rest_framework import routers


from . import views

# router = routers.DefaultRouter()
# router.register(r"games", views.Games, basename="games")


# urlpatterns = [
#     url(r"^", include(router.urls)),
# ]

from django.urls import path
urlpatterns = [
    path('<str:room_name>/', views.room, name='room'),
]
