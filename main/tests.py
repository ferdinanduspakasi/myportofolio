import json

from django.contrib.auth.models import Group, User
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
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, reverse("main:get_experience_json"))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experience_json(self):
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        fields = data[0]["fields"]
        self.assertEqual(fields["title"], self.experience.title)
        self.assertEqual(fields["description"], self.experience.description)
        self.assertEqual(fields["category"], "Part-Time")
        self.assertTrue(fields["is_ongoing"])
        self.assertEqual(fields["star_count"], 0)
        self.assertFalse(fields["is_starred"])

    def test_experience_json_search(self):
        r = self.client.get(reverse("main:get_experience_json"), {"title": "zzz"})
        self.assertEqual(json.loads(r.content), [])
        r = self.client.get(reverse("main:get_experience_json"), {"title": "asisten"})
        self.assertEqual(len(json.loads(r.content)), 1)

    def test_empty_experience_json(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertEqual(json.loads(response.content), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:get_experience_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(json.loads(response.content)[0]["fields"]["is_ongoing"])


class EducationTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution_name="SMA Negeri 1 Contoh",
            degree="high-school",
            field_of_study="IPA",
            description="Fokus pada pengembangan web dan rekayasa perangkat lunak.",
        )
        self.owner = User.objects.create_superuser(
            "owner", password="pw12345!")
        self.client.force_login(self.owner)

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
<<<<<<< HEAD
<<<<<<< Updated upstream
=======
=======
>>>>>>> origin/main


class EducationAuthorizationTest(TestCase):
    """Empat peran: pengunjung, pengguna biasa, Editor, dan pemilik (superuser)."""

    FORM = {
        "institution_name": "Kampus Baru",
        "degree": "bachelor",
        "field_of_study": "Ilmu Komputer",
        "logo_url": "",
        "description": "x",
        "ended_at": "",
    }

    def setUp(self):
        self.education = Education.objects.create(
            institution_name="SMA Contoh", degree="high-school",
            field_of_study="IPA")
        self.user = User.objects.create_user("biasa", password="pw12345!")
        self.editor = User.objects.create_user("editor", password="pw12345!")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.owner = User.objects.create_superuser(
            "owner", password="pw12345!")
        self.create_url = reverse("main:create_education")
        self.update_url = reverse(
            "main:update_education", args=[self.education.id])
        self.delete_url = reverse(
            "main:delete_education", args=[self.education.id])
        self.star_url = reverse(
            "main:toggle_education_star", args=[self.education.id])

    # --- pengunjung tanpa login
    def test_anonymous_can_read_but_is_redirected_for_actions(self):
        self.assertEqual(self.client.get(
            reverse("main:show_education")).status_code, 200)
        self.assertEqual(self.client.get(
            reverse("main:get_education_json")).status_code, 200)
        for url in (self.create_url, self.update_url):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 302)
            self.assertTrue(r["Location"].startswith("/login/"))
        for url in (self.delete_url, self.star_url):
            r = self.client.post(url)
            self.assertEqual(r.status_code, 302)
            self.assertTrue(r["Location"].startswith("/login/"))
        self.assertTrue(Education.objects.filter(
            pk=self.education.pk).exists())

    def test_anonymous_sees_no_action_buttons(self):
        r = self.client.get(reverse("main:show_education"))
        self.assertNotContains(r, self.create_url)
        self.assertNotContains(r, self.update_url)
        self.assertNotContains(r, self.delete_url)

    # --- pengguna biasa
    def test_regular_user_forbidden_on_write_actions(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.post(
            self.create_url, self.FORM).status_code, 403)
        self.assertEqual(self.client.get(self.update_url).status_code, 403)
        self.assertEqual(self.client.post(
            self.update_url, self.FORM).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "SMA Contoh")

    def test_regular_user_sees_star_but_no_action_buttons(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("main:show_education"))
        self.assertContains(r, self.star_url)
        self.assertNotContains(r, self.create_url)
        self.assertNotContains(r, self.update_url)
        self.assertNotContains(r, self.delete_url)

    # --- editor
    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_login(self.editor)
        self.assertEqual(self.client.get(self.update_url).status_code, 200)
        r = self.client.post(
            self.update_url, {**self.FORM, "institution_name": "Diubah"})
        self.assertRedirects(r, reverse("main:show_education"))
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "Diubah")
        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.post(
            self.create_url, self.FORM).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_sees_edit_button_only(self):
        self.client.force_login(self.editor)
        r = self.client.get(reverse("main:show_education"))
        self.assertContains(r, self.update_url)
        self.assertNotContains(r, self.create_url)
        self.assertNotContains(r, self.delete_url)

    # --- superuser
    def test_owner_can_create_update_delete(self):
        self.client.force_login(self.owner)
        self.client.post(self.create_url, self.FORM)
        self.assertEqual(Education.objects.count(), 2)
        self.client.post(self.update_url, {
                         **self.FORM, "institution_name": "Owner Edit"})
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution_name, "Owner Edit")
        self.client.post(self.delete_url)
        self.assertFalse(Education.objects.filter(
            pk=self.education.pk).exists())

    # --- star
    def test_star_toggle_max_one_per_user_and_counts(self):
        self.client.force_login(self.user)
        self.client.post(self.star_url)
        self.assertEqual(self.education.starred_by.count(), 1)
        r = self.client.get(reverse("main:show_education"))
        self.assertContains(r, "Unstar")
        self.client.force_login(self.editor)
        self.client.post(self.star_url)
        self.assertEqual(self.education.starred_by.count(), 2)
        self.client.force_login(self.user)
        self.client.post(self.star_url)  # batalkan
        self.assertEqual(self.education.starred_by.count(), 1)
        self.assertFalse(self.education.starred_by.filter(
            pk=self.user.pk).exists())

    def test_star_get_does_not_toggle(self):
        self.client.force_login(self.user)
        r = self.client.get(self.star_url)
        self.assertRedirects(r, reverse("main:show_education"))
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_star_requires_csrf_token(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        c.force_login(self.user)
        self.assertEqual(c.post(self.star_url).status_code, 403)

    # --- JSON
    def test_json_does_not_leak_user_data(self):
        self.education.starred_by.add(self.user, self.editor)
        r = self.client.get(reverse("main:get_education_json"))
        item = json.loads(r.content)[0]
        self.assertNotIn("starred_by", item["fields"])
        self.assertNotIn("biasa", r.content.decode())
        self.assertNotIn("owner", r.content.decode())


class RoleBadgeTest(TestCase):
    """Lencana peran di navbar tampil sesuai peran akun, di semua halaman."""

    def setUp(self):
        self.user = User.objects.create_user("biasa", password="pw12345!")
        self.editor = User.objects.create_user("editor", password="pw12345!")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.owner = User.objects.create_superuser(
            "owner", password="pw12345!")

    def badge(self, user, url_name="main:show_main"):
        if user:
            self.client.force_login(user)
        return self.client.get(reverse(url_name))

    def test_anonymous_has_no_badge(self):
        self.assertNotContains(self.badge(None), "role-badge")

    def test_regular_user_badge(self):
        r = self.badge(self.user)
        self.assertContains(r, "role-badge--user")
        self.assertContains(r, ">User</span>")

    def test_editor_badge(self):
        self.assertContains(self.badge(self.editor), "role-badge--editor")

    def test_owner_badge_wins_over_editor_group(self):
        self.owner.groups.add(Group.objects.get(name="Editor"))
        r = self.badge(self.owner)
        self.assertContains(r, "role-badge--owner")
        self.assertNotContains(r, "role-badge--editor")

    def test_badge_shown_on_other_pages(self):
        for name in ("main:show_experience", "main:show_education"):
            self.assertContains(self.badge(
                self.editor, name), "role-badge--editor")
<<<<<<< HEAD


class ExperienceAjaxTest(TestCase):
    payload = {
        "title": "Panitia Acara",
        "description": "Mengurus acara kampus.",
        "category": "volunteer",
        "started_at": "2026-01-01",
    }

    def setUp(self):
        self.owner = User.objects.create_superuser("owner", password="pw12345!")
        self.user = User.objects.create_user("biasa", password="pw12345!")
        self.url = reverse("main:create_experience_ajax")

    def test_owner_can_create(self):
        self.client.force_login(self.owner)
        r = self.client.post(self.url, self.payload)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Experience.objects.count(), 1)

    def test_anonymous_and_regular_user_get_403_json(self):
        self.assertEqual(self.client.post(self.url, self.payload).status_code, 403)
        self.client.force_login(self.user)
        r = self.client.post(self.url, self.payload)
        self.assertEqual(r.status_code, 403)
        self.assertIn("message", r.json())
        self.assertEqual(Experience.objects.count(), 0)

    def test_get_not_allowed(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_invalid_returns_400_with_errors(self):
        self.client.force_login(self.owner)
        r = self.client.post(self.url, {**self.payload, "title": "   "})
        self.assertEqual(r.status_code, 400)
        self.assertIn("title", r.json()["errors"])

    def test_html_only_title_rejected_and_tags_stripped(self):
        self.client.force_login(self.owner)
        r = self.client.post(
            self.url, {**self.payload, "title": "<img src=x onerror=alert(1)>"})
        self.assertEqual(r.status_code, 400)
        r = self.client.post(
            self.url, {**self.payload, "description": "Halo <b>dunia</b>"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Experience.objects.get().description, "Halo dunia")

    def test_javascript_url_rejected(self):
        self.client.force_login(self.owner)
        r = self.client.post(
            self.url, {**self.payload, "thumbnail": "javascript:alert(1)"})
        self.assertEqual(r.status_code, 400)

    def test_json_reflects_star_state(self):
        exp = Experience.objects.create(
            title="X", description="d", started_at=timezone.now().date())
        exp.starred_by.add(self.user)
        self.client.force_login(self.user)
        f = json.loads(self.client.get(reverse("main:get_experience_json")).content)[0]["fields"]
        self.assertTrue(f["is_starred"])
        self.assertEqual(f["star_count"], 1)
        self.assertEqual(f["starred_by_names"], "biasa")
>>>>>>> Stashed changes
=======
>>>>>>> origin/main
