from django.contrib.auth import get_user_model
from django.test import TestCase


from rest_framework.test import APIClient

from .models import Tweet


User = get_user_model()
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='abc', password='abcd1234')
        self.userb = User.objects.create_user(username='abc-2', password='abcd1234-2')
        Tweet.objects.create(content="test tweet 1", user=self.user)
        Tweet.objects.create(content="test tweet 2", user=self.user)
        Tweet.objects.create(content="test tweet 3", user=self.user)
        Tweet.objects.create(content="test tweet 4", user=self.userb)
        self.currentCount = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="test tweet 5", user=self.user)
        self.assertEqual(tweet_obj.id, 5)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='abcd1234')
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",{"id":1, "action":"like"})
        likes_count = response.json().get("likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(likes_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",{"id":2, "action":"like"})
        likes_count = response.json().get("likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(likes_count, 1)
        response = client.post("/api/tweets/action/",{"id":2, "action":"unlike"})
        likes_count = response.json().get("likes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(likes_count, 0)

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/",{"id":3, "action":"retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        retweet_id = data.get("id")
        self.assertNotEqual(retweet_id, 3)
        self.assertEqual(self.currentCount + 1, retweet_id)

    def test_tweet_create_api_view(self):
        request_data = {"content": "tweet for testing tweet create api view"}
        client = self.get_client()
        response = client.post("/api/tweets/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEqual(self.currentCount + 1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 404)
        response_incorrect_user = client.delete("/api/tweets/4/delete/")
        self.assertEqual(response_incorrect_user.status_code, 401)
