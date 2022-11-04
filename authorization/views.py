import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from authorization import serializers, models, exceptions  # noqa:E0401 


class UserViewSet(ModelViewSet):  # noqa:R0901
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    lookup_field = "identifier"
    lookup_url_kwarg = "identifier"

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        serializer.save()
        return Response(serializer.data, status=201)

    @action(
        detail=False, url_path="login", methods=["post"]
    )
    def login(self, request):
        email = request.data['email']
        password = request.data['password']  # noqa:W0612 TODO
        user = models.User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.UnauthenticatedException(detail="Invalid user!")

        hashed_password = user.password
        if not check_password(password, hashed_password):
            raise exceptions.UnauthenticatedException(detail="Invalid password!")

        payload = {
            'identifier': user.identifier,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'user': user.json()
        }
        return response

    @action(
        detail=False, url_path="logout", methods=["post"], permission_classes=[]
    )
    def logout(self, request):  # noqa:W0613
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
