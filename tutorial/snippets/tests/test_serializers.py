from django.test import TestCase
from django.contrib.auth.models import User

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer

from rest_framework.test import APIRequestFactory

class SnippetSerializerTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="testuser", password="pass123")
        self.factory = APIRequestFactory()
        self.request = self.factory.get("/")
    def test_serialize_snippet(self):
        snippet = Snippet.objects.create(owner=self.owner, code="print('hello, world')")
        serializer = SnippetSerializer(snippet, context={"request": self.request})  

        self.assertEqual(serializer.data["code"], "print('hello, world')")
        self.assertEqual(serializer.data["language"], "python")
        self.assertEqual(serializer.data["style"], "friendly")

    def test_deserialize_and_create(self):
        data = {"code": "print('test')", "language": "python"}
        serializer = SnippetSerializer(data=data, context={"request": self.request}) 

        self.assertTrue(serializer.is_valid(), serializer.errors)
        snippet = serializer.save(owner=self.owner)

        self.assertEqual(snippet.code, "print('test')")
        self.assertEqual(snippet.owner, self.owner)

    def test_update_snippet(self):
        snippet = Snippet.objects.create(owner=self.owner, code="old code", language="python")
        serializer = SnippetSerializer(
            snippet,
            data={"code": "new code", "language": "javascript"},
            context={"request": self.request},  
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_snippet = serializer.save()

        self.assertEqual(updated_snippet.code, "new code")
        self.assertEqual(updated_snippet.language, "javascript")
        self.assertEqual(updated_snippet.owner, self.owner)

class UserSerializerTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.request = self.factory.get("/")

    def test_lists_owned_snippet_ids(self):
        owner = User.objects.create_user(username="user", password="pass123")
        snippet = Snippet.objects.create(owner=owner, code="a = 1")
        data = UserSerializer(owner, context={"request": self.request}).data
        self.assertEqual(data["username"], "user")
        self.assertIn(str(snippet.pk), data["snippets"][0])  