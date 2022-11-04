from django.db import models
from django.contrib.auth.hashers import make_password
from django.conf import settings

class User(models.Model):
    identifier = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, settings.PASSWORD_HASH_KEY, settings.PASSWORD_HASH_ALG)
        super(User, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.identifier}, {self.name}, {self.surname}"

    def json(self) -> dict:
        return {
            "identifier": self.identifier,
            "name": self.name,
            "surname": self.surname,
            "username": self.username
        }
