import json

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status


User = get_user_model()


class UserLoginAPIViewAPITestCase(APITestCase):
    """Tests to users login"""

    url = reverse('api-account:user-login')

    def setUp(self):
        self.email = 'test@testuser.com'
        self.password = '1234567a'
        user = User.objects.create(
            first_name='Test',
            last_name='User',
            email=self.email,
            passport_number='1231231231'
        )

        user.set_password(self.password)
        user.save()

        self.token = user.token

    def test_user_login(self):
        """Test user login with verify data"""

        user_data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(self.url, user_data)

        self.assertTrue('token' in json.loads(response.content))


class ClientRegisterViewAPITestCase(APITestCase):
    """Tests to client registration"""

    url = reverse('api-account:client-account-register')

    def test_client_registration(self):
        """Test to verify that a post call with user valid data"""

        user_data = {
            "first_name": "Tester",
            "last_name": "Test",
            "email": "test@testuser.com",
            "passport_number": "1231231231",
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_unique_email_validation(self):
        """Test to verify that a post calls with already exists email"""

        user_data_1 = {
            "first_name": "Tester",
            "last_name": "Test",
            "email": "test@testuser.com",
            "passport_number": "1231231231",
        }

        response = self.client.post(self.url, user_data_1)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


        user_data_2 = {
            "first_name": "Tester",
            "last_name": "Test",
            "email": "test@testuser.com",
            "passport_number": "1231231232",
        }

        response = self.client.post(self.url, user_data_2)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class ClientProvidePINViewAPITestCase(APITestCase):
    """Tests to client provide PIN"""

    url = reverse('api-account:client-provide-pin')

    def setUp(self):

        self.user = User.objects.create(
            first_name='Test',
            last_name='Test',
            email="test@testuser.com",
        )

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token %s' % self.user.token)

    def test_client_provide_pin(self):
        """Test to verify put calls with valid data"""
        user_data = {
            'password': '1234567a',
            'password1': '1234567a'
        }
        response = self.client.put(self.url, user_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_client_verify_pin(self):
        """Test to verify put calls with invalid data"""
        user_data = {
            'password': '1234567a',
            'password1': '1234567'
        }
        response = self.client.put(self.url, user_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class ClientProfileViewAPITestCase(APITestCase):
    """Test for client profile"""

    url = reverse('api-account:client-profile')


    def setUp(self):
        client_active_with_pass = User.objects.create(
            first_name='Test',
            last_name='User',
            email='test@testuser.com',
            passport_number='12345678'
        )

        client_active_with_pass.set_password('1234567a')
        client_active_with_pass.save()

        client_active_without_pass = User.objects.create(
            first_name='Test1',
            last_name='User1',
            email='test1@testuser.com',
            passport_number='232414123'
        )

        client_deactive_with_pass = User.objects.create(
            first_name='Test2',
            last_name='User2',
            email='test2@testuser.com',
            passport_number='232414129',
            is_active=False
        )

        client_deactive_with_pass.set_password('1234567a')
        client_deactive_with_pass.save()

        manager = User.objects.create(
            first_name='Test',
            last_name='Test',
            email='test@testmanager.com',
            is_manager=True,
            passport_number='12345679'
        )

        self.client_1 = APIClient()
        self.client_1.credentials(HTTP_AUTHORIZATION='Token %s' % client_active_with_pass.token)

        self.client_2 = APIClient()
        self.client_2.credentials(HTTP_AUTHORIZATION='Token %s' % client_active_without_pass.token)

        self.client_3 = APIClient()
        self.client_3.credentials(HTTP_AUTHORIZATION='Token %s' % client_deactive_with_pass.token)

        self.manager = APIClient()
        self.manager.credentials(HTTP_AUTHORIZATION='Token %s' % manager.token)

    def test_update_user_profile(self):
        """Test to update the client's profile"""

        user_data = {
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'email': 'test@testuser.com',
            'passport_number': '21345678',
        }

        response = self.client_1.put(self.url, user_data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_active_client_allowed_to_profile(self):
        """Test to endpoint allow only for active client with password"""

        response = self.client_1.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client_2.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        response = self.client_3.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        response = self.manager.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class ManagerClientListViewAPITestCase(APITestCase):
    """Tests to endpoint api-account:manager-client-list"""

    url = reverse('api-account:manager-client-list')

    def setUp(self):
        manager = User.objects.create(
            first_name='Manager',
            last_name='manager',
            email='test@testuser.com',
            passport_number='32491220',
            is_manager=True,
        )

        client_1 = User.objects.create(
            first_name='Test',
            last_name='Client',
            email='test1@testuser.com',
            passport_number='32491221',
            is_closed=True,
        )

        client_2 = User.objects.create(
            first_name='Test',
            last_name='Client',
            email='test2@testuser.com',
            passport_number='32491222',
            is_active=False,
        )

        self.manager = APIClient()
        self.manager.credentials(HTTP_AUTHORIZATION='Token %s' % manager.token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token %s' % client_1.token)

    def test_only_manager_allowed(self):
        """Test endpoint to allow only for managers"""

        response = self.manager.get(self.url)
        content = json.loads(response.content)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, content['count'])

        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class ManagerClientDetailViewAPITestCase(APITestCase):
    """Test to endpoint """

    def setUp(self):
        manager = User.objects.create(
            first_name='Manager',
            last_name='manager',
            email='test@testuser.com',
            passport_number='32491220',
            is_manager=True,
        )

        client = User.objects.create(
            first_name='Test',
            last_name='Client',
            email='test1@testuser.com',
            passport_number='32491221',
            is_active=True,
        )

        self.url = reverse('api-account:manager-client-detail', kwargs={'id':client.id})

        self.manager = APIClient()
        self.manager.credentials(HTTP_AUTHORIZATION='Token %s' % manager.token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token %s' % client.token)

    def test_allowed_for_manager(self):
        """Test to verify endpoint for allow only for manager"""

        response = self.manager.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_activate_client(self):
        """Test to activate user by manager"""

        user_data = {
            'is_active': True,
        }

        response = self.manager.put(self.url, user_data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_client(self):
        """Test delete client by manager"""

        response = self.manager.delete(self.url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


