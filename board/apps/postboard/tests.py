import json, jwt
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
                            
        Category.objects.create(
                            id = 1,
                            name = "a"
        )
        

    # def tearDown(self):
    #     User.objects.all().delete()
    #     Category.objects.all().delete()

    def test_게시물_등록_success(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        board = {
                    "user": self.user.id,
                    "tag": [
                        "git",
                        "github"
                    ],
                    "title": "VCS",
                    "content": "Session5",
                    "category": "a"
                }
       
        # access_token = jwt.encode({'id':1}, SECRET_KEY, JWT_ALGORITHM)  
        # headers = {"HTTP_Authorization" : f"Bearer ${access_token}"}
        response = self.client.post('/api/postboard/board', data=board, content_type='application/json')
        self.assertEqual(response.status_code, 201)


# Create your tests here.
