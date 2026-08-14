from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from snippets.models import Snippet

class SnippetPermissionTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass123")
        self.other = User.objects.create_user(username="other", password="pass321")

        self.snippet = Snippet.objects.create(owner = self.owner, code="print(1)")

    # --- Read access: Everyone including anonymous --- 
    def test_anonymous_can_list_snippets(self):
        response = self.client.get("/snippets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_retrieve_snippet(self):
        response = self.client.get(f"/snippets/{self.snippet.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- Create: requires Auth ---
    def test_anonymous_cannot_create_snippet(self):
        payload = {"code": "print(1)", "langauge": "python", "style": "friendly"}
        response = self.client.post("/snippets/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_user_can_create_snippet(self):
        self.client.force_login(self.owner)
        payload = {"code": "print(1)", "langauge": "python", "style": "friendly"}
        response = self.client.post("/snippets/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"] and Snippet.objects.get(id=response.data["id"]).owner, self.owner)

    # --- Update: owner only --- 
    def test_anonymous_cannot_update_snippet(self):
        response = self.client.put(
            f"/snippets/{self.snippet.pk}/",
            {"code": "updated", "language": "python", "style": "friendly"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_snippet(self):
        self.client.force_login(self.owner)
        response = self.client.put(
            f"/snippets/{self.snippet.pk}/",
            {"code": "updated", "language": "python", "style": "friendly"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.snippet.refresh_from_db()
        self.assertEqual(self.snippet.code, "updated")

    def test_non_owner_cannot_update_snippet(self):
        self.client.force_login(self.other)
        response = self.client.put(
            f"/snippets/{self.snippet.pk}/",
            {"code": "updated", "language": "python", "style": "friendly"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Delete: owner only ---
    def test_anonymous_cannot_delete_snippet(self):
        response = self.client.delete(f"/snippets/{self.snippet.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Snippet.objects.filter(pk=self.snippet.pk).exists)
    def test_non_owner_cannot_delete_snippet(self):
        self.client.force_login(self.other)
        response = self.client.delete(f"/snippets/{self.snippet.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Snippet.objects.filter(pk=self.snippet.pk).exists)

    def test_owner_can_delete_snippet(self):
        self.client.force_login(self.owner)
        response = self.client.delete(f"/snippets/{self.snippet.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Snippet.objects.filter(pk=self.snippet.pk).exists())
