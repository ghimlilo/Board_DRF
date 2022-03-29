import json, jwt, datetime

from unittest import mock
from django.utils import timezone

from rest_framework import status
from rest_framework.test import force_authenticate, APITestCase, APIClient
from django.test import TestCase, Client

from board.apps.postboard.models import Board, BoardTag, Review, Category, Tag
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

class BoardDetailViewTestCase(APITestCase):

    time_test_now = timezone.now() - datetime.timedelta(days=1)

    @mock.patch("django.utils.timezone.now")
    def setUp(self, mock_now):

        mock_now.return_value = self.time_test_now
        
        self.user = User.objects.create(
                            email = "kimlilo@gmail.com",
                            account_name = "킴릴로"
                            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        Category.objects.create(
                            id = 1,
                            name = "z",
        )

        Category.objects.create(
                            id = 2,
                            name = "x",
        )

        Board.objects.create(
            id = 1,
            user = self.user,
            title = "c",
            content = "d",
            category = Category.objects.get(id=1),       
        )

        Board.objects.create(
            id = 2,
            user = self.user,
            title = "e",
            content = "f",
            category = Category.objects.get(id=2),       
        )

        Tag.objects.create(
            id = 1,
            name = "a"
        )

        Tag.objects.create(
            id = 2,
            name = "b",
        )
        
        BoardTag.objects.create(
            id = 1,
            tag = Tag.objects.get(id=1),
            board = Board.objects.get(id=1),
        )

        BoardTag.objects.create(
            id = 2,
            tag = Tag.objects.get(id=2),
            board = Board.objects.get(id=1),
        )

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        BoardTag.objects.all().delete()
        Tag.objects.all().delete()
        Board.objects.all().delete()

    def test_get_register_success(self):
        dt = self.time_test_now.isoformat()
        dt = str(dt).replace('+00:00', 'Z')
        
        response = self.client.get('/api/postboard/board/1')
        self.assertEqual(response.json(), 
            {
                "id": 1,
                "user": "킴릴로",
                "tag": [
                    "a",
                    "b"
                ],
                "title": "c",
                "content": "d",
                "viewcount": 0,
                "category": 1, 
                "created_at" : dt,
                "updated_at" : dt,
                "reviews" : []
            }
        )

class ReviewCreateViewTestCase(APITestCase):

    time_test_now = timezone.now() - datetime.timedelta(days=1)    

    @mock.patch("django.utils.timezone.now")
    def setUp(self, mock_now):

        mock_now.return_value = self.time_test_now

        self.user = User.objects.create(
                            email = "kimlilo@gmail.com",
                            account_name = "킴릴로"
                            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        Category.objects.create(
                            id = 1,
                            name = "z"
        )

        Board.objects.create(
            id = 1,
            user = self.user,
            title = "c",
            content = "d",
            category = Category.objects.get(id=1),       
        )       

        Tag.objects.create(
            id = 1,
            name = "a"
        )

        Tag.objects.create(
            id = 2,
            name = "b",
        )
        
        BoardTag.objects.create(
            id = 1,
            tag = Tag.objects.get(id=1),
            board = Board.objects.get(id=1),
        )

        BoardTag.objects.create(
            id = 2,
            tag = Tag.objects.get(id=2),
            board = Board.objects.get(id=1),
        )


    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        BoardTag.objects.all().delete()
        Tag.objects.all().delete()
        Board.objects.all().delete()

    def test_post_register_success(self):

        data = {
                    "content" : "test"
                }
        
        # access_token = jwt.encode({'id':1}, SECRET_KEY, JWT_ALGORITHM)  
        # headers = {"HTTP_Authorization" : f"Bearer ${access_token}"}
        response = self.client.post('/api/postboard/board/1/review', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)