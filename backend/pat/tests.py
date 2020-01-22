from pat.models import User, Pack
from rest_framework.test import APITestCase
from rest_framework import status
from .utils import UserType
from rest_framework.test import APIClient


class RegistrationTestCase(APITestCase):

    def test_create_user(self):
        data = {'email': 'test@wp.pl', 'password': 'Test123!', 'first_name': 'Test',
                'last_name': 'Tester', 'type': 2}
        response = self.client.post('/api/users/', data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(1, User.objects.all().count())


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="set@wp.pl", username="set@wp.pl", password="test321!",
                                             first_name='Test', last_name='Tester', type=UserType.CLIENT)
        self.get_token()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def get_token(self):
        data = {"email": "set@wp.pl", "password": "test321!"}
        response = self.client.post('/auth/token/', data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.token = response.data.get("access")

    def test_get_user_detail(self):
        response = self.client.get('/api/users/me/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get("email"), User.objects.get(pk=1).email)

    def test_forbidden_to_get_user_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'abc')
        response = self.client.get('/api/users/me/')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)  # Get back proper token

    def test_user_patch(self):
        data = {"first_name": "Pat"}
        response = self.client.patch("/api/users/me/", data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        response = self.client.delete("/api/users/me/")
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)


class PackTestCase(APITestCase):

    def setUp(self):
        self.user_client = User.objects.create_user(email="set@wp.pl", username="set@wp.pl", password="test321!",
                                                    first_name='Client', last_name='Tester', type=UserType.CLIENT)
        self.user_courier = User.objects.create_user(email="set2@wp.pl", username="set2@wp.pl", password="test321!",
                                                     first_name='Courier', last_name='Tester', type=UserType.COURIER)
        self.pack = Pack.objects.create(name="Test Pack", pickup_address="Gdynia", shipping_address="Sopot",
                                        purchaser=self.user_client)

        self.get_tokens()
        self.client = APIClient()

    def get_tokens(self):
        # Courier token
        data = {"email": "set@wp.pl", "password": "test321!"}
        response = self.client.post('/auth/token/', data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.token_client = response.data.get("access")

        # Client token
        data = {"email": "set2@wp.pl", "password": "test321!"}
        response = self.client.post('/auth/token/', data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.token_courier = response.data.get("access")

    def test_add_pack(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_client)
        data = {"name": "Test Pack", "pickup_address": "Gdynia", "shipping_address": "Sopot",
                "purchaser": self.user_client.id}
        response = self.client.post("/api/packs/", data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_show_packs(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_client)
        response = self.client.get("/api/packs/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_courier_reserve_pack(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_courier)
        response = self.client.patch("/api/packs/courier/1")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
