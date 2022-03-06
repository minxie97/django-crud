from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )
        self.snack = Snack.objects.create(
            title="pretzels", purchaser=self.user, description="it's german!",
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "pretzels")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "pretzels")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(f"{self.snack.description}", "it's german!")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pretzels")
        self.assertTemplateUsed(response, "snack_list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Purchaser: tester")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "hot dog",
                "purchaser": self.user.id,
                "description": "glizzy"
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "glizzy")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_update_view(self):
        response = self.client.post(
            reverse("snack_update", args='1'),
            {
                "title": "pretzels updated",
                "purchaser": self.user.id,
                "description": "with some cheese dip"
            },
            follow=True
        )

        self.assertRedirects(response, reverse('snack_detail', args='1'))
        self.assertContains(response, "with some cheese dip")
        self.assertTemplateUsed(response, "snack_detail.html")

    def test_snack_delete_view(self):
        response = self.client.get(reverse('snack_delete', args='1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'snack_delete.html')

        response = self.client.post(reverse('snack_delete', args='1'), follow=True)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertNotContains(response, 'pretzels')