from django.test import TestCase
from snippets.models import Snippet

class SnippetModelTests(TestCase):
    def test_create_snippet_with_defaults(self):
        snippet = Snippet.objects.create(code="print('hello')")

        self.assertEqual(snippet.title, "")
        self.assertEqual(snippet.language, "python")
        self.assertEqual(snippet.style, "friendly")
        self.assertFalse(snippet.linenos)

    def test_create_field_is_auto_set(self):
        snippet = Snippet.objects.create(code="print(1)")
        self.assertIsNotNone(snippet.created)

    def test_ordering_by_created(self):
        first = Snippet.objects.create(code="first")
        second = Snippet.objects.create(code="second")

        snippets = list(Snippet.objects.all())
        self.assertEqual(snippets, [first, second])