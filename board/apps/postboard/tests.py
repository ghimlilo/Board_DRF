import json, jwt
from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase, APIClient
from django.test import TestCase, Client

from board.apps.postboard.models import Board, Review, Category, Tag
from board.apps.user.models import User
from board.settings import SECRET_KEY, JWT_ALGORITHM


class BoardListCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
                            email = "kimlilo@gmail.com",
                            account_name = "킴릴로"
                            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        Category.objects.create(
                            id = 1,
                            name = "a"
        )
       
    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()

    def test_post_register_success(self):

        data = {
                    "tag": ["a", "b"],
                    "title": "VCS",
                    "content": "Session5",
                    "category": 1
                }
        
        # access_token = jwt.encode({'id':1}, SECRET_KEY, JWT_ALGORITHM)  
        # headers = {"HTTP_Authorization" : f"Bearer ${access_token}"}
        response = self.client.post('/api/postboard/board', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
