import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Education, Experience


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="Portfolio", description="My experience", category="internship",
            started_at="2025-01-01",
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse(
            "api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star",
                                args=[self.experience.id])
        self.payload = {
            "title": "New experience", "description": "A useful experience",
            "category": "research", "thumbnail": "https://example.com/image.png",
            "started_at": "2025-02-01", "ended_at": "2025-03-01",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(
            self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(
                self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {
                             "title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(
                self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(
            pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)" >'}, "title"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
        ]:
            response = self.client.post(
                self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
            self.assertEqual(Experience.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(
            self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.description, "My experience")
        response = self.client.put(
            self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(
            self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(
            pk=self.experience.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(
            self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        payload = {**self.payload, "ended_at": None}
        response = self.client.post(self.list_url, {
            **payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
            "is_ongoing": False,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertTrue(response.data["is_ongoing"])

    def test_staff_and_editor_cannot_manage_tutorial_experiences(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(
            self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(
            self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(
            username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="education-owner", password="test-password",
            email="education-owner@example.com",
        )
        self.visitor = User.objects.create_user(
            username="education-visitor", password="test-password",
        )
        editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="education-editor", password="test-password",
        )
        self.editor.groups.add(editor_group)
        self.education = Education.objects.create(
            institution_name="Universitas Indonesia", degree="bachelor",
            field_of_study="Computer Science", description="Undergraduate study",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.id])
        self.star_url = reverse("api:education-star", args=[self.education.id])
        self.payload = {
            "institution_name": "Example University", "degree": "master",
            "field_of_study": "Data Science", "logo_url": "https://example.com/logo.png",
            "description": "Graduate study", "ended_at": None,
        }

    def test_public_list_detail_and_search(self):
        response = self.client.get(self.list_url, {"q": "COMPUTER"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["degree_display"], "Bachelor's")
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("starred_by", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.get(self.list_url, {"degree": "doctorate"}).data, [])
        missing_url = reverse("api:education-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing_url).status_code, 404)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        education_url = reverse("api:education-detail", args=[response.data["id"]])
        response = self.client.patch(
            education_url, {"institution_name": "Updated University"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["field_of_study"], "Data Science")
        self.assertEqual(self.client.delete(education_url).status_code, 204)

    def test_non_owner_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(
                self.list_url, self.payload, format="json",
            ).status_code, 403)
            self.assertEqual(self.client.patch(
                self.detail_url, {"institution_name": "Changed"}, format="json",
            ).status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(
            self.detail_url, {"institution_name": "Edited University"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(
            self.list_url, self.payload, format="json",
        ).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "Edited University")
        self.assertEqual(Education.objects.count(), 1)

    def test_serializer_validation_and_read_only_fields(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"institution_name": "  "}, "institution_name"),
            ({"institution_name": "<b></b>"}, "institution_name"),
            ({"logo_url": "javascript:alert(1)"}, "logo_url"),
        ]:
            response = self.client.post(
                self.list_url, {**self.payload, **changes}, format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
            self.assertEqual(Education.objects.count(), 1)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 10, "is_starred": True,
            "started_at": "2000-01-01T00:00:00Z", "is_ongoing": False,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertTrue(response.data["is_ongoing"])

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(user=self.visitor)
        self.assertTrue(self.client.post(self.star_url).data["is_starred"])
        self.assertEqual(self.client.post(self.star_url).data["star_count"], 0)

    def test_session_write_checks_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="education-owner", password="test-password")
        self.assertEqual(client.post(
            self.list_url, self.payload, format="json",
        ).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), 1)
