import json

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=timezone.now().date(),
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class EducationTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution_name="SMA Negeri 1 Contoh",
            degree="high-school",
            field_of_study="IPA",
            description="Fokus pada pengembangan web dan rekayasa perangkat lunak.",
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_page_shows_data_when_available(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, self.education.institution_name)
        self.assertContains(response, self.education.field_of_study)
        self.assertContains(response, "High School")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(
            response, f'href="{reverse("main:show_education")}"')

    def test_education_page_shows_empty_state_when_no_data(self):
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response, "Belum ada riwayat pendidikan yang ditambahkan.")
        self.assertNotContains(response, self.education.institution_name)

    def test_education_model(self):
        self.assertEqual(
            str(self.education),
            "high-school - SMA Negeri 1 Contoh",
        )
        self.assertTrue(self.education.is_ongoing)

    def test_completed_education(self):
        self.education.ended_at = timezone.now()
        self.education.save()
        response = self.client.get(reverse("main:show_education"))

        self.assertFalse(self.education.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_get_education_json(self):
        response = self.client.get(reverse("main:get_education_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["fields"]["institution_name"],
            self.education.institution_name,
        )

    def test_get_education_json_filtered_by_degree(self):
        response = self.client.get(
            reverse("main:get_education_json"), {"degree": "bachelor"}
        )
        data = json.loads(response.content)

        self.assertEqual(len(data), 0)

    def test_create_education_form_page_is_accessible(self):
        response = self.client.get(reverse("main:create_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education_form.html")

    def test_create_education_post_adds_new_entry(self):
        response = self.client.post(
            reverse("main:create_education"),
            {
                "institution_name": "Universitas Indonesia",
                "degree": "bachelor",
                "field_of_study": "Ilmu Komputer",
                "logo_url": "",
                "description": "Program studi S1 Ilmu Komputer.",
                "ended_at": "",
            },
        )

        self.assertRedirects(response, reverse("main:show_education"))
        self.assertEqual(Education.objects.count(), 2)
        self.assertTrue(
            Education.objects.filter(
                institution_name="Universitas Indonesia").exists()
        )

    def test_update_education_form_prefilled_and_saves_changes(self):
        response = self.client.get(
            reverse("main:update_education", args=[self.education.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education_form.html")
        self.assertContains(response, self.education.institution_name)

        response = self.client.post(
            reverse("main:update_education", args=[self.education.id]),
            {
                "institution_name": "SMA Negeri 1 Contoh (Updated)",
                "degree": "high-school",
                "field_of_study": "IPA",
                "logo_url": "",
                "description": "Deskripsi yang diperbarui.",
                "ended_at": "",
            },
        )

        self.assertRedirects(response, reverse("main:show_education"))
        self.education.refresh_from_db()
        self.assertEqual(
            self.education.institution_name, "SMA Negeri 1 Contoh (Updated)"
        )

    def test_delete_education_removes_entry(self):
        response = self.client.post(
            reverse("main:delete_education", args=[self.education.id])
        )

        self.assertRedirects(response, reverse("main:show_education"))
        self.assertFalse(
            Education.objects.filter(pk=self.education.id).exists())
