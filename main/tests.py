import hashlib

from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Secret


# Create your tests here.

class GenerateTestCase(APITestCase):
    def test_create_secret(self):
        secret = {
            'secret_string': 'test_string',
            'code_phrase': 'test_code',
        }

        response = self.client.post(
            '/generate/',
            data=secret
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        bad_secret = {
            'secret_string': 'test_string'
        }

        response = self.client.post(
            '/generate/',
            data=bad_secret
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class SecretsTestCase(APITestCase):
    def setUp(self) -> None:
        secret_key = 'test_secret_key'
        code_phrase = 'test_phrase'
        hash_secret_key = hashlib.new('md5')
        hash_code_phrase = hashlib.new('md5')
        hash_secret_key.update(secret_key.encode())
        hash_code_phrase.update(code_phrase.encode())
        Secret.objects.create(
            secret_string='test_string',
            code_phrase=hash_code_phrase.hexdigest(),
            secret_key=hash_secret_key.hexdigest()
        )

    def test_show_secret(self):
        response = self.client.post(
            '/secrets/test_secret_ke/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

        response = self.client.post(
            '/secrets/test_secret_key/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        response = self.client.post(
            '/secrets/test_secret_key/',
            data={'code_phrase': 'wrong_code_phrase'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        response = self.client.post(
            '/secrets/test_secret_key/',
            data={'code_phrase': 'test_phrase'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'secret_string': 'test_string'}
        )

        response = self.client.post(
            '/secrets/test_secret_key/',
            data={'code_phrase': 'test_phrase'}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            response.json(),
            {'message': 'секрет уже просматривался'}
        )

