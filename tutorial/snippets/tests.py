from django.test import TestCase
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# Create your tests here.
class SnippetSerializerTests(TestCase):
    def test_serialize_snippet(self):
        snippet = Snippet.objects.create(code="print('hello, world')")
        serializer = SnippetSerializer(snippet)

        self.assertEqual(serializer.data["code"], "print('hello, world')")
        self.assertEqual(serializer.data["language"], "python")
        self.assertEqual(serializer.data["style"], "friendly")

    def test_deserialize_and_create(self):
        data = {"code": "print('test')", "language": "python"}
        serializer = SnippetSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        snippet = serializer.save()

        self.assertEqual(snippet.code, "print('test')")

    def test_update_snippet(self):
        snippet = Snippet.objects.create(code="old code", language="python")
        serializer = SnippetSerializer(snippet, data={"code": "new code", "language": "javascript"})

        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_snippet = serializer.save()

        self.assertEqual(updated_snippet.code, "new code")
        self.assertEqual(updated_snippet.language, "javascript")
