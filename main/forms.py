from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput

from main.models import Experience, Education


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Jenis Pengalaman",
            "thumnail": "Logo institusi",
            "started_at": "Tanggal mulai",
            "ended_at": "Tanggal selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Judul pengalamanmu",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select"
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "(opsional)",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),

            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),

        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution_name",
            "degree",
            "field_of_study",
            "logo_url",
            "description",
            "ended_at",
        ]

        labels = {
            "institution_name": "Nama Institusi",
            "degree": "Jenjang Pendidikan",
            "field_of_study": "Bidang Studi",
            "logo_url": "URL Logo Institusi",
            "description": "Deskripsi",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "institution_name": TextInput(
                attrs={
                    "placeholder": "Nama sekolah/universitas",
                    "maxlength": 255,
                }
            ),
            "degree": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "field_of_study": TextInput(
                attrs={
                    "placeholder": "Contoh: Ilmu Komputer",
                    "maxlength": 255,
                }
            ),
            "logo_url": URLInput(
                attrs={
                    "placeholder": "(opsional)",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalaman pendidikanmu",
                    "rows": 3,
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "datetime-local",
                },
            ),
        }

    # Sanitasi XSS di sisi server: buang tag HTML dari setiap input teks
    # sebelum divalidasi lebih lanjut dan disimpan ke database.
    def clean_institution_name(self):
        institution_name = strip_tags(
            self.cleaned_data["institution_name"]).strip()
        if not institution_name:
            raise ValidationError(
                "Nama institusi tidak boleh hanya berisi tag HTML.")
        return institution_name

    def clean_field_of_study(self):
        field_of_study = strip_tags(
            self.cleaned_data["field_of_study"]).strip()
        if not field_of_study:
            raise ValidationError(
                "Bidang studi tidak boleh hanya berisi tag HTML.")
        return field_of_study

    def clean_logo_url(self):
        logo_url = strip_tags(self.cleaned_data.get("logo_url") or "").strip()
        # Hanya izinkan URL http(s) agar skema berbahaya (mis. javascript:)
        # tidak pernah tersimpan sebagai sumber gambar.
        if logo_url and not logo_url.lower().startswith(("http://", "https://")):
            raise ValidationError(
                "URL logo harus diawali dengan http:// atau https://.")
        return logo_url or None

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

