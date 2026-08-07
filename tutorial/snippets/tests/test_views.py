import json
from django.test import TestCase
from snippets.models import Snippet

class SnippetViewTests(TestCase):
    def setUp(self):
        self.snippet = Snippet.objects.create(
            title = "Test title",
            code = "print('Test Code Snippet')",
            language = "python",
            style = "friendly"
        )

    def test_list_snippets_get(self):
        response = self.client.get("/snippets/")
        self.assertEqual(response.status_code, 200)

    def test_create_snippet_post(self):
        payload = {
            "title": "New Test Title",
            "code": "print('New Test Code Snippet')",
            "language": "python",
            "style": "friendly"
        }
        response = self.client.post("/snippets/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_snippet_detail_not_found(self):
        response = self.client.get("/snippets/9999")
        self.assertEqual(response.status_code, 404)

    def test_delete_snippet(self):
        response = self.client.delete(f"/snippets/{self.snippet.pk}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Snippet.objects.count(), 0)