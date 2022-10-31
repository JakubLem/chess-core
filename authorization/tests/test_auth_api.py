import pytest
from authorization import models

@pytest.mark.django_db
class TestUsers:
    def test_register_login_user_and_logout(self, client):
        # creating user in kc and in database
        assert models.User.objects.count() == 0
        c = client()
        response = c.post("/auth/users/", {
            "name": "test_name",
            "surname": "some_surname",
            "username": "some_username",
            "email": "test@mail.pl",
            "password": "password1234"
        })
        assert response.status_code == 201
        assert response.json()["identifier"]
        assert models.User.objects.count() == 1
        # test invalid password
        response = c.post("/auth/users/login/", {
            "email": "test@mail.pl",
            "password": "invalid password"
        })
        assert response.status_code == 401
        assert response.json() == {'detail': 'Invalid password!'} 
        assert "jwt" not in response.cookies

        # test valid password
        response = c.post("/auth/users/login/", {
            "email": "test@mail.pl",
            "password": "password1234"
        })
        # assert response.status_code == 200
        assert response.json()["jwt"]
        assert response.json()["user"]
        assert response.json()["user"]["identifier"]
        assert response.json()["user"]["username"]
        assert "jwt" in response.cookies
        assert response.cookies["jwt"].value
        # c.cookies["jwt"] = SimpleCookie({"invalid": "invalid"})
        # response = c.get("/auth/users/user/")
        # assert response.status_code == 200
        response = c.post("/auth/users/logout/")
        assert response.status_code == 200
        assert response.json() == {"message": "success"}
        assert not response.cookies["jwt"].value

    def test_register_strip(self, client):
        c = client()
        response = c.post("/auth/users/", {
            "name": "       test_name_2    ",
            "surname": "      some_surname     ",
            "username": "        some_username__2      ",
            "email": "       test2@mail.pl       ",
            "password": "password21234"
        })
        assert response.status_code == 201
        assert models.User.objects.count() == 1
        user = models.User.objects.all()[0]
        assert user.username == "some_username__2"

    def test_invalid_email(self, client):
        c = client()
        response = c.post("/auth/users/", {
            "firstName": "       test_name_2    ",
            "lastName": "      some_surname     ",
            "username": "        some_username__2      ",
            "email": "       test2@mail.pl       ",
            "password": "password21234"
        })
        assert response.status_code == 400
        assert models.User.objects.count() == 0
